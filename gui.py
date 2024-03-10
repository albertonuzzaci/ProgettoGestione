import customtkinter as ctk
import tkinter, yaml
from CTkListbox import *
from tkinter import ttk, Menu
from controller import Controller
from index import Index
import threading

index = Index()
control = Controller(index)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def searchFunction(input, valueList):
    valueList.delete("all")
    control.updateInputSearch(input)
    results = list(control.callSearch().values())
    for c, elem in enumerate(results):
        valueList.insert(c, elem)


def setResult(var):
    control.updateResult(var)
    
def increase(lbl, valueList):
    lbl.configure(text=int(lbl.cget("text"))+1)
    control.updatePeople(int(lbl.cget("text")))
    if(control.inputSearch != ""): 
        searchFunction(control.inputSearch, valueList)
    
def decrease(lbl, valueList):
    if(int(lbl.cget("text"))>0):
        lbl.configure(text=int(lbl.cget("text"))-1)
        control.updatePeople(int(lbl.cget("text"))) 
        if(control.inputSearch != ""):
            searchFunction(control.inputSearch, valueList)
    
def onselect(evt, listbox, mainView):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        try:
            newTab = mainView.add(f'{selected_item.strip()[:10]}{"..." if len(selected_item)>10 else ""}')
        except ValueError:
            print("Pagina già aperta") # METTERSI D'ACCORDO SU COME GESTIRE IL CASO
        
def slider_ev(value, label, info):
    print(info.cget("text"))
    if info.cget("text")=="Price Max":
        label.configure(text=f"{int(value)}€")
    else:
        label.configure(text=f"{round(value,1)} ☆")

def reset(*args):
    #RadioButton Results
    args[0].deselect()
    args[1].deselect()
    args[2].deselect()
    
    #People Label
    args[3].configure(text="0")
    
    #Price
    args[4].configure(text="")    
    args[5].set(50)
    
    #Score
    args[6].set(2.5)
    args[7].configure(text="")
    
    #CheckBox Neighborhood
    for check in args[8].get_checked_items():
        check.deselect()
    
    #Beds
    args[9].set(None)
    
    #Baths
    args[10].set(None)
    
def bedsCommand(button):
    print(button.get())

def bathsCommand(button):
    print(button.get())
    
class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item, hover_color="#d72545",fg_color= [ "gray90","#FF385C"])
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox for checkbox in self.checkbox_list if checkbox.get() == 1]

