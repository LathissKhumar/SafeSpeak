// SafeSpeak Content Script

let debounceTimer;
const API_URL = "http://127.0.0.1:8000/analyze";

// State
let lastAnalysedText = "";
let currentTooltip = null;

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
    if (!text || text.trim() === "" || text === lastAnalysedText) {
        removeTooltip();
        return;
    }

    lastAnalysedText = text;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text, user_id: 'browser_user' })
        });

        const data = await response.json();
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

    // Add logic handling
    let buttonsHtml = '';

    if (action === 'block_and_alert') {
        message += `<br><strong>Action:</strong> Message Blocked!`;
        // In real app, we might disable the button or clear input
    } else {
        if (rewrite) {
            message += `<br><em>Tip:</em> "${rewrite}"`;
            buttonsHtml += `<button id="ss-btn-rewrite" class="safespeak-btn safespeak-btn-rewrite">Use Polite Version</button>`;
        }
    }

    buttonsHtml += `<button id="ss-btn-dismiss" class="safespeak-btn safespeak-btn-dismiss">Dismiss</button>`;

    tooltip.innerHTML = `<div>${message}</div><div class="safespeak-actions">${buttonsHtml}</div>`;

    // Positioning
    tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
    tooltip.style.left = `${rect.left + window.scrollX}px`;

    document.body.appendChild(tooltip);
    currentTooltip = tooltip;

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
