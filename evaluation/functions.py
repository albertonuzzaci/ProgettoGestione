#import external libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functools import reduce
#import usefull classes
from index import Index
from model import IRModel
#Import the models
from whoosh.scoring import BM25F
from doc2vec.doc2vec_model import Doc2VecModel
from sentiment.sentiment_model import SentimentWeightingModel, AdvancedSentimentWeightingModel

models = [
	BM25F() 
 	#Doc2VecModel(),
	#SentimentWeightingModel(),
	#AdvancedSentimentWeightingModel()
]

query_test = {
	"UIN" : "enjoyable double room",
	"query" : "double room",
	"sentiments" : [
        "joy", "surprise"
    ],
	"relevant_documents" : [
        8032080, 13763334, 19636343
    ]
}

query_test_2 = {
        "uin": "I need an apartment near st james park",
        "query": "apartment near st james",
        "sentiments":[],
        "relevant_documents": [
            44652702,17989962,6430495,561569908310899814,541903175815998607,15336396,15954244,51592505,544034283385258902,584579738630287719,49478531,51592515,51677622
        ]
    }

class Benchmark():
    
    def __init__(self, query):
        self.query = query
        self.index = Index()
    
    def getResults(self, nResult, model, verbose = False):
        my_model = IRModel(self.index, model)
        _, result = my_model.search(query=self.query["query"], resLimit=nResult, sentiments=self.query["sentiments"])
        results = [int(id) for id in result.keys()]
        if verbose:
            print(f'Results: {results}\nRelevant documents: {self.query["relevant_documents"]}')
        print(f'Relevant retrived: {set(results).intersection(set(self.query["relevant_documents"]))}')
        return results
    
    def recall(self, R, A):
        return round(len(set(R).intersection(set(A))) / len(R), 2) if len(R) > 0 else 0
    
    def precision(self, R, A):
        return round(len(set(R).intersection(set(A))) / len(A), 2) if len(A) > 0 else 0

    def getPrecisionValues(self, resultsDoc, verbose = False):
        precisionValues = []
        
        for c in range(1, len(resultsDoc)+1):
            precisionValues.append(self.precision(self.query["relevant_documents"], resultsDoc[:c]))
        
        if verbose:
            print(f'Precision values: {precisionValues}')
            
        return precisionValues
  
    def getRecallValues(self, resultsDoc, verbose = False): 
        recallValues = []
        for c in range(1, len(resultsDoc)+1):
            recallValues.append(self.recall(self.query["relevant_documents"], resultsDoc[:c]))

        if verbose:
            print(f'Recall values: {recallValues}')
        
        return recallValues
    
    def getNRLValues(self, model, nResult, verbose=False):
        results = self.getResults(nResult, model, verbose)
        p_val = self.getPrecisionValues(results, verbose)
        r_val = self.getRecallValues(results, verbose)
        NPRvalues = list(zip(r_val, p_val))
        if verbose:
            print(f'Recall-Precision Values: {NPRvalues}')
        
        return NPRvalues
    
    def getSRLValues(self, pNRL):
        i = 0
        pSRL = [(0, pNRL[i][1])]
        for r in range(1, 11):
            if (i+1 < len(pNRL) and r/10 > pNRL[i][0]):
                i = i + 1
            last = i - 1 if i > 0 else 0
            next = i
            pSRL.append((r/10, max(pNRL[last][1], pNRL[next][1])))
        return pSRL
    import numpy as np
    
    def getSRLValuesChatty(self, precision, recall):
        levels = [i / 10 for i in range(11)] # Livelli di richiamo standard: 0.0, 0.1, ..., 1.0
        srlValues = []
        for level in levels:
            precisions = [p for p, r in zip(precision, recall) if r >= level]
            if precisions:
                srlValues.append(max(precisions))
            else:
                srlValues.append(0.0)

        return list(zip(levels, srlValues))
    
    
    def plot(self, prVal):
                
        x, y = zip(*prVal)
        
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, 'bo')  
        
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Query: {self.query["query"]}')

    def plot_sns():
        # plot the precisions
        # apply the default theme
        sns.set_theme()

        axes = ["standard recall levels", "precision"]

        dfB = pd.DataFrame(pB, columns = axes)
        dfB["Version"] = "Base"

        dfAV = pd.DataFrame(pAV, columns = axes)
        dfAV["Version"] = "Sentiment Analysis AV"

        dfINAV = pd.DataFrame(pINAV, columns = axes)
        dfINAV["Version"] = "Sentiment Analysis INAV"

        # create a dataframe for Seaborn
        df = pd.concat([dfB, dfAV, dfINAV])

        # print the examined query
        b.print_query(examined_q)

        # plot the line graph
        pltP = sns.lineplot(data = df, x = 'standard recall levels', y = 'precision', marker='o', markersize=8, 
                    hue="Version", palette="colorblind")

        # set fixed axes, the semicolon suppress the output
        pltP.set_xlim([-0.05, 1.05])
        pltP.set_ylim([-0.05, 1.05])

if __name__ == "__main__":
    bench_test = Benchmark(query_test_2)
    
    for i in models:
        print("\n",i.__class__.__name__)
        results = bench_test.getResults(10, i)
        NRLVal = bench_test.getNRLValues(i, 10, True)
        SRLVal = bench_test.getSRLValues(NRLVal)
        chatty = bench_test.getSRLValuesChatty(bench_test.getPrecisionValues(results), 
                                               bench_test.getRecallValues(results))
        print(SRLVal)
        bench_test.plot(chatty)
    plt.show()
        
        
# [(0.08, 1.0), (0.15, 1.0), (0.15, 0.67), (0.23, 0.75), (0.23, 0.6), (0.23, 0.5), (0.23, 0.43), 
# (0.23, 0.38), (0.23, 0.33), (0.31, 0.4)]
    # 0.0 -> >= 0.0 = 1.0
    # 0.1 -> >= 0.1 = 1.0
    # 0.2 -> >= 0.2 = 0.75
    # 0.3 -> >= 0.3 = 0.4
    # 0.4 -> >= 0.4 = 0 
        
    


		