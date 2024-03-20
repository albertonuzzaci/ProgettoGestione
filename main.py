from index import Index
from GUI.gui import MyGUI
from controller import Controller

def main() -> None:
    my_index = Index(forceBuildIndex=False)
    control = Controller(my_index)
    my_gui = MyGUI(control)
    

if __name__ == "__main__":
    main()