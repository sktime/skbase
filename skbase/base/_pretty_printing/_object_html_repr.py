# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# Many elements of this code were developed in scikit-learn. These elements
# are copyrighted by the scikit-learn developers, BSD-3-Clause License. For
# conditions see https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
"""Functionality to represent instances of BaseObject as HTML."""

import html
import inspect
import re
import reprlib
import uuid
from contextlib import closing
from functools import lru_cache
from importlib import resources
from inspect import isclass
from io import StringIO
from string import Template
from urllib.parse import quote

__author__ = ["RNKuhns"]


class _HTMLDocumentationLinkMixin:
    """Mixin for generating API documentation links in object HTML diagrams.

    Classes can opt in by inheriting from this mixin or by defining compatible
    class/instance attributes:

    - ``_doc_link_module``: root module that is allowed to receive doc links.
      Defaults to ``"skbase"``. Set to ``None`` to allow any root module.
    - ``_doc_link_template``: format string used to build the link. The default
      is a generic skbase ReadTheDocs API reference URL.
    - ``_doc_link_url_param_generator``: optional callable returning a dict of
      additional format parameters for custom templates.
    """

    _doc_link_module = "skbase"
    _doc_link_template = (
        "https://skbase.readthedocs.io/en/latest/api_reference/auto_generated/"
        "{object_module}.{object_name}.html"
    )
    _doc_link_url_param_generator = None

    def _get_doc_link(self):
        """Generate a documentation URL for this object, or ``""`` if disabled."""
        return _get_doc_link(self)


class _VisualBlock:
    """HTML Representation of BaseObject.

    Parameters
    ----------
    kind : {'serial', 'parallel', 'single'}
        kind of HTML block

    estimators : list of ``BaseObject``s or ``_VisualBlock``s or a single ``BaseObject``
        If ``kind != 'single'``, then ``estimators`` is a list of ``BaseObjects``.
        If ``kind == 'single'``, then ``estimators`` is a single ``BaseObject``.

    names : list of str, default=None
        If ``kind != 'single'``, then ``names`` corresponds to ``BaseObjects``.
        If ``kind == 'single'``, then ``names`` is a single string corresponding to
        the single ``BaseObject``.

    name_details : list of str, str, or None, default=None
        If ``kind != 'single'``, then ``name_details`` corresponds to ``names``.
        If ``kind == 'single'``, then ``name_details`` is a single string
        corresponding to the single ``BaseObject``.

    name_caption : str, default=None
        The caption below the name. ``None`` stands for no caption.
        Only active when ``kind == 'single'``.

    doc_link_label : str, default=None
        The label for the documentation link. If provided, the label is
        "Documentation for {doc_link_label}". Otherwise it uses ``names``.
        Only active when ``kind == 'single'``.

    dash_wrapped : bool, default=True
        If true, wrapped HTML element will be wrapped with a dashed border.
        Only active when ``kind != 'single'``.
    """

    def __init__(
        self,
        kind,
        estimators,
        *,
        names=None,
        name_details=None,
        name_caption=None,
        doc_link_label=None,
        dash_wrapped=True,
    ):
        self.kind = kind
        self.estimators = estimators
        self.dash_wrapped = dash_wrapped
        self.name_caption = name_caption
        self.doc_link_label = doc_link_label

        if self.kind in ("parallel", "serial"):
            if names is None:
                names = (None,) * len(estimators)
            if name_details is None:
                name_details = (None,) * len(estimators)

        self.names = names
        self.name_details = name_details

    def _sk_visual_block_(self):
        return self


@lru_cache
def _get_resource(name):
    """Read a packaged pretty-printing resource."""
    return (
        resources.files("skbase.base._pretty_printing")
        .joinpath(name)
        .read_text(encoding="utf-8")
    )


def _get_css_style():
    """Return CSS used by the HTML representation."""
    return _get_resource("_object_html_repr.css")


def _get_js():
    """Return JavaScript used by the HTML representation."""
    return _get_resource("_object_html_repr.js")


@lru_cache
def _get_param_doc_descriptions(docstring):
    """Parse a small subset of NumPy-style parameter docs.

    The parser intentionally stays lightweight to avoid a hard numpydoc
    dependency in skbase. It extracts parameter type lines and indented
    description text from a ``Parameters`` section.
    """
    if not docstring:
        return {}

    lines = inspect.cleandoc(docstring).splitlines()
    in_parameters = False
    params = {}
    current = None

    for idx, line in enumerate(lines):
        stripped = line.strip()
        next_line = lines[idx + 1].strip() if idx + 1 < len(lines) else ""

        if not in_parameters:
            if stripped == "Parameters" and set(next_line) <= {"-"} and next_line:
                in_parameters = True
            continue

        if stripped and set(stripped) <= {"-"}:
            continue

        # A non-indented heading followed by an underline starts the next section.
        if line == stripped and stripped and set(next_line) <= {"-"} and next_line:
            break

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+)$", stripped)
        if match:
            current = match.group(1)
            params[current] = {"type": match.group(2), "desc": []}
            continue

        if current is not None:
            if not stripped:
                continue
            params[current]["desc"].append(stripped)

    return params


