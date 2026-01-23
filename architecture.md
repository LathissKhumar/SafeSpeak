# SafeSpeak System Architecture

## Overview
SafeSpeak is an end-to-end AI safety system designed to detect and mitigate toxic communication in real-time. It moves beyond simple keyword filtering by using large language models (Transformers) to understand context, severity, and intent.

## Data Flow

1.  **User Input Interaction**
    *   User types in a browser input field (e.g., chat box, comment section).
    *   **Chrome Extension (`content.js`)** detects the "stop typing" event (debounced) or form submission.
    *   Input text is extracted and sent to the Backend API.

2.  **Analysis Phase (Backend)**
    *   **FastAPI (`main.py`)** receives the text.
    *   **Toxicity Analyzer (`analyzer.py`)** processes the text using **Hugging Face Inference API** (`s-nlp/roberta_toxicity_classifier`).
        *   The backend sends a request to HF's servers for low-latency analysis.
        *   A **Severity Score (0-100)** is calculated based on returned confidence scores.
    *   The analyzer returns a JSON object with label, severity, confidence, and explanation.

3.  **Decision Phase**
    *   **Decision Engine (`decision_engine.py`)** evaluates the analysis result against safety rules: 
        *   **0-19**: Allow.
        *   **20-39**: Warn.
        *   **40-70**: Block & Rewrite.
        *   **>70**: Block & Alert.
    *   **Escalation Logic**: Checks an in-memory `OFFENCE_RECORDS` counter. If a user repeatedly triggers blocking, the action escalates to "Block & Alert".

4.  **Intervention Phase**
    *   If the action is `warn` or `block_and_rewrite`, the **Rewriter (`rewriter.py`)** is triggered.
    *   It calls the **Hugging Face Inference API** using `google/flan-t5-large` to generate a polite, child-safe alternative.
    *   The backend responds to the extension with the Action, Reason, and Rewrite suggestion.

5.  **User Feedback (Frontend)**
    *   The **Extension** receives the decision.
    *   If `action != allow`, a UI Overlay (visual indicator) appears near the input field:
        *   **Yellow/Orange/Red** based on severity.
        *   Displays the reason and the rewritten suggestion.
    *   User can choose to "Dismiss" or "Use Polite Version" (which replaces their text).

## Why AI > Keyword Filters?
*   **Context Awareness**: "I will kill you" (Threat) vs "I killed it at the game" (Positive). Keyword filters fail here; SafeSpeak's Transformer models understand the difference.
*   **Constructive Correction**: Instead of just saying "No", SafeSpeak teaches children *how* to rephrase politely using the rewriting module.
*   **Adaptability**: The models (RoBERTa/T5) are pre-trained on vast datasets, recognizing slang, subtle insults, and evolving toxicity patterns.

## Ethical & Privacy Considerations
*   **Privacy**: Analysis is stateless (unless logging is enabled for escalation). No data needs to be stored permanently.
*   **Bias**: We use standard open-source models. Future work involves fine-tuning on child-specific datasets to reduce bias against protected groups.
*   **Child Safety First**: The "Block & Alert" mechanism ensures that high-risk threats are stopped immediately.

## Deployment
*   **Backend**: Configured with `Procfile` for native deployment on platforms like Render, Railway, or Heroku.
*   **Environment Variables**:
    *   `HF_API_KEY`: Required for Hugging Face Inference API.
*   **Frontend**: Distributed as a standard Chrome Extension (Manifest V3), adhering to modern browser security standards.
