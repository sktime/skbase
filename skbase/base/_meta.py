#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: skbase developers, BSD-3-Clause License (see LICENSE file)
# BaseMetaObject and BaseMetaEstimator reuse code developed in scikit-learn and sktime.
# These elements are copyrighted by the respective
# scikit-learn developers (BSD-3-Clause License) and sktime (BSD-3-Clause) developers.
# For conditions see licensing:
# scikit-learn: https://github.com/scikit-learn/scikit-learn/blob/main/COPYING
# sktime:  https://github.com/sktime/sktime/blob/main/LICENSE
"""Implements functionality for meta objects composed of other objects."""
from inspect import isclass

from skbase.base._base import BaseEstimator, BaseObject
from skbase.base._pretty_printing._object_html_repr import _VisualBlock
from skbase.utils._iter import _format_seq_to_str, make_strings_unique
from skbase.validate import is_named_object_tuple

__author__ = ["mloning", "fkiraly", "RNKuhns"]
__all__ = ["BaseMetaEstimator", "BaseMetaObject"]


class _MetaObjectMixin:
    """Parameter and tag management for objects composed of named objects.

    Allows objects to get and set nested parameters when a parameter of the the
    class has values that follow the named object specification. For example,
    in a pipeline class with the the "step" parameter accepting named objects,
    this would allow `get_params` and `set_params` to retrieve and update the
    parameters of the objects in each step.

    Notes
    -----
    Partly adapted from sklearn utils.metaestimator.py and sktime's
    _HeterogenousMetaEstimator.
    """

    # for default get_params/set_params from _HeterogenousMetaEstimator
    # _steps_attr points to the attribute of self
    # which contains the heterogeneous set of estimators
    # this must be an iterable of (name: str, estimator) pairs for the default
    _tags = {"named_object_parameters": "steps"}

    def is_composite(self):
        """Check if the object is composite.

        A composite object is an object which contains objects as parameter values.

        Returns
        -------
        bool
            Whether self contains a parameter whose value is a BaseObject,
            list of (str, BaseObject) tuples or dict[str, BaseObject].
        """
        # children of this class are always composite
        return True

    def get_params(self, deep=True):
        """Get a dict of parameters values for this object.

        This expands on `get_params` of standard `BaseObject` by also retrieving
        components parameters when ``deep=True`` a component's follows the named
        object API (either sequence of str, BaseObject tuples or dict[str, BaseObject]).

        Parameters
        ----------
        deep : bool, default=True
            Whether to return parameters of components.

            - If True, will return a dict of parameter name : value for this object,
              including parameters of components.
            - If False, will return a dict of parameter name : value for this object,
              but not include parameters of components.

        Returns
        -------
        dict[str, Any]
            Dictionary of parameter name and value pairs. Includes direct parameters
            and indirect parameters whose values implement `get_params` or follow
            the named object API (either sequence of str, BaseObject tuples or
            dict[str, BaseObject]).

            - If ``deep=False`` the name-value pairs for this object's direct
              parameters (you can see these via `get_param_names`) are returned.
            - If ``deep=True`` then the parameter name-value pairs are returned
              for direct and component (indirect) parameters.

              - When a BaseObject's direct parameter value implements `get_params`
                the component parameters are returned as
                `[direct_param_name]__[component_param_name]` for 1st level components.
                Arbitrary levels of component recursion are supported (if the
                component has parameter's whose values are objects that implement
                `get_params`). In this case, return parameters follow
                `[direct_param_name]__[component_param_name]__[param_name]` format.
              - When a BaseObject's direct parameter value is a sequence of
                (name, BaseObject) tuples or dict[str, BaseObject] the parameters name
                and value pairs of all component objects are returned. The
                parameter naming follows ``scikit-learn`` convention of treating
                named component objects like they are direct parameters; therefore,
                the names are assigned as `[component_param_name]__[param_name]`.
        """
        # Use tag interface that will be available when mixin is used
        named_object_attr = self.get_tag("named_object_parameters")  # type: ignore
        return self._get_params(named_object_attr, deep=deep)

    def set_params(self, **kwargs):
        """Set the object's direct parameters and the parameters of components.

        Valid parameter keys can be listed with ``get_params()``.

        Like `BaseObject` implementation it allows values of indirect parameters
        of a component to be set when a parameter's value is an object that
        implements `set_params`. This also also expands the functionality to
        allow parameter to allow the indirect parameters of components to be set
        when a parameter's values follow the named object API (either sequence
        of str, BaseObject tuples or dict[str, BaseObject]).

        Returns
        -------
        Self
            Instance of self.
        """
        # Use tag interface that will be available when mixin is used
        named_object_attr = self.get_tag("named_object_parameters")  # type: ignore
        return self._set_params(named_object_attr, **kwargs)

    def _get_fitted_params(self):
        """Get fitted parameters.

        Method implements logic to retrieve fitted parameters. It is called from
        get_fitted_params.

        Returns
        -------
        dict[str, Any]
            Fitted parameters where keys represent the parameters name (with
            trailing "_" removed) and the corresponding value is the value of
            the parameter learned during fit.
        """
        fitted_params = self._get_fitted_params_default()

        fitted_named_object_attr = self.get_tag(
            "fitted_named_object_parameters"
        )  # type: ignore

        named_objects_fitted_params = self._get_params(
            fitted_named_object_attr, fitted=True
        )

        fitted_params.update(named_objects_fitted_params)

        return fitted_params

    def _get_params(self, attr, deep=True, fitted=False):
        """Logic for getting parameters on meta objects/estimators.

        Separates out logic for parameter getting on meta objects from public API point.

        Parameters
        ----------
        attr : str
            Name of parameter whose values should contain named objects.
        deep : bool, default=True
            Whether to return parameters of components.

            - If True, will return a dict of parameter name : value for this object,
              including parameters of components.
            - If False, will return a dict of parameter name : value for this object,
              but not include parameters of components.

        fitted : bool, default=False
            Whether to retrieve the fitted params learned when `fit` is called on
            ``estimator`` instead of the instances parameters.

            - If False, then retrieve instance parameters like typical.
            - If True, the retrieves the parameters learned during "fitting" and
              stored in attributes ending in "_" (private attributes excluded).

        Returns
        -------
        dict[str, Any]
            Dictionary of parameter name and value pairs. Includes direct parameters
            and indirect parameters whose values implement `get_params` or follow
            the named object API (either sequence of str, BaseObject tuples or
            dict[str, BaseObject]).
        """
        # Set variables that let us use same code for retrieving params or fitted params
        if fitted:
            method_shallow = "_get_fitted_params"
            method_public = "get_fitted_params"
            deepkw = {}
        else:
            method_shallow = "get_params"
            method_public = "get_params"
            deepkw = {"deep": deep}

        # Get the direct params/fitted params
        out = getattr(super(), method_shallow)(**deepkw)

        if deep and hasattr(self, attr):
            named_objects = getattr(self, attr)
            named_objects_ = [
                (x[0], x[1])
                for x in self._coerce_to_named_object_tuples(
                    named_objects, make_unique=False
                )
            ]
            out.update(named_objects_)
            for name, obj in named_objects_:
                # checks estimator has the method we want to call
                cond1 = hasattr(obj, method_public)
                # checks estimator is fitted if calling get_fitted_params
                is_fitted = hasattr(obj, "is_fitted") and obj.is_fitted
                # if we call get_params and not get_fitted_params, this is True
                cond2 = not fitted or is_fitted
                # check both conditions together
                if cond1 and cond2:
                    for key, value in getattr(obj, method_public)(**deepkw).items():
                        out["%s__%s" % (name, key)] = value
        return out

    def _set_params(self, attr: str, **params):
        """Logic for setting parameters on meta objects/estimators.

        Separates out logic for parameter setting on meta objects from public API point.

        Parameters
        ----------
        attr : str
            Name of parameter whose values should contain named objects.

        Returns
        -------
        Self
            Instance of self.
        """
        # Ensure strict ordering of parameter setting:
        # 1. All steps
        if attr in params:
            setattr(self, attr, params.pop(attr))
        # 2. Step replacement
        items = getattr(self, attr)
        names = []
        if items and isinstance(items, (list, tuple)):
            names = list(zip(*items))[0]
        for name in list(params.keys()):
            if "__" not in name and name in names:
                self._replace_object(attr, name, params.pop(name))
        # 3. Step parameters and other initialisation arguments
        super().set_params(**params)  # type: ignore
        return self

    def _replace_object(self, attr, name, new_val) -> None:
        """Replace an object in attribute that contains named objects.

        Replaces the object with name ``name`` in attribute ``attr`` with ``new_val``.
        ``getattr(self, attr)`` is assumed to contain a list of (str, object) tuples.

        Directly mutates the list pointed to by ``attr``, in place.

        Parameters
        ----------
        attr : str
            Name of parameter whose values should contain named objects.
        name : str
            Name of object to replace.
        new_val : Any
            New value to replace object with.

        Returns
        -------
        None
        """
        # assumes `name` is a valid object name
        new_objects = list(getattr(self, attr))
        for i, obj_tpl in enumerate(new_objects):
            object_name = obj_tpl[0]
            if object_name == name:
                new_tpl = list(obj_tpl)
                new_tpl[1] = new_val
                new_objects[i] = tuple(new_tpl)
                break
        setattr(self, attr, new_objects)

    def _check_names(self, names, make_unique=True):
        """Validate that names of named objects follow API rules.

        The names for named objects should:

        - Be unique,
        - Not be the name of one of the object's direct parameters,
        - Not contain "__" (which is reserved to denote components in get/set params).

        Parameters
        ----------
        names : list[str] | tuple[str]
            The sequence of names from named objects.
        make_unique : bool, default=True
            Whether to coerce names to unique strings if they are not.

        Returns
        -------
        list[str] | tuple[str]
            A sequence of unique string names that follow named object API rules.
        """
        if len(set(names)) != len(names):
            raise ValueError("Names provided are not unique: {0!r}".format(list(names)))
        # Get names that match direct parameter
        invalid_names = set(names).intersection(self.get_params(deep=False))
        invalid_names = invalid_names.union({name for name in names if "__" in name})
        if invalid_names:
            raise ValueError(
                "Object names conflict with constructor argument or "
                "contain '__': {0!r}".format(sorted(invalid_names))
            )
        if make_unique:
            names = make_strings_unique(names)

        return names

    def _coerce_object_tuple(self, obj, clone=False):
        """Coerce object or (str, BaseObject) tuple to (str, BaseObject) tuple.

        Used to make sure input will work with expected named object tuple API format.

        Parameters
        ----------
        objs : BaseObject or (str, BaseObject) tuple
            Assumes that this has been checked, no checks are performed.
        clone : bool, default = False.
            Whether to return clone of estimator in obj (True) or a reference (False).

        Returns
        -------
        tuple[str, BaseObject]
            Named object tuple.

            - If `obj` was an object then returns (obj.__class__.__name__, obj).
            - If `obj` was already a (name, object) tuple it is returned (a copy
              is returned if ``clone=True``).
        """
        if isinstance(obj, tuple) and len(obj) >= 2:
            _obj = obj[1]
            name = obj[0]

        else:
            if isinstance(obj, tuple) and len(obj) == 1:
                _obj = obj[0]
            else:
                _obj = obj
            name = type(_obj).__name__

        if clone:
            _obj = _obj.clone()
        return (name, _obj)

    def _check_objects(
        self,
        objs,
        attr_name="steps",
        cls_type=None,
        allow_dict=False,
        allow_mix=True,
        allow_empty=False,
        clone=True,
    ):
        """Check that objects is a list of objects or sequence of named objects.

        Parameters
        ----------
        objs : Any
            Should be list of objects, a list of (str, object) tuples or a
            dict[str, objects]. Any objects should `cls_type` class.
        attr_name : str, default="steps"
            Name of checked attribute in error messages.
        cls_type : class or tuple of classes, default=BaseEstimator.
            class(es) that all objects are checked to be an instance of.
        allow_dict : bool, default=False
            Whether ``objs`` can be a dictionary mapping str names to objects.
        allow_mix : bool, default=True
            Whether mix of objects and (str, objects) is allowed in ``objs``.
        allow_empty : bool, default=False
            Whether ``objs`` can be empty.
        clone : bool, default=True
            Whether objects or named objects in ``objs`` are returned as clones
            (True) or references (False).

        Returns
        -------
        list[tuple[str, BaseObject]]
            List of tuples following named object API.

            - If `objs` was already a list of (str, object) tuples then either the
              same named objects (as with other cases cloned versions are
              returned if ``clone=True``).
            - If `objs` was a dict[str, object] then the named objects are unpacked
              into a list of (str, object) tuples.
            - If `objs` was a list of objects then string names were generated based
               on the object's class names (with coercion to unique strings if
               necessary).

        Raises
        ------
        TypeError
            If `objs` is not a list of (str, object) tuples or a dict[str, objects].
            Also raised if objects in `objs` are not instances of `cls_type`
            or `cls_type is not None, a class or tuple of classes.
        """
        msg = (
            f"Invalid {attr_name!r} attribute, {attr_name!r} should be a list "
            "of objects, or a list of (string, object) tuples. "
        )

        if cls_type is None:
            cls_type = BaseObject
            _class_name = "BaseObject"
        elif isclass(cls_type):
            _class_name = cls_type.__name__  # type: ignore
        elif isinstance(cls_type, tuple) and all(isclass(c) for c in cls_type):
            _class_name = _format_seq_to_str(
                [c.__name__ for c in cls_type], last_sep="or"
            )
        else:
            raise TypeError("`cls_type` must be a class or tuple of classes.")

        msg += f"All objects in {attr_name!r} must be of type {_class_name}"

        if (
            objs is None
            or (not allow_empty and len(objs) == 0)
            or not (isinstance(objs, list) or (allow_dict and isinstance(objs, dict)))
        ):
            raise TypeError(msg)

        def is_obj_is_tuple(obj):
            """Check whether obj is estimator of right type, or (str, est) tuple."""
            is_est = isinstance(obj, cls_type)
            is_tuple = is_named_object_tuple(obj, object_type=cls_type)

            return is_est, is_tuple

        # We've already guarded against objs being dict when allow_dict is False
        # So here we can just check dictionary elements
        if isinstance(objs, dict) and not all(
            isinstance(name, str) and isinstance(obj, cls_type)
            for name, obj in objs.items()
        ):
            raise TypeError(msg)

        elif not all(any(is_obj_is_tuple(x)) for x in objs):
            raise TypeError(msg)

        msg_no_mix = (
            f"Elements of {attr_name} must either all be objects, "
            f"or all (str, objects) tuples. A mix of the two is not allowed."
        )
        if not allow_mix and not all(is_obj_is_tuple(x)[0] for x in objs):
            if not all(is_obj_is_tuple(x)[1] for x in objs):
                raise TypeError(msg_no_mix)

        return self._coerce_to_named_object_tuples(objs, clone=clone, make_unique=True)

    def _get_names_and_objects(self, named_objects, make_unique=False):
        """Return lists of names and object from input that follows named object API.

        Handles input that is dictionary mapping str names of object instances or
        input that is a list of (str, object) tuples.

        Parameters
        ----------
        named_objects : list[tuple[str, object], ...], list[object], dict[str, object]
            The objects whose names should be returned.
        make_unique : bool, default=False
            Whether names should be made unique.

        Returns
        -------
        names : list[str]
            Lists of the names and objects that were input.
        objs : list[BaseObject]
            The
        """
        if isinstance(named_objects, dict):
            names, objs = zip(*named_objects.items())
        else:
            names, objs = zip(*[self._coerce_object_tuple(x) for x in named_objects])

        # Optionally make names unique
        if make_unique:
            names = make_strings_unique(names)
        return list(names), list(objs)

    def _coerce_to_named_object_tuples(self, objs, clone=False, make_unique=True):
        """Coerce sequence of objects or named objects to list of (str, obj) tuples.

        Input that is sequence of objects, list of (str, obj) tuples or
        dict[str, object] will be coerced to list of (str, obj) tuples on return.

        Parameters
        ----------
        objs : list of objects, list of (str, object tuples) or dict[str, object]
            The input should be coerced to list of (str, object) tuples. Should
            be a sequence of objects, or follow named object API.
        clone : bool, default=False.
            Whether objects in the returned list of (str, object) tuples are
            cloned (True) or references (False).
        make_unique : bool, default=True
            Whether the str names in the returned list of (str, object) tuples
            should be coerced to unique str values (if str names in input
            are already unique they will not be changed).

        Returns
        -------
        list[tuple[str, BaseObject]]
            List of tuples following named object API.

            - If `objs` was already a list of (str, object) tuples then either the
              same named objects (as with other cases cloned versions are
              returned if ``clone=True``).
            - If `objs` was a dict[str, object] then the named objects are unpacked
              into a list of (str, object) tuples.
            - If `objs` was a list of objects then string names were generated based
               on the object's class names (with coercion to unique strings if
               necessary).
        """
        if isinstance(objs, dict):
            named_objects = [(k, v) for k, v in objs.items()]
        else:
            # Otherwise get named object format
            named_objects = [
                self._coerce_object_tuple(obj, clone=clone) for obj in objs
            ]
        if make_unique:
            # Unpack names and objects while making names unique
            names, objs = self._get_names_and_objects(
                named_objects, make_unique=make_unique
            )
            # Repack the objects
            named_objects = list(zip(names, objs))
        return named_objects

    def _dunder_concat(
        self,
        other,
        base_class,
        composite_class,
        attr_name="steps",
        concat_order="left",
        composite_params=None,
    ):
        """Logic to concatenate pipelines for dunder parsing.

        This is useful in concrete heterogeneous meta-objects that implement
        dunders for easy concatenation of pipeline-like composites.

        Parameters
        ----------
        other : BaseObject subclass
            An object inheriting from `composite_class` or `base_class`, otherwise
            `NotImplemented` is returned.
        base_class : BaseObject subclass
            Class assumed as base class for self and `other`. ,
            and estimator components of composite_class, in case of concatenation
        composite_class : BaseMetaObject or BaseMetaEstimator subclass
            Class that has parameter `attr_name` stored in attribute of same name
            that contains list of base_class objects, list of (str, base_class)
            tuples, or a mixture thereof.
        attr_name : str, default="steps"
            Name of the attribute that contains base_class objects,
            list of (str, base_class) tuples. Concatenation is done for this attribute.
        concat_order : {"left", "right"}, default="left"
            Specifies ordering for concatenation.

            - If "left", resulting attr_name will be like
              self.attr_name + other.attr_name.
            - If "right", resulting attr_name will be like
              other.attr_name + self.attr_name.

        composite_params : dict, default=None
            Parameters of the composite are always set accordingly
            i.e., contains key-value pairs, and composite_class has key set to value.

        Returns
        -------
        BaseMetaObject or BaseMetaEstimator
            Instance of `composite_class`, where `attr_name` is set so that self and
            other are "concatenated".

            - If other is instance of `composite_class` then instance of
              `composite_class`, where `attr_name` is a concatenation of
              ``self.attr_name`` and ``other.attr_name``.
            - If `other` is instance of `base_class`, then instance of `composite_class`
              is returned where `attr_name` is set so that so that
              composite_class(attr_name=other) is returned.
            - If str are all the class names of est, list of est only is used instead
        """
        # Validate input
        if concat_order not in ["left", "right"]:
            raise ValueError(
                f"`concat_order` must be 'left' or 'right', but found {concat_order!r}."
            )
        if not isinstance(attr_name, str):
            raise TypeError(f"`attr_name` must be str, but found {type(attr_name)}.")
        if not isclass(composite_class):
            raise TypeError("`composite_class` must be a class.")
        if not isclass(base_class):
            raise TypeError("`base_class` must be a class.")
        if not issubclass(composite_class, base_class):
            raise ValueError("`composite_class` must be a subclass of base_class.")
        if not isinstance(self, composite_class):
            raise TypeError("self must be an instance of `composite_class`.")

        def concat(x, y):
            if concat_order == "left":
                return x + y
            else:
                return y + x

        # get attr_name from self and other
        # can be list of ests, list of (str, est) tuples, or list of mixture of these
        self_attr = getattr(self, attr_name)

        # from that, obtain ests, and original names (may be non-unique)
        # we avoid _make_strings_unique call too early to avoid blow-up of string
        self_names, self_objs = self._get_names_and_objects(self_attr)
        if isinstance(other, composite_class):
            other_attr = getattr(other, attr_name)
            other_names, other_objs = other._get_names_and_objects(other_attr)
        elif isinstance(other, base_class):
            other_names = [type(other).__name__]
            other_objs = [other]
        elif is_named_object_tuple(other, object_type=base_class):
            other_names = [other[0]]
            other_objs = [other[1]]
        else:
            return NotImplemented

        new_names = concat(self_names, other_names)
        new_objs = concat(self_objs, other_objs)
        # create the "steps" param for the composite
        # if all the names are equal to class names, we eat them away
        if all(type(x[1]).__name__ == x[0] for x in zip(new_names, new_objs)):
            step_param = {attr_name: list(new_objs)}
        else:
            step_param = {attr_name: list(zip(new_names, new_objs))}

        # retrieve other parameters, from composite_params attribute
        if composite_params is None:
            composite_params = {}
        else:
            composite_params = composite_params.copy()

        # construct the composite with both step and additional params
        composite_params.update(step_param)
        return composite_class(**composite_params)

    def _sk_visual_block_(self):
        """Logic to help render meta estimator as visual HTML block."""
        # Use tag interface that will be available when mixin is used
        named_object_attr_name = self.get_tag("named_object_parameters")  # type: ignore
        named_object_attr = getattr(self, named_object_attr_name)
        named_objects = self._coerce_to_named_object_tuples(named_object_attr)
        _, objs = self._get_names_and_objects(named_objects)

        def _get_name(name, obj):
            if obj is None or obj == "passthrough":
                return f"{name}: passthrough"
            # Is an estimator
            return f"{name}: {obj.__class__.__name__}"

        names = [_get_name(name, est) for name, est in named_objects]
        name_details = [str(obj) for obj in objs]
        return _VisualBlock(
            "serial",
            objs,
            names=names,
            name_details=name_details,
            dash_wrapped=False,
        )


