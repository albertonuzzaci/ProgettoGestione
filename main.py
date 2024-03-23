from index import Index
from GUI.gui import MyGUI
from controller import Controller
from model import IRModel
from sentiment import SentimentWeightingModel

def main() -> None:
    my_index = Index(forceBuildIndex=False, limit=1000)
    my_model = IRModel(my_index,SentimentWeightingModel())
    control = Controller(my_index, my_model)
    MyGUI(control)
    

if __name__ == "__main__":
    main()