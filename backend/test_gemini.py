
import os
from dotenv import load_dotenv
from rewriter import MessageRewriter

load_dotenv(override=True)

print("Testing Gemini Rewriter (Refined Prompt)...")
rewriter = MessageRewriter()

# Test cases designed to check meaning preservation
test_cases = [
    "You are stupid",
    "This idea is absolute garbage, what were you thinking?",
    "I hate you, go away."
]

for text in test_cases:
    print(f"\nOriginal: {text}")
    rewritten = rewriter.rewrite_message(text)
    print(f"Rewritten: {rewritten}")
