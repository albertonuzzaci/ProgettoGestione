from index import Index
from whoosh import qparser
from whoosh.scoring import WeightingModel
from sentiment.sentiment_model import SentimentModelWA
from doc2vec.doc2vec_model import Doc2VecModel
from functools import reduce
from whoosh.scoring import BM25F

class IRModel:
	def __init__(self, index: Index, weightingModel: WeightingModel = BM25F):
		self.index = index
		self.model = weightingModel
		self.query = ""

	def search(self, query: str, resLimit, sentiments=None, verbose=True):
		resDict = {}
		correctedString = ""
		try:
			if isinstance(self.model, SentimentModelWA):
				self.model.set_user_sentiment(sentiments)
			elif isinstance(self.model, Doc2VecModel):
				self.model.set_query(query)
			s = self.index.indexAcc.searcher(weighting = self.model)
			qp = qparser.MultifieldParser(['name','description'], schema=self.index.schemaAcc, group=qparser.OrGroup)

   
			parsedQ = qp.parse(query)
			if(verbose):
				print(f"Input: {query}")			
				print(f"Parsed query: {parsedQ}")
    
			results = s.search(parsedQ, terms=True, limit=resLimit)
			for i in results:
				resDict[i["id"]] = [ i["name"], i["price"]]
			
			corrected = s.correct_query(parsedQ, query)
			if corrected.query != parsedQ:
				correctedString = reduce(
        			lambda x,y: x+" "+str(y[1]),
           			list(filter(lambda term: term[1] if term[0] == "name" else "", corrected.query.iter_all_terms())),
					""
              	).strip()
		except Exception as e: 
			print(e)
		finally:
			s.close()
		return correctedString, resDict