class _MetaTagLogicMixin:
    """Mixin for tag conjunction, disjunction, chain operations for meta-objects.

    Contains methods to set tags of a meta-object dependent on component objects.
    """

    def _anytagis(self, tag_name, value, estimators):
        """Return whether any estimator in list has tag `tag_name` of value `value`.

        Parameters
        ----------
        tag_name : str, name of the tag to check
        value : value of the tag to check for
        estimators : list of (str, estimator) pairs to query for the tag/value

        Return
        ------
        bool : True iff at least one estimator in the list has value in tag tag_name
        """
        tagis = [est.get_tag(tag_name, value) == value for _, est in estimators]
        return any(tagis)

    def _anytagis_then_set(self, tag_name, value, value_if_not, estimators):
        """Set self's `tag_name` tag to `value` if any estimator on the list has it.

        Writes to self:
        sets the tag `tag_name` to `value` if `_anytagis(tag_name, value)` is True
            otherwise sets the tag `tag_name` to `value_if_not`

        Parameters
        ----------
        tag_name : str, name of the tag
        value : value to check and to set tag to if one of the tag values is `value`
        value_if_not : value to set in self if none of the tag values is `value`
        estimators : list of (str, estimator) pairs to query for the tag/value
        """
        if self._anytagis(tag_name=tag_name, value=value, estimators=estimators):
            self.set_tags(**{tag_name: value})
        else:
            self.set_tags(**{tag_name: value_if_not})

    def _anytag_notnone_val(self, tag_name, estimators):
        """Return first non-'None' value of tag `tag_name` in estimator list.

        Parameters
        ----------
        tag_name : str, name of the tag
        estimators : list of (str, estimator) pairs to query for the tag/value

        Return
        ------
        tag_val : first non-'None' value of tag `tag_name` in estimator list.
        """
        for _, est in estimators:
            tag_val = est.get_tag(tag_name)
            if tag_val != "None":
                return tag_val
        return tag_val

    def _anytag_notnone_set(self, tag_name, estimators):
        """Set self's `tag_name` tag to first non-'None' value in estimator list.

        Writes to self:
        tag with name tag_name, sets to _anytag_notnone_val(tag_name, estimators)

        Parameters
        ----------
        tag_name : str, name of the tag
        estimators : list of (str, estimator) pairs to query for the tag/value
        """
        tag_val = self._anytag_notnone_val(tag_name=tag_name, estimators=estimators)
        if tag_val != "None":
            self.set_tags(**{tag_name: tag_val})

    def _tagchain_is_linked(
        self,
        left_tag_name,
        mid_tag_name,
        estimators,
        left_tag_val=True,
        mid_tag_val=True,
    ):
        """Check whether all tags left of the first mid_tag/val are left_tag/val.

        Useful to check, for instance, whether all instances of estimators
            left of the first missing value imputer can deal with missing values.

        Parameters
        ----------
        left_tag_name : str, name of the left tag
        mid_tag_name : str, name of the middle tag
        estimators : list of (str, estimator) pairs to query for the tag/value
        left_tag_val : value of the left tag, optional, default=True
        mid_tag_val : value of the middle tag, optional, default=True

        Returns
        -------
        chain_is_linked : bool,
            True iff all "left" tag instances `left_tag_name` have value `left_tag_val`
            a "left" tag instance is an instance in estimators which is earlier
            than the first occurrence of `mid_tag_name` with value `mid_tag_val`
        chain_is_complete : bool,
            True iff chain_is_linked is True, and
                there is an occurrence of `mid_tag_name` with value `mid_tag_val`
        """
        for _, est in estimators:
            if est.get_tag(mid_tag_name) == mid_tag_val:
                return True, True
            if not est.get_tag(left_tag_name) == left_tag_val:
                return False, False
        return True, False

    def _tagchain_is_linked_set(
        self,
        left_tag_name,
        mid_tag_name,
        estimators,
        left_tag_val=True,
        mid_tag_val=True,
        left_tag_val_not=False,
        mid_tag_val_not=False,
    ):
        """Check if _tagchain_is_linked, then set self left_tag_name and mid_tag_name.

        Writes to self:
        tag with name left_tag_name, sets to left_tag_val if _tag_chain_is_linked[0]
            otherwise sets to left_tag_val_not
        tag with name mid_tag_name, sets to mid_tag_val if _tag_chain_is_linked[1]
            otherwise sets to mid_tag_val_not

        Parameters
        ----------
        left_tag_name : str, name of the left tag
        mid_tag_name : str, name of the middle tag
        estimators : list of (str, estimator) pairs to query for the tag/value
        left_tag_val : value of the left tag, optional, default=True
        mid_tag_val : value of the middle tag, optional, default=True
        left_tag_val_not : value to set if not linked, optional, default=False
        mid_tag_val_not : value to set if not linked, optional, default=False
        """
        linked, complete = self._tagchain_is_linked(
            left_tag_name=left_tag_name,
            mid_tag_name=mid_tag_name,
            estimators=estimators,
            left_tag_val=left_tag_val,
            mid_tag_val=mid_tag_val,
        )
        if linked:
            self.set_tags(**{left_tag_name: left_tag_val})
        else:
            self.set_tags(**{left_tag_name: left_tag_val_not})
        if complete:
            self.set_tags(**{mid_tag_name: mid_tag_val})
        else:
            self.set_tags(**{mid_tag_name: mid_tag_val_not})


