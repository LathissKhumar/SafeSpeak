window.SafeSpeak = window.SafeSpeak || {};

window.SafeSpeak.WhatsAppAdapter = class WhatsAppAdapter extends window.SafeSpeak.BaseAdapter {
    static matches(url) {
        return url.includes('web.whatsapp.com') || url.includes('whatsapp.com');
    }

    start(onInputCallback) {
        console.log("SafeSpeak: Starting WhatsApp Adapter");
        const debouncedInput = this.debounce((target) => {
            onInputCallback(target);
        }, 800);

        // WhatsApp uses a MutationObserver or efficient event handling
        // But Input event usually works on the contenteditable div
        document.addEventListener('input', (e) => {
            const target = e.target;
            // WhatsApp input is a contenteditable div with specific classes, often has role="textbox" or similar
            if (target.isContentEditable) {
                debouncedInput(target);
            }
        }, true);
    }

    getText(target) {
        // WhatsApp puts text in spans. innerText is usually safe.
        // We might need to handle emojis or specific formatting.
        return target.innerText;
    }

    setText(target, text) {
        console.log("SafeSpeak: WhatsApp Adapter setting text");
        target.focus();

        // WhatsApp requires execCommand to trigger its internal state updates
        // Select all text first
        document.execCommand('selectAll', false, null);

        if (text === "") {
            document.execCommand('delete', false, null);
        } else {
            // Insert replacement
            document.execCommand('insertText', false, text);
        }
    }

    getTooltipPosition(target) {
        // WhatsApp input bar is at the bottom, we want tooltip strictly above it.
        const rect = target.getBoundingClientRect();
        // The input container in WA usually has a specific wrapper, but rect.top is a safe bet.
        return {
            top: rect.top - 15,
            left: rect.left
        };
    }
};