def _generate_link_to_param_doc(object_class, param_name, doc_link):
    """Generate a text-fragment URL to a parameter docstring entry."""
    docstring = inspect.getdoc(object_class)
    param_map = _get_param_doc_descriptions(docstring)
    param_doc = param_map.get(param_name)

    if param_doc is None:
        return None

    text_fragment = f"{quote(param_name)},-{quote(param_doc['type'])}"
    return f"{doc_link}#:~:text={text_fragment}"


def _get_doc_link(base_object):
    """Return the configured documentation link for ``base_object``."""
    if base_object is None or isinstance(base_object, str) or isclass(base_object):
        return ""

    direct_link = getattr(base_object, "_html_repr_doc_link", None)
    if direct_link:
        return direct_link

    get_doc_link = getattr(base_object, "_get_doc_link", None)
    mixin_get_doc_link = _HTMLDocumentationLinkMixin._get_doc_link
    is_mixin_doc_link = getattr(get_doc_link, "__func__", None) is mixin_get_doc_link
    if get_doc_link is not None and not is_mixin_doc_link:
        try:
            return get_doc_link()
        except Exception:
            return ""

    template = getattr(base_object, "_doc_link_template", None)
    if not template:
        return ""

    module_name = base_object.__class__.__module__
    root_module = module_name.split(".")[0]
    doc_link_module = getattr(base_object, "_doc_link_module", None)
    if doc_link_module is not None and root_module != doc_link_module:
        return ""

    generator = getattr(base_object, "_doc_link_url_param_generator", None)
    if generator is None:
        object_name = base_object.__class__.__name__
        params = {
            "object_module": module_name,
            "object_name": object_name,
            "estimator_module": module_name,
            "estimator_name": object_name,
        }
    else:
        try:
            params = generator()
        except Exception:
            return ""

    try:
        return template.format(**params)
    except Exception:
        return ""


def _get_fitted_status(base_object):
    """Return CSS/status icon for BaseEstimator-like fitted state."""
    if not hasattr(base_object, "is_fitted"):
        return "", ""

    try:
        is_fitted = bool(base_object.is_fitted)
    except Exception:
        is_fitted = False

    status_label = "Fitted" if is_fitted else "Not fitted"
    css_class = "fitted" if is_fitted else ""
    status_icon = (
        f'<span class="sk-estimator-doc-link {css_class}">'
        f"i<span>{status_label}</span></span>"
    )

    return css_class, status_icon


def _changed_param_names(base_object):
    """Return shallow parameter names with non-default values."""
    try:
        from skbase.base._pretty_printing._pprint import _changed_params

        return tuple(_changed_params(base_object))
    except Exception:
        return ()


def _read_param(name, value, non_default_params):
    """Categorize and format a parameter value for HTML display."""
    repr_instance = reprlib.Repr()
    repr_instance.maxdict = 2
    repr_instance.maxlist = 2
    repr_instance.maxset = 2
    repr_instance.maxstring = 50
    repr_instance.maxtuple = 1
    repr_instance.maxother = 80

    return {
        "param_type": "user-set" if name in non_default_params else "default",
        "param_type_extra": (
            "sk-param-row--changed"
            if name in non_default_params
            else "sk-param-row--default"
        ),
        "param_name": html.escape(name),
        "param_value": html.escape(repr_instance.repr(value)),
    }


