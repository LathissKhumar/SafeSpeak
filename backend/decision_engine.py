from datetime import datetime

# Simple in-memory storage for offences
# Key: user_id (or IP/session), Value: list of offence timestamps
# In a real app, use Redis or a Database
OFFENCE_RECORDS = {}

def decide_action(analysis_result: dict, user_id: str = "anonymous") -> dict:
    """
    Decide the action based on the analysis severity score.
    
    Rules:
      - severity < 20 → allow
      - 20–40 → warn
      - 40–70 → block_and_rewrite
      - >70 → block_and_alert
      
    Also handles escalation for repeated offences.
    """
    severity = analysis_result.get("severity", 0)
    action = "allow"
    reason = "Safe message."
    
    # 0. Handle API Errors
    if analysis_result.get("label") == "error":
        return {
            "action": "block_and_alert",
            "reason": "System Error: Unable to analyze toxicity (Check API Key)."
        }

    # 1. Base Logic
    if severity < 20:
        action = "allow"
        reason = "Message is clean."
    elif 20 <= severity < 40:
        action = "warn"
        reason = "Mild toxicity detected. User warned."
    elif 40 <= severity <= 70:
        action = "block_and_rewrite"
        reason = "Toxic content detected. Message blocked and rewrite suggested."
    else: # > 70
        action = "block_and_alert"
        reason = "Severe toxicity detected. Message blocked and admin alerted."

    # 2. Escalation Logic (if toxic)
    if severity >= 40:
        register_offence(user_id)
        offence_count = get_offence_count(user_id)
        
        if offence_count > 3 and action == "block_and_rewrite":
             action = "block_and_alert"
             reason += " (Escalated due to repeated offences)"
    
    return {
        "action": action,
        "reason": reason
    }

def register_offence(user_id: str):
    """Log an offence for a user."""
    if user_id not in OFFENCE_RECORDS:
        OFFENCE_RECORDS[user_id] = []
    OFFENCE_RECORDS[user_id].append(datetime.now())

def get_offence_count(user_id: str) -> int:
    """Get number of offences."""
    return len(OFFENCE_RECORDS.get(user_id, []))
