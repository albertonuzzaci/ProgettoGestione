from index import Index
from GUI.gui import MyGUI
from controller import Controller

if __name__ == "__main__":
    my_index = Index(forceBuildIndex=False, limit=1000)
    control = Controller(my_index)
    my_gui = MyGUI(control)
    
