from index import Index
from whoosh import qparser
from whoosh import query, scoring
from whoosh.scoring import WeightingModel
from whoosh.index import open_dir


class IRModel:
	def __init__(self, index: Index, weightingModel: WeightingModel):
		self.index = index
		self.model = weightingModel
  
	def search(self, query: str, resLimit):
		resDict = {}
		try:
			s = self.index.indexAcc.searcher()
			#qp = qparser.QueryParser("recipe_name", schema=my_index.schema)
		
			qp = qparser.MultifieldParser(['name','description'], schema=self.index.schemaAcc, group=qparser.OrGroup)
			
			parsedQ = qp.parse(input)
			print(f"Input: {input}")
			print(f"Parsed query: {parsedQ}")
			results = s.search(parsedQ, terms=True, limit=resLimit)
			for i in results:
				print(i.matched_terms())
				resDict[i["id"]] = [ i["name"], i["price"]]
			
			return resDict
		except Exception as e: 
			print(e)
		finally:
			s.close()
		return resDict