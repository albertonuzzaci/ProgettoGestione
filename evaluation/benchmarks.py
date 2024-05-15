from functools import reduce

'''
    Defines methods to evaluate an IR system through the computation of relevance measures 
    on a set of queries.
'''
class Benchmarks:
    def __init__(self, queries):
        self.queries = queries
    
    '''
        Print the chosen query from the benchmark queries set
    '''
    def print_query(self, q):
        print("UIN: " + self.queries[q]["uin"])
        print("Query: " + self.queries[q]["text"])
        print("Sentiments: " + ", ".join(self.queries[q]["sentiments"]))
        print("Relevant documents: " + ", ".join(map(str, self.queries[q]["relevant_documents"])))
    
    '''
        The fraction of the relevant documents (the set R) which has been retrieved.
    '''
    def recall(self, R, A):
        return len(set(R).intersection(set(A))) / len(R) if len(R) > 0 else 0
    
    '''
        The fraction of the retrieved documents (the set A) which is relevant.
    '''
    def precision(self, R, A):
        return len(set(R).intersection(set(A))) / len(A) if len(A) > 0 else 0
    
    '''
        Precision at Natural Recall Levels.
    '''
    def precisionNRL(self, R, A):
        pNRL = []
        r = 1
        for a in range(len(A)):
            if A[a] in R:
                pNRL.append((r/len(R), r/(a+1)))
                r = r + 1
        for i in range(r, len(R)+1):
            pNRL.append((i/len(R), 0))
        return pNRL
    
    '''
        Precision at Standard Recall Levels.
        Obtained applying ceiling interpolation on the Natural Recall Levels Precision.
    '''
    def precisionSRL(sefl, pNRL):
        i = 0
        pSRL = [(0, pNRL[i][1])]
        for r in range(1, 11):
            if (i+1 < len(pNRL) and r/10 > pNRL[i][0]):
                i = i + 1
            last = i - 1 if i > 0 else 0
            next = i
            pSRL.append((r/10, max(pNRL[last][1], pNRL[next][1])))
        return pSRL
    
    '''
        Compute average precision at each standard recall level across all queries examined.
        
        @param pSRLs: a list of precision measures at standard recall levels
    '''
    def AveragePrecision(self, pSRLs):
        n = len(self.queries)
        if (n != len(pSRLs)):
            print("The number of queries examined does not correspond to the number of precisions.")
            return
        AvP = []
        for r in range(0, 11):
            sum = reduce(lambda x, y : x + y, [p[r][1] for p in pSRLs], 0)
            AvP.append((r/10, sum/n))
        return AvP
    
    '''
        Average of the precisions obtained after each new relevant document is observed.
        
        @param qpSRL: list of precisions at standard recalls level for the examined query
    '''
    def InterAvgPrec(self, qpSRL):
        sum = reduce(lambda x, y: x + y, [qpSRL[i][1] for i in range(len(qpSRL))], 0)
        qIntAvP = sum / len(qpSRL)
        return qIntAvP
    
    '''
        Mean Average Precision: average of the average precisions across all the queries in benchmark queries set.
        
        @param IntAvPs: list of average precisions
    '''
    def MAP(self, IntAvPs):
        sum = reduce(lambda x, y: x + y, [p for p in IntAvPs], 0)
        return sum / len(IntAvPs)
    
    '''
        Precision at position R in the ranking of results for a query that has R relevant documents.
    
        @param R: list of relevant documents
        @param A: list of answers to the examined query
    '''
    def RPrecision(self, R, A):
        r = len(R)
        return self.precision(R, A[:r])
        
    '''
        List of subtractions between RPrecision of version 1 and version 2 for each query in the benchmark 
        queries set.
    
        @param Av1: list of lists of answers to each query provided by the version 1
        @param Av1: list of lists of answers to each query provided by the version 1
    '''
    def RPrecisions(self, Av1, Av2):
        RPs = []
        for q in range(len(self.queries)):
            RPs.append(self.RPrecision(self.queries[q]["relevant_documents"], Av1[q]) - 
                       self.RPrecision(self.queries[q]["relevant_documents"], Av2[q]))
        return RPs
    
    '''
        Harmonic Mean.
        
        @param R: list of relevant documents
        @param A: list of answers to the examined query
    '''
    def FMeasure(self, R, A):
        r = self.recall(R, A)
        p = self.precision(R, A)
        return (2*r*p)/(p+r)
    
    '''
        If b > 1 emphasizes precision, if b < 1 emphasizes recall, otherwise (b = 1) is equivalent to 
        the complement of harmonic mean.
    
        @param R: list of relevant documents
        @param A: list of answers to the examined query
        @param b
    '''
    def EMeasure(self, R, A, b):
        r = self.recall(R, A)
        p = self.precision(R, A)
        return 1-((1+b**2)/((b**2)/r + 1/p))

# features tests
if __name__ == "__main__":
    q = [{
        "UIN" : "Simulator of real farms",
        "query" : "farm simulator",
        "fields" : ["name", "description"],
        "relevant_documents" :
        [
            236790, 259890, 273790, 92900, 313160, 447020, 90200, 787860, 612030, 220260
        ]
    },
    {
        "UIN" : "Planes flight simulator in virtual reality",
        "query" : "flight simulator vr",
        "fields" : ["name", "description", "cgt"],
        "relevant_documents" :
        [
            314160, 269950, 434030, 223750, 1001240, 347170, 862390
        ]
    }]
    b = Benchmarks(q)
    a = [0, 314160, 1, 269950, 434030, 3, 347170, 4, 5, 862390, 223750]
    pNRL = b.precisionNRL(b.queries[1]["relevant_documents"], a)
    pSRL = b.precisionSRL(pNRL)
    print(pNRL)
    print(pSRL)
                