def _params_html_repr(base_object, doc_link=""):
    """Generate HTML table with shallow parameters for ``base_object``."""
    if not hasattr(base_object, "get_params") or isclass(base_object):
        return ""

    try:
        params = base_object.get_params(deep=False)
    except Exception:
        return ""

    if not isinstance(params, dict) or not params:
        return ""

    non_default_params = _changed_param_names(base_object)
    object_class = base_object.__class__
    param_doc_map = _get_param_doc_descriptions(inspect.getdoc(object_class))

    rows = []
    for param_name, value in params.items():
        param = _read_param(param_name, value, non_default_params)
        param_display = param["param_name"]

        param_doc = param_doc_map.get(param_name)
        param_link = (
            _generate_link_to_param_doc(object_class, param_name, doc_link)
            if doc_link
            else None
        )
        if param_link and param_doc:
            param_link = html.escape(param_link, quote=True)
            description = (
                f"{html.escape(param_name)}: {html.escape(param_doc['type'])}"
                "<br><br>"
                f"{'<br>'.join(html.escape(x) for x in param_doc['desc'])}"
            )
            param_display = (
                '<a class="param-doc-link" rel="noreferrer" target="_blank" '
                'href="{}">{}<span class="param-doc-description">{}</span></a>'
            ).format(param_link, param["param_name"], description)

        rows.append(
            '<tr class="{param_type} {param_type_extra}">'
            '<td><i class="copy-paste-icon sk-copy-btn" '
            "onclick=\"skbaseCopyToClipboard('{raw_name}', "
            'this.parentElement.nextElementSibling)"></i></td>'
            '<td class="param">{param_display}</td>'
            '<td class="value">{param_value}</td>'
            "</tr>".format(
                raw_name=html.escape(param_name, quote=True),
                param_display=param_display,
                **param,
            )
        )

    return (
        '<div class="estimator-table">'
        "<details>"
        "<summary>Parameters</summary>"
        '<table class="parameters-table sk-params-table"><tbody>'
        f"{''.join(rows)}"
        "</tbody></table>"
        "</details>"
        "</div>"
    )


def _write_label_html(
    out,
    name,
    name_details,
    params="",
    name_caption=None,
    doc_link_label=None,
    outer_class="sk-label-container",
    inner_class="sk-label",
    checked=False,
    doc_link="",
    is_fitted_css_class="",
    is_fitted_icon="",
    param_prefix="",
):
    """Write labeled HTML with or without a dropdown with named details."""
    out.write(
        '<div class="{}"><div class="{} {} sk-toggleable">'.format(
            outer_class,
            inner_class,
            is_fitted_css_class,
        )
    )
    raw_name = str(name)
    name = html.escape(raw_name)

    if name_details is not None or params:
        checked_str = "checked" if checked else ""
        est_id = "sk-estimator-id-" + str(uuid.uuid4())

        if doc_link:
            label = html.escape(
                str(doc_link_label) if doc_link_label is not None else raw_name
            )
            doc_link = (
                '<a class="sk-estimator-doc-link {}" '
                'rel="noreferrer" target="_blank" '
                'href="{}">?<span>Documentation for {}</span></a>'
            ).format(is_fitted_css_class, html.escape(doc_link, quote=True), label)

        name_caption_div = (
            ""
            if name_caption is None
            else f'<div class="caption">{html.escape(str(name_caption))}</div>'
        )
        name_caption_div = f"<div><div>{name}</div>{name_caption_div}</div>"
        links_div = (
            f"<div>{doc_link}{is_fitted_icon}</div>"
            if doc_link or is_fitted_icon
            else ""
        )
        label_html = (
            '<label for="{}" class="sk-toggleable__label {} '
            'sk-toggleable__label-arrow">{}{}</label>'
        ).format(est_id, is_fitted_css_class, name_caption_div, links_div)

        out.write(
            '<input class="sk-toggleable__control sk-hidden--visually" '
            'id="{}" type="checkbox" {}>{}'
            '<div class="sk-toggleable__content {}" data-param-prefix="{}">'.format(
                est_id,
                checked_str,
                label_html,
                is_fitted_css_class,
                html.escape(param_prefix, quote=True),
            )
        )
        if params:
            out.write(params)
        elif name_details is not None:
            out.write(f"<pre>{html.escape(str(name_details))}</pre>")
        out.write("</div>")
    else:
        out.write(f"<label>{name}</label>")
    out.write("</div></div>")  # outer_class inner_class


def _get_visual_block(base_object):
    """Generate information about how to display a BaseObject."""
    if hasattr(base_object, "_sk_visual_block_"):
        try:
            return base_object._sk_visual_block_()
        except Exception:
            return _VisualBlock(
                "single",
                base_object,
                names=base_object.__class__.__name__,
                name_details=str(base_object),
            )

    if isinstance(base_object, str):
        return _VisualBlock(
            "single", base_object, names=base_object, name_details=base_object
        )
    elif base_object is None:
        return _VisualBlock("single", base_object, names="None", name_details="None")

    # collect BaseObject-like instances in the first layer to display in parallel
    if hasattr(base_object, "get_params") and not isclass(base_object):
        base_objects = []
        try:
            params = base_object.get_params(deep=False)
        except Exception:
            params = {}

        for key, value in params.items():
            # Recurse to nested BaseObject-like instances in the first layer only.
            if hasattr(value, "get_params") and not isclass(value):
                base_objects.append((key, value))
        if base_objects:
            return _VisualBlock(
                "parallel",
                [obj for _, obj in base_objects],
                names=[f"{key}: {obj.__class__.__name__}" for key, obj in base_objects],
                name_details=[str(obj) for _, obj in base_objects],
            )

    return _VisualBlock(
        "single",
        base_object,
        names=base_object.__class__.__name__,
        name_details=str(base_object),
    )


