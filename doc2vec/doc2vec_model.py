# This module contains the custom classes for scoring
from whoosh.scoring import BM25F
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from whoosh.analysis import StandardAnalyzer
import json
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_query(query, model:Doc2Vec):
    analyzer = StandardAnalyzer()
    processed_query = [token.text for token in analyzer(query)]
    
    query_vector = model.infer_vector(processed_query)
    return query_vector



def get_doc2vec_score(id, query, docs, model):
    query_vector = preprocess_query(query, model)
    doc_vector = docs[id]
    similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
    return similarity
    
class Doc2VecModel(BM25F):
    use_final = True
    
    def __init__(self):
        super().__init__(B=0.75, K1=1.5)
        self.model = Doc2Vec.load("./Doc2Vec/doc2vec.model")
        with open("./Doc2Vec/docs_vectors.json", "r") as f:
            self.docs = json.load(f)
    
    def set_query(self, query):
        self.query = query  
        
    def final(self, searcher, docnum, score):
        id = searcher.stored_fields(docnum)['id']
        doc2vec_score = get_doc2vec_score(id, self.query, self.docs, self.model)
        
        
        return score * doc2vec_score
