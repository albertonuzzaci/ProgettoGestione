from whoosh.scoring import BM25F
import math
from Sentiment.reviews import ReviewsIndex
from Sentiment.extractEmotions import ExtractEmotions

class SentimentWeightingModel(BM25F):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_sentiment = None
        self._reviews_index = ReviewsIndex()
        self.use_final = True
        
    
    def cosine_similarity(self, doc: dict, query: dict):
        '''
        Calcola cosine similarity.
        '''
        #denominatore
        d_norm = math.sqrt(sum(v**2 for v in doc.values()))                 #radice norma documenti ritrovati
        q_norm = math.sqrt(sum(v**2 for v in query.values()))               #radice norma query
        denom = (d_norm * q_norm)                                           

        #numeratore
        num = sum(doc[k]*query[k] for k in (doc.keys() & query.keys()))
        #print(doc,query)
        if denom:
            return num/denom
        return 0
    
    def get_sentiment_score(self, listing_id, sentiment):
        '''
        Cosine similarity tra: 
            - sentimenti di un certo documento
            - sentimenti query
        '''
        return self.cosine_similarity(self._reviews_index.get_sentiments(int(listing_id)), sentiment)
    

    def set_user_sentiment(self, user_sentiment: list=None):
        if user_sentiment:
            self._user_sentiment = {k: 1 for k in user_sentiment}
        else:
            self._user_sentiment = None


    def final(self, searcher, docnum, score):
        score = super().final(searcher, docnum, score)
        if not self._user_sentiment:
            return score

        id = searcher.stored_fields(docnum)['id']
        sentiment_score = self.get_sentiment_score(id, self._user_sentiment)
        return (score*sentiment_score)

class AdvancedSentimentWeightingModel(SentimentWeightingModel):
    
    def final(self, searcher, docnum, score):
        score = super().final(searcher, docnum, score)
        if not self._user_sentiment:
            return score

        id = searcher.stored_fields(docnum)['id']
        sentiment_score = self.get_sentiment_score(id, self._user_sentiment)
        #print(sentiment_score, score)
        return (score*sentiment_score*self._reviews_index.get_sentiment_len_for(id))


if __name__=="__main__":
	classifier = ExtractEmotions()
	text = "We had a great (3-week) stay. The house is exactly as presented in the photos, and is in an excellent location - the road itself is very quiet, but is just around the corner from the increasingly buzzing action of Parson's Green. Camilla was a great host - very quick to reply to any messages, and she made checking in and checking out extremely easy. Would definitely stay here again."
	results = classifier.extract(text)
	print(results)