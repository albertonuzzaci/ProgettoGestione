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
    text = "What a wonderful accomodation! I loved staying there. Although people outside were a little bit scary, the stay was pleasant."
    results = classifier.extract(text)
    print(results)
