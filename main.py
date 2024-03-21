from index import Index
from GUI.gui import MyGUI
from controller import Controller
from model import IRModel

def main() -> None:
    my_index = Index(forceBuildIndex=False)
    my_model = IRModel(Index,)
    control = Controller(my_index)
    my_gui = MyGUI(control)
    

if __name__ == "__main__":
    main()