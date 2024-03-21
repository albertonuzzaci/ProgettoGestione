from transformers import RobertaTokenizer, AutoModelForSequenceClassification, pipeline


class ExtractEmotions:

    def __init__(self, model_name='original'):
        self.tokenizer = RobertaTokenizer.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")


    def create_pipeline(self):
        self.goemotions = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-classification",
            top_k=7,
            function_to_apply='sigmoid',
            max_length=512, 
            truncation=True
        )


    def extract(self, texts):
        if not hasattr(self, 'goemotions'):
            self.create_pipeline()
        return self.goemotions(texts)

if __name__=="__main__":
	classifier = ExtractEmotions()
	texts = ["Really welcoming hosts. The room is nice and cosy, the location is very quiet so you can get a good sleep. Kitchen is well stocked with equipment. Highly recommended! "]
	results = classifier.classify_texts(texts)
	print(results)