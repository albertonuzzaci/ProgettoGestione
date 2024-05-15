#import external libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functools import reduce
#import usefull classes
from index import Index
from model import IRModel
#Import the models





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
   
   
    def getSRLValues(self, precision, recall, verbose = False):
        levels = [i / 10 for i in range(11)] # Livelli di richiamo standard: 0.0, 0.1, ..., 1.0
        srlValues = []
        
        NRLvalues = zip(precision, recall)
        
        if verbose:
            print(f'Natural Recall-Precision Values {list(NRLvalues)}')

        for level in levels:
            precisions = [p for p, r in NRLvalues if r >= level]
            if precisions:
                srlValues.append(max(precisions))
            else:
                srlValues.append(0.0)

        srlValues = list(zip(levels, srlValues))
        
        if verbose:
            print(f'Standard Recall-Precision Values {srlValues}')
            
        return srlValues
    

if __name__ == "__main__":
    
    bench_test = Benchmark(query_test_2)
    
    axes = ["standard recall levels", "precision"]
    df = pd.DataFrame()
    
    for model, model_name in models:
        result = bench_test.getResults(10, model)
        SRLValues = bench_test.getSRLValues(
            bench_test.getPrecisionValues(result),
            bench_test.getRecallValues(result)
        )
        
        dfB = pd.DataFrame(SRLValues, columns = axes)
        dfB["Version"] = f'{model_name}'
        
        df = pd.concat([df, dfB])

    sns.set_theme()

    # create a dataframe for Seaborn

    # plot the line graph
    pltP = sns.lineplot(data = df, x = 'standard recall levels', y = 'precision', marker='o', markersize=8, 
                hue="Version", palette="colorblind")

    # set fixed axes, the semicolon suppress the output
    pltP.set_xlim([-0.05, 1.05])
    pltP.set_ylim([-0.05, 1.05])
    
    

   


		