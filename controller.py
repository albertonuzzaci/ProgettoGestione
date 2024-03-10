from index import searchAcc

class Controller():
    
    nresult = 10
    inputSearch = ""
    people = None
    resultsDict = {}
    
    #pricemax
    #scoremin
    #neighborhood
    #beds
    
    
    def __init__(self, index):
        self.index = index
        
    def callSearch(self):
        results = searchAcc(self.index, Controller.inputSearch, Controller.nresult, Controller.people)
        Controller.resultsDict = results
        return results
    
    
    @staticmethod
    def updateResult(val):
        Controller.nresult = val
    
    @staticmethod
    def updateInputSearch(val):
        Controller.inputSearch = val
    
    @staticmethod
    def updatePeople(val):
        Controller.people = val