window.SafeSpeak = window.SafeSpeak || {};

window.SafeSpeak.DefaultAdapter = class DefaultAdapter extends window.SafeSpeak.BaseAdapter {
    static matches(url) {
        return true;
    }

    start(onInputCallback) {
        console.log("SafeSpeak: Starting Default Adapter");
        const debouncedInput = this.debounce((target) => {
            onInputCallback(target);
        }, 800);

        document.addEventListener('input', (e) => {
            const target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
                debouncedInput(target);
            }
        }, true);
    }

    getText(target) {
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
            return target.value;
        } else if (target.isContentEditable) {
            return target.innerText;
        }
        return "";
    }

    setText(target, text) {
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
            const proto = Object.getPrototypeOf(target);
            const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;

            if (setter) {
                setter.call(target, text);
            } else {
                target.value = text;
            }

            target.dispatchEvent(new Event('input', { bubbles: true }));
            target.dispatchEvent(new Event('change', { bubbles: true }));
        } else if (target.isContentEditable) {
            target.focus();
            target.innerText = text;
            target.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
};
