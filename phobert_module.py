from transformers import pipeline

class PhoBERTModule:
    def __init__(self, model_name="wonrax/phobert-base-vietnamese-sentiment"):
        self.pipe = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)

    def analyze_sentiment(self, text):
        """Analyze sentiment using PhoBERT"""
        result = self.pipe(text)[0]
        label = result['label']
        confidence = result['score']
        # Map labels to POSITIVE, NEUTRAL, NEGATIVE
        if label == 'POS':
            sentiment = 'POSITIVE'
        elif label == 'NEG':
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'
        return sentiment, confidence