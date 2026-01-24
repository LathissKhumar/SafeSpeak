// SafeSpeak Content Script

let debounceTimer;
const API_URL = "https://safespeak-zoec.onrender.com/analyze";

// State
let lastAnalysedText = "";
let currentTooltip = null;
let justBlocked = false; // Flag to prevent tooltip cleanup on auto-clear

// Listen for input events
document.addEventListener('input', (event) => {
    const target = event.target;

    // Only target text areas or inputs
    if (target.tagName !== 'TEXTAREA' && target.tagName !== 'INPUT' && !target.isContentEditable) {
        return;
    }

    // Debounce analysis
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        analyzeInput(target);
    }, 800); // Wait 800ms after typing stops
}, true);

async function analyzeInput(target) {
    const text = getTextFromTarget(target);

    // Check if empty
    if (!text || text.trim() === "") {
        // If we just blocked it, consume the flag and DO NOT remove tooltip
        if (justBlocked) {
            justBlocked = false;
            lastAnalysedText = ""; // Reset history so re-typing same thing works
            return;
        }
        removeTooltip();
        return;
    }

    if (text === lastAnalysedText) {
        return;
    }

    lastAnalysedText = text;

    try {
        console.log("SafeSpeak: Analyzing text...", text);
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text, user_id: 'browser_user' })
        });

        const data = await response.json();
        console.log("SafeSpeak: API Response", data);
        handleDecision(target, data);

    } catch (error) {
        console.error("SafeSpeak Error:", error);
    }
}

function getTextFromTarget(target) {
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
        return target.value;
    } else if (target.isContentEditable) {
        return target.innerText;
    }
    return "";
}

function setTextToTarget(target, newText) {
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
        target.value = newText;
    } else if (target.isContentEditable) {
        target.innerText = newText;
    }
    // Trigger input event to notify site scripts (like React/Vue handlers)
    target.dispatchEvent(new Event('input', { bubbles: true }));
}

function handleDecision(target, data) {
    const action = data.action;
    const analysis = data.analysis;
    const severity = analysis.severity;
    const rewrite = data.rewrite;

    removeTooltip();

    if (action === 'allow') {
        return;
    }

    // BLOCKING LOGIC: Clear the input if it's severe
    if (action === 'block_and_alert' || action === 'block_and_rewrite') {
        justBlocked = true; // Prevent immediate cleanup
        setTextToTarget(target, ""); // Clear the toxic message immediately
    }

    // Create tooltip
    showTooltip(target, action, severity, rewrite, data.reason);
}

function showTooltip(target, action, severity, rewrite, reason) {
    const rect = target.getBoundingClientRect();

    const tooltip = document.createElement('div');
    tooltip.className = 'safespeak-overlay visible';

    let severityClass = 'safespeak-mild';
    if (severity > 70) severityClass = 'safespeak-severe';
    else if (severity > 40) severityClass = 'safespeak-toxic';

    tooltip.classList.add(severityClass);

    let message = `<strong>SafeSpeak Alert:</strong> ${reason}`;
    let buttonsHtml = '';

    // If blocked, we state it clearly
    if (action === 'block_and_alert' || action === 'block_and_rewrite') {
        message += `<br><strong>Action:</strong> Message Cleared & Blocked.`;
    }

    // Always offer rewrite if available, even if blocked
    if (rewrite) {
        message += `<br><em>Suggestion:</em> "${rewrite}"`;
        buttonsHtml += `<button id="ss-btn-rewrite" class="safespeak-btn safespeak-btn-rewrite">Paste Polite Version</button>`;
    }

    buttonsHtml += `<button id="ss-btn-dismiss" class="safespeak-btn safespeak-btn-dismiss">Dismiss</button>`;

    tooltip.innerHTML = `<div>${message}</div><div class="safespeak-actions">${buttonsHtml}</div>`;

    // Positioning: Fixed relative to viewport
    // rect.top is the top edge of the input box.
    // We subtract 15px to give it a gap.
    // CSS translateY(-100%) moves it up by its own height.
    // Result: The bottom of the tooltip is 15px above the input.
    tooltip.style.top = `${rect.top - 15}px`;
    tooltip.style.left = `${rect.left}px`;

    // Add a class for "above" styling
    tooltip.classList.add('safespeak-above');

    document.body.appendChild(tooltip);
    currentTooltip = tooltip;
    console.log("SafeSpeak: Tooltip appended to body at", tooltip.style.top, tooltip.style.left);

    // Event Listeners
    const btnRewrite = document.getElementById('ss-btn-rewrite');
    if (btnRewrite) {
        btnRewrite.addEventListener('click', (e) => {
            e.preventDefault();
            setTextToTarget(target, rewrite);
            removeTooltip();
        });
    }

    const btnDismiss = document.getElementById('ss-btn-dismiss');
    if (btnDismiss) {
        btnDismiss.addEventListener('click', (e) => {
            e.preventDefault();
            removeTooltip();
        });
    }
}

function removeTooltip() {
    if (currentTooltip) {
        currentTooltip.remove();
        currentTooltip = null;
    }
}
