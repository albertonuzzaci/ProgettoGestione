#import external libraries
import matplotlib.pyplot as plt
from functools import reduce
#import usefull classes
from index import Index
from model import IRModel

#Import the models
from whoosh.scoring import BM25F
from Doc2Vec.doc2vec_model import Doc2VecModel
from Sentiment.sentimentModel import SentimentWeightingModel, AdvancedSentimentWeightingModel

models = [
	BM25F(), 
 	Doc2VecModel(),
	SentimentWeightingModel(),
	AdvancedSentimentWeightingModel()
]

query_test = {
	"UIN" : "enjoyable double room",
	"query" : "double room",
	"sentiments" : ["joy", "surprise"],
	"relevant_documents" : [8032080, 13763334, 19636343]
}

query_test_2 = {
        "uin": "I need an apartment near st james park",
        "query": "apartment near st james",
        "sentiments":[],
        "relevant_documents":[44652702,17989962,6430495,561569908310899814,541903175815998607,15336396,15954244,51592505,544034283385258902,584579738630287719,49478531,51592515,51677622]
    }

class Benchmark():
    
    def __init__(self, query):
        self.query = query
        self.index = Index()
    
    def getResults(self, nResult, model):
        my_model = IRModel(self.index, model)
        corQuery, result = my_model.search(query=self.query["query"], resLimit=nResult, sentiments=self.query["sentiments"])
        return [int(id) for id in result.keys()]
    
    def getPrecisionValues(self, resultsDoc):
        relevantDoc_retrieved = 0
        precisionValues = []
        for c, doc in enumerate(resultsDoc):
            if doc in self.query["relevant_documents"]:
                relevantDoc_retrieved += 1
            precisionValues.append(round(relevantDoc_retrieved/(c+1),2))
        return precisionValues
  
    def getRecallValues(self, resultsDoc): 
        relevantDoc_retrieved = 0
        recallValues = []
        for c, doc in enumerate(resultsDoc):
            if doc in self.query["relevant_documents"]:
                relevantDoc_retrieved += 1
            recallValues.append(round(relevantDoc_retrieved/len(self.query["relevant_documents"]),2)
                                if len(self.query["relevant_documents"]) != 0 else 0)
        return recallValues
    
    def getPRValues(self, model, nResult, verbose=False):
        results = self.getResults(nResult, model)
        p_val = self.getPrecisionValues(results)
        r_val = self.getRecallValues(results)
        
        if verbose:
            print(f"Results: {results}")
            print(f'Relevant document: {self.query["relevant_documents"]}')
            print(f"Recall: {r_val}")
            print(f"Precision: {p_val}")
        
        return list(zip(r_val, p_val))
    
    def plot(self, model, nResult):
        prVal = self.getPRValues(model, nResult)
        
        prVal = reduce(lambda acc, punto: acc + [punto] if not acc or acc[-1][0] != punto[0] else acc, prVal, [])
        #[(0.08, 1.0), (0.08, 0.5), (0.08, 0.33), (0.15, 0.5), (0.23, 0.6), 
        # (0.23, 0.5), (0.31, 0.57), (0.38, 0.62), (0.38, 0.56), (0.46, 0.6)]
		#[(0.0, ), (0.1, ),
        print(prVal)
        
        x, y = zip(*prVal)
        
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, 'bo')  
        
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Query: {self.query["query"]}')
        

if __name__ == "__main__":
    bench_test = Benchmark(query_test_2)
    
    for i in models:
        print("\n",i.__class__.__name__)
        print(bench_test.getPRValues(i,10, True))
        bench_test.plot(i, 11)
    
    plt.show()
    
    


		