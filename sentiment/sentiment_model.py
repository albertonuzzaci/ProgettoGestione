from whoosh.scoring import BM25F
import math
from sentiment.reviews import ReviewsIndex
from sentiment.extract_emotions import ExtractEmotions


class SentimentModelWA(BM25F): # Sentiment Model Weighted Average
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_sentiment = None
        self.reviews_index = ReviewsIndex()
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
        if denom:
            return num/denom
        return 0
    
    def get_sentiment_score(self, listing_id, sentiment):
        '''
        Cosine similarity tra: 
            - sentimenti di un certo documento
            - sentimenti query
        '''
        return self.cosine_similarity(self.reviews_index.get_sentiments(int(listing_id)), sentiment)
    

    def set_user_sentiment(self, user_sentiment: list=None):
        '''
        Imposta i sentimenti in un dizionario dove le chiavi sono i sentimenti. 
        '''
        if user_sentiment:
            self.user_sentiment = {k: 1 for k in user_sentiment}
        else:
            self.user_sentiment = None


    def final(self, searcher, docnum, score):
        global listScore
        
        score = super().final(searcher, docnum, score)
                            
        if not self.user_sentiment:
            return score

        id = searcher.stored_fields(docnum)['id']
        sentiment_score = self.get_sentiment_score(id, self.user_sentiment)
        
        return ((score/30*70)+(sentiment_score*30))/2
 
class SentimentModelARWA(SentimentModelWA): # Sentiment Model Len Review Weighted Average
    '''
    Modello che differisce dal primo poichè premia i documenti con più recensioni penalizzando
    pesantemente quelli che ne hanno poche. 
    '''
    def final(self, searcher, docnum, score):
        score = super().final(searcher, docnum, score)
        if not self.user_sentiment:
            return score
        id = searcher.stored_fields(docnum)['id']
        sentiment_score = self.get_sentiment_score(id, self.user_sentiment)
        
        return ((score/30*70)+(sentiment_score*20)+(self.reviews_index.get_sentiment_len_for(id)*10))/3