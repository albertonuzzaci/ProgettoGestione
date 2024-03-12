from index import searchAcc

class Controller():
    
    nresult = 10
    inputSearch = ""
    people = None
    resultsDict = {}
    pricemax = None
    #scoremin
    #neighborhood
    #beds
    
    
    def __init__(self, index):
        self.index = index
        
    def callSearch(self):
        print(f"{Controller.getInput()}")
        results = searchAcc(self.index, Controller.getInput(), Controller.nresult)
        Controller.resultsDict = results
        return results
    
    @staticmethod 
    def getInput():
        inputQuery = ""
        if Controller.inputSearch != "":
            inputQuery += Controller.inputSearch
        if Controller.people != None and Controller.people != 0:
            inputQuery += f' AND accomodates:{Controller.people}'
        if Controller.pricemax != None:
            inputQuery += f' AND price:[0 TO {Controller.pricemax}]'
        return inputQuery
        
    @staticmethod
    def updateResult(val):
        Controller.nresult = val
    
    @staticmethod
    def updateInputSearch(val):
        Controller.inputSearch = val
    
    @staticmethod
    def updatePeople(val):
        Controller.people = val

    @staticmethod
    def updatePrice(val):
        Controller.pricemax = val
    