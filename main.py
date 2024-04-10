from index import Index
from GUI.gui import MyGUI
from controller import Controller
from model import IRModel
from Sentiment.sentimentModel import SentimentWeightingModel

def main() -> None:
    my_index = Index(forceBuildIndex=False)
    sent = SentimentWeightingModel()
    my_model = IRModel(my_index, sent)
    control = Controller(my_index, my_model)
    MyGUI(control)
    

if __name__ == "__main__":
    main()