class BaseMetaObject(_MetaObjectMixin, _MetaTagLogicMixin, BaseObject):
    """Parameter and tag management for objects composed of named objects.

    Allows objects to get and set nested parameters when a parameter of the the
    class has values that follow the named object specification. For example,
    in a pipeline class with the the "step" parameter accepting named objects,
    this would allow `get_params` and `set_params` to retrieve and update the
    parameters of the objects in each step.

    Note: if inheriting from an abstract descendant of `BaseObject`, use
    ``BaseMetaObjectMixin`` and not ``BaseMetaObject``.

    See Also
    --------
    BaseMetaObjectMixin :
        Mixin for inheriting from abstract descendants of ``BaseObject``.
        Same as ``BaseMetaObject``, but does not inherit from ``BaseObject``.
    BaseMetaEstimator :
        Expands on ``BaseMetaObject`` by adding functionality for getting fitted
        parameters from a class's component estimators.
    """


class BaseMetaObjectMixin(_MetaObjectMixin, _MetaTagLogicMixin):
    """Parameter and tag management for objects composed of named objects.

    Allows objects to get and set nested parameters when a parameter of the the
    class has values that follow the named object specification. For example,
    in a pipeline class with the the "step" parameter accepting named objects,
    this would allow `get_params` and `set_params` to retrieve and update the
    parameters of the objects in each step.

    Mixin for inheriting from abstract descendants of ``BaseObject``.
    Intended use is inheriting as follows:

    ``class MyAbstractBaseClass(BaseObject)``, and then
    ``class MyConcreteClass(BaseMetaObjectMixin, MyAbstractBaseClass)``

    The mixin will override:
    ``get_params``, ``set_params``, ``_get_params``, ``_set_params``,
    ``_get_fitted_params``, ``_sk_visual_block_``

    See Also
    --------
    BaseMetaEstimatorMixin :
        Expands on ``BaseMetaObjectMixin`` by adding functionality for getting fitted
        parameters from a class's component estimators.
    BaseMetaObject :
        same as ``BaseMetaObjectMixin``, but also inherits from ``BaseObject``.
        Use for a standalone meta-object class.
        Do not use if inheriting from an abstract descendant of ``BaseObject``.
    """


