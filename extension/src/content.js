// SafeSpeak Main Entry Point

(function () {
    console.log("SafeSpeak: Initializing...");

    // Configuration
    const API_URL = "http://localhost:10000/analyze";

    // Dependencies
    const TooltipManager = new window.SafeSpeak.TooltipManager();
    let currentAdapter = null;
    let justBlocked = false;
    let lastAnalysedText = "";

    // Adapter Selection
    const url = window.location.href;
    if (window.SafeSpeak.WhatsAppAdapter.matches(url)) {
        currentAdapter = new window.SafeSpeak.WhatsAppAdapter();
    } else {
        currentAdapter = new window.SafeSpeak.DefaultAdapter();
    }

    // Start Adapter
    currentAdapter.start(handleInput);

    async function handleInput(target) {
        const text = currentAdapter.getText(target);

        if (!text || text.trim() === "") {
            if (justBlocked) {
                justBlocked = false;
                lastAnalysedText = "";
                return;
            }
            TooltipManager.remove();
            return;
        }

        if (text === lastAnalysedText) return;
        lastAnalysedText = text;

        try {
            console.log("SafeSpeak: Analyzing...", text);
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, user_id: 'browser_user' })
            });

            const data = await response.json();
            handleDecision(target, data);
        } catch (error) {
            console.error("SafeSpeak Error:", error);
        }
    }

    function handleDecision(target, data) {
        const { action, analysis, rewrite, reason } = data;

        TooltipManager.remove();

        if (action === 'allow') return;

        if (action === 'block_and_alert' || action === 'block_and_rewrite') {
            justBlocked = true;
            currentAdapter.setText(target, ""); // Clear text
        }

        const position = currentAdapter.getTooltipPosition(target);
        TooltipManager.show(
            target,
            reason,
            action,
            rewrite,
            () => { // onRewrite
                if (rewrite) currentAdapter.setText(target, rewrite);
            },
            () => { }, // onDismiss
            position
        );
    }
})();
