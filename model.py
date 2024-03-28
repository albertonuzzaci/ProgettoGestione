from index import Index
from whoosh import qparser
from whoosh import query, scoring
from whoosh.scoring import WeightingModel
from whoosh.index import open_dir
from Sentiment.sentimentModel import SentimentWeightingModel


class IRModel:
	def __init__(self, index: Index, weightingModel: WeightingModel):
		self.index = index
		self.model = weightingModel

	def search(self, query: str, resLimit, sentiments=None):
		resDict = {}
		try:
			if isinstance(self.model, SentimentWeightingModel):
				self.model.set_user_sentiment(sentiments)

			s = self.index.indexAcc.searcher(weighting = self.model)
			#qp = qparser.QueryParser("recipe_name", schema=my_index.schema)
		
			qp = qparser.MultifieldParser(['name','description'], schema=self.index.schemaAcc, group=qparser.OrGroup)
		
			parsedQ = qp.parse(query)
			print(f"Input: {query}")
			print(f"Parsed query: {parsedQ}")
			results = s.search(parsedQ, terms=True, limit=resLimit)
			for i in results:
				print(i.matched_terms())
				resDict[i["id"]] = [ i["name"], i["price"]]
				print(i.score)
			
			return resDict
		except Exception as e: 
			print(e)
		finally:
			s.close()
		return resDict