class BaseMetaEstimator(_MetaObjectMixin, _MetaTagLogicMixin, BaseEstimator):
    """Parameter and tag management for estimators composed of named objects.

    Allows estimators to get and set nested parameters when a parameter of the the
    class has values that follow the named object specification. For example,
    in a pipeline class with the the "step" parameter accepting named objects,
    this would allow `get_params` and `set_params` to retrieve and update the
    parameters of the objects in each step.

    Note: if inheriting from an abstract descendant of `BaseEstimator`, use
    ``BaseMetaEstimatorMixin`` and not ``BaseMetaEstimator``.

    See Also
    --------
    BaseMetaEstimatorMixin :
        Mixin for inheriting from abstract descendants of ``BaseObject``.
        Same as ``BaseMetaObject``, but does not inherit from ``BaseObject``.
    BaseMetaObject :
        Provides similar functionality to  `BaseMetaEstimator`,
        but does not have the estimator interface for fitting and fitted parameters.
    """


class BaseMetaEstimatorMixin(_MetaObjectMixin, _MetaTagLogicMixin):
    """Parameter and tag management for estimators composed of named objects.

    Allows estimators to get and set nested parameters when a parameter of the the
    class has values that follow the named object specification. For example,
    in a pipeline class with the the "step" parameter accepting named objects,
    this would allow `get_params` and `set_params` to retrieve and update the
    parameters of the objects in each step.

    Mixin for inheriting from abstract descendants of ``BaseEstimator``.
    Intended use is inheriting as follows:

    ``class MyAbstractBaseClass(BaseEstimator)``, and then
    ``class MyConcreteClass(BaseMetaEstimatorMixin, MyAbstractBaseClass)``

    Note: the order of inheritance is important.

    The mixin will override:
    ``get_params``, ``set_params``, ``_get_params``, ``_set_params``,
    ``_get_fitted_params``, ``_sk_visual_block_``

    See Also
    --------
    BaseMetaObjectMixin :
        Provides similar functionality to  `BaseMetaEstimatorMixin`,
        but does not have the estimator interface for fitting and fitted parameters.
    BaseMetaEstimator :
        same as ``BaseMetaEstimatorMixin``, but also inherits from ``BaseEstimator``.
        Use for a standalone meta-estimator class.
        Do not use if inheriting from an abstract descendant of ``BaseEstimator``.
    """
