from datetime import datetime
from typing import Dict, List
from app.schemas.analysis import AnalysisResult, AnalysisResponse
from app.core.logging import logger

class DecisionService:
    def __init__(self):
        # In-memory storage. Replace with Redis/DB in production.
        self._offence_records: Dict[str, List[datetime]] = {}
        logger.info("DecisionService initialized.")

    def decide(self, analysis: AnalysisResult, user_id: str = "anonymous") -> tuple[str, str]:
        """
        Returns (action, reason) based on analysis severity.
        """
        severity = analysis.severity
        action = "allow"
        reason = "Safe message."

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
            self._register_offence(user_id)
            offence_count = self._get_offence_count(user_id)
            
            if offence_count > 3 and action == "block_and_rewrite":
                action = "block_and_alert"
                reason += " (Escalated due to repeated offences)"
        
        return action, reason

    def _register_offence(self, user_id: str):
        if user_id not in self._offence_records:
            self._offence_records[user_id] = []
        self._offence_records[user_id].append(datetime.now())

    def _get_offence_count(self, user_id: str) -> int:
        return len(self._offence_records.get(user_id, []))
