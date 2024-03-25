from whoosh.scoring import BM25F
import math
from Sentiment.reviews import ReviewsIndex
from Sentiment.extractEmotions import ExtractEmotions

class SentimentWeightingModel(BM25F):
    def __init__(self, *args, **kwargs):
        self._user_sentiment = None
        self._reviews_index = ReviewsIndex()
        super().__init__(*args, **kwargs)
    
    def cosine_similarity(self, doc: dict, query: dict):
        '''
        Calcola cosine similarity.
        '''
        #denominatore
        d_norm = math.sqrt(sum(v**2 for v in doc.values()))                 #radice norma documenti ritrovati
        q_norm = math.sqrt(sum(v**2 for v in query.values()))               #radice norma query
        denom = (d_norm * q_norm)                                           

        #numeratore
        num = sum(doc[k]*query[k] for k in (doc.keys() & query.keys()))     #! ???? cosa sarebbe la &

        return num / denom if denom else 0
    
    def _sentiment_score(self, listing_id, sentiment):
        '''
        Cosine similarity tra: 
            - sentimenti di un certo documento
            - sentimenti query
        '''
        return self.cosine_similarity(self.get_sentiment_for(listing_id), sentiment)
    
    def get_sentiment_for(self, listing_id):
        '''
        Ritorna i sentimenti di un certo documento
        #! Funzione che secondo me si può togliere.... tanto vale usare direttamente il get_sentiments sopra...
        '''
        return self._reviews_index.get_sentiments(int(listing_id))

    def combine_scores(self, textual_score, sentiment_score):
        return textual_score * sentiment_score

    def set_user_sentiment(self, user_sentiment: list):
        #user_sentiment = user_sentiment.strip() + ' '
        
        self._user_sentiment = {k: 1 for k in user_sentiment}
        #if 'not' in self._user_sentiment: del self._user_sentiment['not'] #! si può togliere per me


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