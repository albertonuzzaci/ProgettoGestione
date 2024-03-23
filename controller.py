from model import IRModel

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
    
    
    def __init__(self, index, model):
        self.index = index
        self.model = model
    def callSearch(self):
        results = self.model.search(Controller.getInput(), Controller.nresult)
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
        if Controller.scoremin != None:
            inputQuery += f' AND review_scores_rating:[{Controller.scoremin} TO 5]'
        if Controller.beds != None: 
            if Controller.beds != "3+":
                inputQuery += f' AND beds:{Controller.beds}'
            else:
                inputQuery += f' AND beds:[3 TO]'
        if Controller.bath != None:
            if Controller.bath == "1":
                inputQuery += f' AND bathrooms:[1.0 TO 1.99]'
            elif Controller.bath == "2":
                inputQuery += f' AND bathrooms:[2.0 TO 2.99]'
            elif Controller.bath == "3+":
                inputQuery += f' AND bathrooms:[3.0 TO]'
        
        if len(Controller.neighborhood):
            inputQuery += f' AND neighbourhood_cleansed:({" OR ".join(Controller.neighborhood)})'

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