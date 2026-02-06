window.SafeSpeak = window.SafeSpeak || {};

window.SafeSpeak.BaseAdapter = class BaseAdapter {
    constructor() {
        if (this.constructor === window.SafeSpeak.BaseAdapter) {
            throw new Error("Abstract classes can't be instantiated.");
        }
    }

    static matches(url) {
        throw new Error("Method 'matches' must be implemented.");
    }

    start() {
        throw new Error("Method 'start' must be implemented.");
    }

    getText(target) {
        throw new Error("Method 'getText' must be implemented.");
    }

    setText(target, text) {
        throw new Error("Method 'setText' must be implemented.");
    }

    getTooltipPosition(target) {
        const rect = target.getBoundingClientRect();
        return {
            top: rect.top - 15,
            left: rect.left
        };
    }

    // Helper to debounce calls
    debounce(func, wait) {
        let timeout;
        return function (...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
};