class MyGUI():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.after(1000, self.update)
        
        self.root.geometry("1200x780")
        self.root.resizable(False, False)

        self.myfont = ctk.CTkFont(family="Montserrat", size=15) # PER CAMBIARE FONT
        
        self.mainView =  self.setupTabView()
        searchTab = self.mainView.add("Search Tab") # tab principale per effettuare la ricerca, contiene il mainFrame
    
        self.mainFrame = ctk.CTkFrame(searchTab, corner_radius=10)
        self.mainFrame.pack(pady=20, padx=15, fill="both", expand=True)

        MyGUI.addColumns(2, self.mainFrame)
        
        self.rightFrame = self.setupRightFrame()
        self.rightFrame.grid(column=1, row=0)
        
        self.leftFrame = self.setupLeftFrame()
        self.leftFrame.grid(column=0, row=0)

        
        self.root.mainloop()

    def update(self):
        if control.inputSearch != self.searchField.get():
            searchFunction(self.searchField.get(), self.listbox)
        self.root.after(100, self.update)
        

    def setupTabView(self):
        mainView = ctk.CTkTabview(self.root,
                                  segmented_button_selected_color="#FF385C",
                                  segmented_button_selected_hover_color="#d72545",
                                  segmented_button_unselected_hover_color="#d72545",
                                  anchor='W' # Parametro da modicare in base alle preferenze, posizione del gestore delle tab
                                  )
        mainView.pack(pady=20, padx=10, fill="both", expand=True)
        return mainView

    
    def setupRightFrame(self):

        rFrame = ctk.CTkFrame(self.mainFrame, corner_radius=10)
        MyGUI.addColumns(2, rFrame)
        
        self.searchField = ctk.CTkEntry(master=rFrame, width=400, placeholder_text="Search destinations...", font=self.myfont)
        self.listbox = CTkListbox(master=rFrame, height=500,highlight_color="#FF385C", hover_color="#d72545", font=self.myfont)
        
        self.listbox.bind('<<ListboxSelect>>', lambda evt, lb=self.listbox, mv=self.mainView: onselect(evt, lb, mv))

        searchButton = ctk.CTkButton(master=rFrame, text="Search", font=self.myfont, command = lambda: searchFunction(self.searchField.get(), self.listbox), fg_color="#FF385C", hover_color="#d72545")
        
        self.searchField.grid(column=0, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        searchButton.grid(column=1, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        self.listbox.grid(column=0,columnspan=2, row=1, sticky=ctk.W+ctk.E, padx=10, pady=20)
        return rFrame
    
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self.mainFrame)
        MyGUI.addRows(7, lFrame)
        MyGUI.addColumns(3, lFrame)
    
        
        #---------------RESULT--------------------
        resultsFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(3, resultsFrame)
        
        resLabel = ctk.CTkLabel(master=lFrame, text="#Results", font=self.myfont)
        resLabel.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')
        
        radioVar = ctk.StringVar(value="")
        
        btn10 = ctk.CTkRadioButton(master=resultsFrame, text="10", variable=radioVar, font=self.myfont, command=lambda: setResult(10),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn10.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')

        btn20 = ctk.CTkRadioButton(master=resultsFrame, text="15",variable=radioVar,font=self.myfont,  command=lambda: setResult(15),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn20.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btn30 = ctk.CTkRadioButton(master=resultsFrame, text="20", variable=radioVar, font=self.myfont, command=lambda: setResult(20),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn30.grid(column=2, row=0,padx=10, pady=10, sticky='NSWE')
        
        btn10.select(True)
        
        resultsFrame.grid(column=1, row=0, padx=10, pady=10, sticky="NSWE")

        #-------------ACCOMODATES----------------
        peopleFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(3, peopleFrame)

        peopleLabel = ctk.CTkLabel(master=lFrame, text="People", font=self.myfont)
        peopleLabel.grid(column=0, row=1, padx=10, pady=10, sticky='NSWE')

        
        valuePeopleLabel = ctk.CTkLabel(master=peopleFrame, text="0", font=self.myfont)
        valuePeopleLabel.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btnPeopleMinus = ctk.CTkButton(master=peopleFrame, text="-", font=self.myfont, command=lambda: decrease(valuePeopleLabel, self.listbox), fg_color="#FF385C", hover_color="#d72545")
        btnPeopleMinus.grid(column=0, row=0,padx=10, pady=10, sticky='NSWE')

        btnPeoplePlus = ctk.CTkButton(master=peopleFrame, text="+", font=self.myfont, command=lambda: increase(valuePeopleLabel, self.listbox), fg_color="#FF385C", hover_color="#d72545")
        btnPeoplePlus.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')
      
        peopleFrame.grid(column=1, row=1, padx=10, pady=10, sticky="NSWE")

        #---------------PRICE--------------------
        priceFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(2, priceFrame)
        priceLabel = ctk.CTkLabel(master=lFrame, text="Price Max", font=self.myfont)
        priceLabel.grid(column=0, row=2, padx=10, pady=20, sticky='NSWE')
        
        labelPriceSlider = ctk.CTkLabel(master=priceFrame, text="100€", font=self.myfont)
        priceSlider = ctk.CTkSlider(master=priceFrame, from_=0, to=100, command=lambda x: slider_ev(priceSlider.get(), labelPriceSlider, priceLabel),button_hover_color=["#FF385C", "#FF385C"], button_color=["#d72545", "#d72545"])
        
        
        priceSlider.grid(column=0, row=0,padx=10, pady=20, sticky='NSWE')
        labelPriceSlider.grid(column=1, row=0, sticky='NSWE')
        priceSlider.set(100)
        
        priceFrame.grid(column=1, row=2, padx=10, pady=10, sticky="NSWE")
        
         #---------------SCORE--------------------
        scoreFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(2, scoreFrame)
        scoreLabel = ctk.CTkLabel(master=lFrame, text="Score Min", font=self.myfont)
        scoreLabel.grid(column=0, row=3, padx=10, pady=20, sticky='NSWE')
        
        labelScoreSlider = ctk.CTkLabel(master=scoreFrame, text="0☆", font=self.myfont)
        scoreSlider = ctk.CTkSlider(master=scoreFrame, from_=0, to=5, command=lambda x: slider_ev(scoreSlider.get(), labelScoreSlider, scoreLabel),button_hover_color=["#FF385C", "#FF385C"], button_color=["#d72545", "#d72545"])
        
        scoreSlider.grid(column=0, row=0,padx=10, pady=20, sticky='NSWE')
        scoreSlider.set(0)

        labelScoreSlider.grid(column=1, row=0, sticky='NSWE')
        
        scoreFrame.grid(column=1, row=3, padx=10, pady=10, sticky="NSWE")
        
        #--------------NEIGH-----------------------
        neighLabel = ctk.CTkLabel(master=lFrame, text="Neighborhood", font=self.myfont)
        neighLabel.grid(column=0, row=4, padx=5, pady=20, sticky='NSWE')

        scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=lFrame, height=2, width=200, item_list=[f"item {i}" for i in range(50)])
        scrollable_checkbox_frame.grid(column=1, row=4,  padx=15, pady=15, sticky='NSWE')
        
        #---------------BEDS & BATHS--------------------
        bedsBathsFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(4, bedsBathsFrame)
        
        bedsLabel = ctk.CTkLabel(master=bedsBathsFrame, text="Beds", font=self.myfont)
        bedsLabel.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')
        
        beds_values = ["None","1","2","3+"]
        bedsButton = ctk.CTkSegmentedButton(master=bedsBathsFrame, command=lambda x: bedsCommand(bedsButton),  values=beds_values, corner_radius=80, selected_color="#FF385C", selected_hover_color="#d72545")
        bedsButton.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')
        
        bathsLabel = ctk.CTkLabel(master=bedsBathsFrame, text="Baths", font=self.myfont)
        bathsLabel.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')

        baths_values = ["1","2","3+"]
        bathButton = ctk.CTkSegmentedButton(master=bedsBathsFrame, command=lambda x: bathsCommand(bathButton), values=baths_values, corner_radius=150, selected_color="#FF385C", selected_hover_color="#d72545")
        bathButton.grid(column=3, row=0, padx=10, pady=10, sticky='NSWE')
        bedsBathsFrame.grid(column=0,columnspan=2, row=5, padx=10, pady=10, sticky="NSWE")    
        
        #---------------RESET------------------
        resetButton = ctk.CTkButton(master=lFrame, text="RESET", font=self.myfont, command = lambda: reset(btn10,btn20,btn30,valuePeopleLabel,labelPriceSlider,priceSlider,scoreSlider,labelScoreSlider,scrollable_checkbox_frame,bedsButton,bathButton), fg_color="#FF385C", hover_color="#d72545")
        resetButton.grid(column=0, columnspan=3, row=6, padx=10, pady=10, sticky="NSWE")
        
        return lFrame
    
    
    @staticmethod
    def addColumns(ncolumn, obj):
        for i in range(ncolumn):
            obj.columnconfigure(i, weight=1)
    
    @staticmethod
    def addRows(nrow, obj):
        for i in range(nrow):
            obj.rowconfigure(i, weight=1)




if __name__ == "__main__":
    
    gui = MyGUI()

    