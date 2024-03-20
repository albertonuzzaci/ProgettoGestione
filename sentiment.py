from transformers import BertTokenizer, AutoModelForSequenceClassification, pipeline


class GoEmotionsClassifier:

    def __init__(self, model_name='original'):
        self.tokenizer = BertTokenizer.from_pretrained(f"monologg/bert-base-cased-goemotions-{model_name}")
        self.model = AutoModelForSequenceClassification.from_pretrained(f"monologg/bert-base-cased-goemotions-{model_name}", num_labels=28)


    def create_pipeline(self):
        self.goemotions = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-classification",
            top_k=3,
            function_to_apply='sigmoid'
        )


    def classify_texts(self, texts):
        if not hasattr(self, 'goemotions'):
            self.create_pipeline()
        return self.goemotions(texts)

if __name__=="__main__":
	classifier = GoEmotionsClassifier()
	texts = ["it's happened before?! love my hometown of beautiful new ken 😂😂"]
	results = classifier.classify_texts(texts)
	print(results)