def _param_prefix_for_child(param_prefix, name):
    """Return nested parameter prefix for a child label."""
    if not isinstance(name, str):
        return param_prefix

    child_name = name.split(":", 1)[0]
    if not child_name:
        return param_prefix
    return f"{param_prefix}{child_name}__"


def _write_base_object_html(
    out,
    base_object,
    base_object_label,
    base_object_label_details,
    first_call=False,
    param_prefix="",
):
    """Write BaseObject to HTML in serial, parallel, or by itself (single)."""
    est_block = _get_visual_block(base_object)
    doc_link = _get_doc_link(base_object)
    is_fitted_css_class, is_fitted_icon = _get_fitted_status(base_object)

    if est_block.kind in ("serial", "parallel"):
        dashed_wrapped = first_call or est_block.dash_wrapped
        dash_cls = " sk-dashed-wrapped" if dashed_wrapped else ""
        out.write(f'<div class="sk-item{dash_cls}">')

        if base_object_label:
            params = _params_html_repr(base_object, doc_link=doc_link)
            _write_label_html(
                out,
                base_object_label,
                base_object_label_details,
                params=params,
                doc_link=doc_link,
                is_fitted_css_class=is_fitted_css_class,
                is_fitted_icon=is_fitted_icon,
                param_prefix=param_prefix,
            )

        kind = est_block.kind
        out.write(f'<div class="sk-{kind}">')
        est_infos = zip(est_block.estimators, est_block.names, est_block.name_details)

        for est, name, name_details in est_infos:
            new_prefix = _param_prefix_for_child(param_prefix, name)
            if kind == "serial":
                _write_base_object_html(
                    out,
                    est,
                    name,
                    name_details,
                    param_prefix=new_prefix,
                )
            else:  # parallel
                out.write('<div class="sk-parallel-item">')
                # wrap element in a serial visualblock
                serial_block = _VisualBlock("serial", [est], dash_wrapped=False)
                _write_base_object_html(
                    out,
                    serial_block,
                    name,
                    name_details,
                    param_prefix=new_prefix,
                )
                out.write("</div>")  # sk-parallel-item

        out.write("</div></div>")
    elif est_block.kind == "single":
        params = _params_html_repr(base_object, doc_link=doc_link)
        _write_label_html(
            out,
            est_block.names,
            est_block.name_details,
            params=params,
            name_caption=est_block.name_caption,
            doc_link_label=est_block.doc_link_label,
            outer_class="sk-item",
            inner_class="sk-estimator",
            checked=first_call,
            doc_link=doc_link,
            is_fitted_css_class=is_fitted_css_class,
            is_fitted_icon=is_fitted_icon,
            param_prefix=param_prefix,
        )


def _object_html_repr(base_object):
    """Build a HTML representation of a BaseObject.

    Parameters
    ----------
    base_object : base object
        The BaseObject or inheriting class to visualize.

    Returns
    -------
    html: str
        HTML representation of BaseObject.
    """
    with closing(StringIO()) as out:
        container_id = "sk-container-id-" + str(uuid.uuid4())
        style_template = Template(_get_css_style())
        style_with_id = style_template.substitute(id=container_id)
        base_object_str = str(base_object)

        # The fallback message is shown by default and loading the CSS sets
        # div.sk-text-repr-fallback to display: none to hide the fallback message.
        #
        # If the notebook is trusted, the CSS is loaded which hides the fallback
        # message. If the notebook is not trusted, then the CSS is not loaded and the
        # fallback message is shown by default.
        #
        # The reverse logic applies to HTML repr div.sk-container.
        # div.sk-container is hidden by default and the loading the CSS displays it.
        fallback_msg = (
            "In a Jupyter environment, please rerun this cell to show the HTML "
            "representation or trust the notebook. <br />On GitHub, the HTML "
            "representation is unable to render, please try loading this page "
            "with nbviewer.org."
        )
        out.write(
            (
                "<style>{}</style>"
                '<div id="{}" class="sk-top-container">'
                '<div class="sk-text-repr-fallback">'
                "<pre>{}</pre><b>{}</b>"
                "</div>"
                '<div class="sk-container" hidden>'
            ).format(
                style_with_id,
                container_id,
                html.escape(base_object_str),
                fallback_msg,
            )
        )
        _write_base_object_html(
            out,
            base_object,
            base_object.__class__.__name__,
            base_object_str,
            first_call=True,
        )
        script = _get_js()
        out.write(
            "</div></div><script>{}\nskbaseForceTheme('{}');</script>".format(
                script,
                container_id,
            )
        )

        html_output = out.getvalue()
        return html_output
