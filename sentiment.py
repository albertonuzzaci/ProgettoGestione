from transformers import RobertaTokenizer, AutoModelForSequenceClassification, pipeline
from whoosh.scoring import BM25F
import math
from reviews import ReviewsIndex

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

class SentimentWeightingModel(BM25F):
    def __init__(self, *args, **kwargs):
        self._user_sentiment = None
        self._reviews_index = ReviewsIndex()
        super().__init__(*args, **kwargs)
    
    def cosine_similarity(self, doc: dict, query: dict):
    
        
        d_norm = math.sqrt(sum(v**2 for v in doc.values()))
        q_norm = math.sqrt(sum(v**2 for v in query.values()))

        num = sum(doc[k]*query[k] for k in (doc.keys() & query.keys()))
        denom = (d_norm * q_norm)

        return num / denom if denom else 0
    
    def _sentiment_score(self, listing_id, sentiment):
        return self.cosine_similarity(self.get_sentiment_for(listing_id), sentiment)
    
    def get_sentiment_for(self, listing_id):
        return self._reviews_index.get_sentiments(int(listing_id))

    def combine_scores(self, textual_score, sentiment_score):
        return textual_score * sentiment_score

    def set_user_sentiment(self, user_sentiment):
        user_sentiment = user_sentiment.strip() + ' '
        

        self._user_sentiment = {k: 1 for k in user_sentiment.split(" ")}
        if 'not' in self._user_sentiment: del self._user_sentiment['not']


    def final(self, searcher, docnum, textual_score):
        textual_score = super().final(searcher, docnum, textual_score)
        if not self._user_sentiment: 
            print("here")
            return textual_score

        id = searcher.stored_fields(docnum)['id']
        sentiment_score = self._sentiment_score(id, self._user_sentiment)
        return self.combine_scores(textual_score, sentiment_score)

if __name__=="__main__":
	classifier = ExtractEmotions()
	text = "We had a great (3-week) stay. The house is exactly as presented in the photos, and is in an excellent location - the road itself is very quiet, but is just around the corner from the increasingly buzzing action of Parson's Green. Camilla was a great host - very quick to reply to any messages, and she made checking in and checking out extremely easy. Would definitely stay here again."
	results = classifier.extract(text)
	print(results)