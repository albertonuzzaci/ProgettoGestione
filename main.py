from index import Index
from GUI.gui import MyGUI
from controller import Controller
from model import IRModel
from Sentiment.sentimentModel import AdvancedSentimentWeightingModel, SentimentWeightingModel
from Doc2Vec.doc2vec_model import Doc2VecModel
def main() -> None:
    my_index = Index(forceBuildIndex=False)
    sent = Doc2VecModel()
    my_model = IRModel(my_index, sent)
    control = Controller(my_index, my_model)
    MyGUI(control)
    

if __name__ == "__main__":
    main()