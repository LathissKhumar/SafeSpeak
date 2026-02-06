window.SafeSpeak = window.SafeSpeak || {};

window.SafeSpeak.TooltipManager = class TooltipManager {
    constructor() {
        this.currentTooltip = null;
    }

    show(target, reason, action, rewrite, onRewrite, onDismiss, position) {
        this.remove(); // Clear existing

        const tooltip = document.createElement('div');
        tooltip.className = 'safespeak-overlay visible';

        // Styling classes
        let severityClass = 'safespeak-mild';
        if (action === 'block_and_alert') severityClass = 'safespeak-severe';
        else if (action === 'block_and_rewrite') severityClass = 'safespeak-toxic';

        tooltip.classList.add(severityClass);

        let message = `<strong>SafeSpeak:</strong> ${reason}`;

        if (action === 'block_and_alert' || action === 'block_and_rewrite') {
            message += `<br><strong>Action:</strong> Message Cleared & Blocked.`;
        }

        let buttonsHtml = '';
        if (rewrite) {
            message += `<br><em>Suggestion:</em> "${rewrite}"`;
            buttonsHtml += `<button id="ss-btn-rewrite" class="safespeak-btn safespeak-btn-rewrite">Paste Polite Version</button>`;
        }
        buttonsHtml += `<button id="ss-btn-dismiss" class="safespeak-btn safespeak-btn-dismiss">Dismiss</button>`;

        tooltip.innerHTML = `<div>${message}</div><div class="safespeak-actions">${buttonsHtml}</div>`;

        // Position
        tooltip.style.top = `${position.top}px`;
        tooltip.style.left = `${position.left}px`;
        tooltip.classList.add('safespeak-above');

        document.body.appendChild(tooltip);
        this.currentTooltip = tooltip;

        // Events
        const btnRewrite = document.getElementById('ss-btn-rewrite');
        if (btnRewrite) {
            btnRewrite.addEventListener('click', (e) => {
                e.preventDefault();
                onRewrite();
                this.remove();
            });
        }

        const btnDismiss = document.getElementById('ss-btn-dismiss');
        if (btnDismiss) btnDismiss.addEventListener('click', (e) => {
            e.preventDefault();
            onDismiss();
            this.remove();
        });
    }

    remove() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }
};
