from transformers import T5Tokenizer, T5ForConditionalGeneration

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter with google/flan-t5-base.
        """
        print("Loading Rewriter Model (google/flan-t5-base)...")
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
        print("Rewriter Model Loaded.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text to be polite and child-safe.
        """
        if not text or not text.strip():
            return ""

        # Construct the prompt as per requirements
        input_text = f"Rewrite this politely for a child: {text}"
        
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids
        
        # Generate the rewritten text
        outputs = self.model.generate(
            input_ids, 
            max_length=128, 
            num_beams=5, 
            early_stopping=True
        )
        
        rewritten_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return rewritten_text
