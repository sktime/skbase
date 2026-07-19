function skbaseCopyToClipboard(text, element) {
    const toggleableContent = element.closest('.sk-toggleable__content');
    const paramPrefix = toggleableContent ? toggleableContent.dataset.paramPrefix : '';
    const fullParamName = paramPrefix ? `${paramPrefix}${text}` : text;
    const originalHTML = element.innerHTML.replace('Copied!', '').replace('Failed!', '');
    const originalWidth = window.getComputedStyle(element).width;
    const restore = () => {
        element.innerHTML = originalHTML;
        element.style.width = '';
        element.style.color = '';
    };
    const markCopied = () => {
        element.style.width = originalWidth;
        element.style.color = 'green';
        element.innerHTML = 'Copied!';
        setTimeout(restore, 2000);
    };
    const markFailed = () => {
        element.style.color = 'red';
        element.innerHTML = 'Failed!';
        setTimeout(restore, 2000);
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(fullParamName).then(markCopied).catch(markFailed);
    } else {
        const textArea = document.createElement('textarea');
        textArea.value = fullParamName;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy') ? markCopied() : markFailed();
        } catch (error) {
            markFailed();
        } finally {
            document.body.removeChild(textArea);
        }
    }
    return false;
}

function skbaseDetectTheme(element) {
    const body = document.querySelector('body');

    if (body !== null) {
        const themeKindAttr = body.getAttribute('data-vscode-theme-kind');
        const themeNameAttr = body.getAttribute('data-vscode-theme-name');

        if (themeKindAttr && themeNameAttr) {
            const themeKind = themeKindAttr.toLowerCase();
            const themeName = themeNameAttr.toLowerCase();

            if (themeKind.includes('dark') || themeName.includes('dark')) {
                return 'dark';
            }
            if (themeKind.includes('light') || themeName.includes('light')) {
                return 'light';
            }
        }

        if (body.getAttribute('data-jp-theme-light') === 'false') {
            return 'dark';
        }
        if (body.getAttribute('data-jp-theme-light') === 'true') {
            return 'light';
        }
    }

    const color = window.getComputedStyle(element.parentNode, null).getPropertyValue('color');
    const match = color.match(/^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*$/i);
    if (match) {
        const red = parseFloat(match[1]);
        const green = parseFloat(match[2]);
        const blue = parseFloat(match[3]);
        const luma = 0.299 * red + 0.587 * green + 0.114 * blue;

        if (luma > 180) {
            return 'dark';
        }
        if (luma < 75) {
            return 'light';
        }
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function skbaseForceTheme(elementId) {
    const estimatorElement = document.getElementById(elementId);
    if (estimatorElement !== null) {
        estimatorElement.classList.add(skbaseDetectTheme(estimatorElement));
    }

    document.querySelectorAll(`#${elementId} .copy-paste-icon`).forEach(function (element) {
        const toggleableContent = element.closest('.sk-toggleable__content');
        const paramPrefix = toggleableContent ? toggleableContent.dataset.paramPrefix : '';
        const paramCell = element.parentElement.nextElementSibling;
        const paramName = paramCell ? paramCell.textContent.trim().split(' ')[0] : '';
        const fullParamName = paramPrefix ? `${paramPrefix}${paramName}` : paramName;
        element.setAttribute('title', fullParamName);
    });
}
