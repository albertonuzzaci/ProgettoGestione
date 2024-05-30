from index import Index
from model import IRModel
from functools import reduce


class Benchmark():
    
    def __init__(self, query):
        self.query = query
        self.index = Index()
    
    def getResults(self, nResult, model, verbose = False):
        my_model = IRModel(self.index, model)
        _, result = my_model.search(query=self.query["query"], resLimit=nResult, sentiments=self.query["sentiments"], verbose=verbose)
        
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
        levels = [i / 10 for i in range(11)] 
        srlValues = []
        
        if verbose:
            print(f'Natural Recall-Precision Values {zip(precision, recall)}')

        for level in levels:
            precisions = [p for p, r in zip(precision, recall) if r >= level]
           
            if precisions:
                srlValues.append(max(precisions))
            else:
                srlValues.append(0.0)

        srlValues = list(zip(levels, srlValues))
        
        if verbose:
            print(f'Standard Recall-Precision Values {srlValues}')
        return srlValues 
        
    
    
    def getNIapAvgPrecision(self, precision, recall, verbose = False):
        NIapAvgP = [precision[i] for i in range(len(recall)) if i == 0 or recall[i] != recall[i-1]]
        
        if verbose:
            print(NIapAvgP)
            
            
        return round(sum(NIapAvgP)/len(self.query["relevant_documents"]),2) if len(self.query["relevant_documents"]) != 0 else 0

    def getIapAvgPrecision(self, SRLValues, verbose = False):
        sumPrec = reduce(lambda x, y: x + y, [SRLValues[i][1] for i in range(len(SRLValues))], 0)
        IapAvgPrec = round(sumPrec / len(SRLValues), 2)
        
        if verbose:
            print(f"Interpolated Average precision: {IapAvgPrec}")
        
        return IapAvgPrec

    def getRPrecision(self, result, verbose = False):
        relevantDocRetrivedFirstRPosition = set(result[:len(self.query["relevant_documents"])]).intersection(set(self.query["relevant_documents"]))
        RPrec = round(len(relevantDocRetrivedFirstRPosition)/len(self.query["relevant_documents"]),2) if len(self.query["relevant_documents"]) != 0 else 0
        
        if verbose:
            print(f"R-Precision: {RPrec}") 
            
        return RPrec
    
    def getFMeasure(self, result, verbose = False):
        r = self.recall(self.query["relevant_documents"], result)
        p = self.precision(self.query["relevant_documents"], result)
        
        FMeasure = round((2*r*p)/(p+r),2)
        
        if verbose:
            print(f"F-Measure: {FMeasure}")
            
        return FMeasure

    
    def getEMeasure(self, result, b, verbose = False):
        r = self.recall(self.query["relevant_documents"], result)
        p = self.precision(self.query["relevant_documents"], result)

        EMeasure = round(1-((1+b**2)/((b**2)/r + 1/p)),2)
        
        if verbose:
            print(f"E-Measure: {EMeasure}")
        
        return EMeasure
    
    def __str__(self) -> str:
        return f'UIN: {self.query["UIN"]}\nQuery: {self.query["query"]}\nSentiments: {self.query["sentiments"]}\nRelevant documents: {self.query["relevant_documents"]} '