from transformers import RobertaTokenizer, AutoModelForSequenceClassification, pipeline


class ExtractEmotions:

    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")

    def extract(self, text):
        self.create_pipeline()
        return self.emotions(text)
    
    def create_pipeline(self):
        self.emotions = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-classification",
            top_k=7,
            max_length=512, 
            truncation=True
        )

if __name__ == "__main__":
    classifier = ExtractEmotions()
    text = "We had a great (3-week) stay. The house is exactly as presented in the photos, and is in an excellent location - the road itself is very quiet, but is just around the corner from the increasingly buzzing action of Parson's Green. Camilla was a great host - very quick to reply to any messages, and she made checking in and checking out extremely easy. Would definitely stay here again."
    results = classifier.extract(text)
    print(results)