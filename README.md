# SafeSpeak – AI Guardian for Children’s Online Communication

## Project Overview
SafeSpeak is an AI-powered system designed to detect cyberbullying and toxic language in real-time. It protects children by:
1.  **Detecting** toxic content (insults, threats, severe toxicity) using RoBERTa.
2.  **Scoring** the severity (0-100).
3.  **Intervening** with actions like Warn, Block, or Alert.
4.  **Rewriting** toxic messages into polite alternatives using Google Flan-T5.

## Architecture
The system consists of:
*   **Backend**: FastAPI + PyTorch + Transformers (RoBERTa & T5).
*   **Frontend**: Chrome Extension for real-time browser protection.
*   **Deployment**: Cloud-ready via Procfile.

For detailed design, see [safespeak/architecture.md](safespeak/architecture.md).

## Project Structure
```
safespeak/
├── backend/
│   ├── analyzer.py          # Toxicity detection (RoBERTa)
│   ├── decision_engine.py   # Rules & Escalation logic
│   ├── rewriter.py          # Message rewriting (Flan-T5)
│   ├── main.py              # FastAPI application
│   ├── Procfile             # Deployment configuration
│   └── requirements.txt
├── extension/
│   ├── manifest.json
│   ├── content.js           # DOM Interception script
│   ├── popup.html           # Extension UI
│   ├── popup.js
│   └── styles.css
└── architecture.md          # Implementation details
```

## Setup & Running

### Option 1: Deploy to Cloud (Render/Railway/Heroku)
This project is configured for cloud deployment using a `Procfile`.
1.  **Push to GitHub**.
2.  **Connect to Render/Railway**.
3.  **Root Directory**: Set the "Root Directory" in your deployment settings to `safespeak/backend`.
4.  **Build Command**: `pip install -r requirements.txt`
5.  **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT` (or let the platform detect the Procfile).

### Option 2: Run Locally (Python)
1.  **Navigate to backend**:
    ```bash
    cd safespeak/backend
    ```
2.  **Create virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start server**:
    ```bash
    uvicorn main:app --reload
    ```

## Installing the Chrome Extension
1.  Open Chrome and go to `chrome://extensions/`.
2.  Enable **Developer mode** (top right toggle).
3.  Click **Load unpacked**.
4.  Select the `safespeak/extension` folder.
5.  The extension is now active! Open any website with a text input (e.g., a forum or chat demo) and type something toxic to test.

## Usage Example (API)
**POST** `/analyze`
```json
{
  "message": "You are stupid and ugly!",
  "user_id": "test_user_1"
}
```

**Response**:
```json
{
  "analysis": {
    "label": "toxic",
    "severity": 95,
    "confidence": 0.98,
    "explanation": "Message contains toxic content."
  },
  "action": "block_and_alert",
  "reason": "Severe toxicity detected. Message blocked and admin alerted.",
  "rewrite": "You are not being very nice.",
  "timestamp": "2023-10-27T10:00:00"
}
```

## Features
*   **Real-time Analysis**: Instant feedback as you type.
*   **Ethical AI**: Prioritizes education via rewriting over simple censorship.
*   **Escalation**: Detects repeat offenders and increases severity of action.
*   **Child Safe**: Specifically tuned to generate polite, child-friendly language.
