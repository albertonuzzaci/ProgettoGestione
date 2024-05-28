from model import IRModel
from index import Index

class Controller():
    
    nresult = 10
    
    inputSearch = ""
    
    people = None
    
    resultsDict = {}
    
    pricemax = None
    
    scoremin = None
    
    beds = None
    
    bath = None
    
    neighborhood = []
    
    sentiments = []
    
    correctedQuery = ""
    
    def __init__(self, index:Index, model: IRModel):
        self.index = index
        self.model = model
        
    def callSearch(self):
        if len(Controller.sentiments) == 0:
            correctedQuery, results = self.model.search(Controller.getInput(), Controller.nresult)
        else:
            correctedQuery, results = self.model.search(Controller.getInput(), Controller.nresult, Controller.sentiments)
        Controller.correctedQuery = correctedQuery
        Controller.resultsDict = results

        return results
    
    @staticmethod
    def getInput():
        inputQuery = ""
        if Controller.inputSearch != "":
            inputQuery += f'({Controller.inputSearch})'
        if Controller.people != None and Controller.people != 0:
                inputQuery += f' AND accomodates:[{Controller.people} TO {float(Controller.people)+0.99}]'
        if Controller.pricemax != None:
            inputQuery += f' AND price:[0 TO {Controller.pricemax}]'
        if Controller.scoremin != None:
            inputQuery += f' AND review_scores_rating:[{Controller.scoremin} TO 5]'
        if Controller.beds != None: 
            if Controller.beds != "3+":
                inputQuery += f' AND beds:[{Controller.beds} TO {float(Controller.beds)+0.99}]'
            else:
                inputQuery += f' AND beds:[3 TO]'
        if Controller.bath != None:
            if Controller.bath != "3+":
                inputQuery += f' AND bathrooms:[{Controller.bath} TO {float(Controller.bath)+0.99}]'
            else:
                inputQuery += f' AND bathrooms:[3.0 TO]'
        
        if len(Controller.neighborhood):
            inputQuery += f' AND neighbourhood_cleansed:({" OR ".join(Controller.neighborhood)})'

        return inputQuery

    def getSuggestion(self):
        return Controller.correctedQuery
    
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
        
    @staticmethod
    def updateScore(val):
        Controller.scoremin = val
    
    @staticmethod
    def updateNeighborhood(val):
        Controller.neighborhood.append(val)
        
    @staticmethod
    def removeNeighborhood(val):
        Controller.neighborhood.remove(val)

    @staticmethod
    def updateBeds(val=None):
        Controller.beds = val
    
    @staticmethod
    def updateBaths(val=None):
        Controller.bath = val

    @staticmethod
    def addSentiment(val):
        Controller.sentiments.append(val)
        print(Controller.sentiments)
    
    @staticmethod
    def removeSentiment(val):
        Controller.sentiments.remove(val)
        print(Controller.sentiments)
