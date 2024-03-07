'''
        self.tabview = ctk.CTkTabview(self.rightFrame, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
'''
        #notebook = ttk.Notebook(self.root)
        #notebook.add(self.mainFrame, text="TAB1")
        #notebook.pack()
        #https://www.youtube.com/watch?v=4en9gSwmn5g

import customtkinter as ctk
import tkinter, yaml
from CTkListbox import *
from tkinter import ttk, Menu


with open('config.yaml','r') as file:
    config_data = yaml.safe_load(file)

 # = config_data["GUI"]["FONTSIZE"]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def cerca(campo, lista):
    print(campo)
    print(lista)
    lista.insert("end", campo)

def setResult(var):
    print(f"set result {var}")

def increase(lbl):
    lbl.configure(text=int(lbl.cget("text"))+1)
    
def decrease(lbl):
    if(int(lbl.cget("text"))>0):
        lbl.configure(text=int(lbl.cget("text"))-1)
    
def onselect(evt, listbox, mainView):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        try:
            newTab = mainView.add(f"{selected_item.strip()[:10]}{"..." if len(selected_item)>10 else ""}")
        except ValueError:
            print("Pagina già aperta") # METTERSI D'ACCORDO SU COME GESTIRE IL CASO
        

def slider_ev(value, label):
    label.configure(text=f"{int(value)}€")

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
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]

class MyGUI():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1200x700")
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
        hotel = [f"Elem{x}" for x in range(15)]
        hotel_selezionato = tkinter.StringVar(value=hotel)
        
        rFrame = ctk.CTkFrame(self.mainFrame, corner_radius=10)
        MyGUI.addColumns(2, rFrame)
        
        searchField = ctk.CTkEntry(master=rFrame, width=400, placeholder_text="Search destinations...")
        listbox = CTkListbox(master=rFrame, listvariable=hotel_selezionato, height=500,highlight_color="#FF385C", hover_color="#d72545")
        listbox.bind('<<ListboxSelect>>', lambda evt, lb=listbox, mv=self.mainView: onselect(evt, lb, mv))

        searchButton = ctk.CTkButton(master=rFrame, text="Search", font=self.myfont, command = lambda: cerca(searchField.get(), listbox), fg_color="#FF385C", hover_color="#d72545")
        
        searchField.grid(column=0, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        searchButton.grid(column=1, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        listbox.grid(column=0,columnspan=2, row=1, sticky=ctk.W+ctk.E, padx=10, pady=20)
        return rFrame
    
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self.mainFrame)
        MyGUI.addRows(7, lFrame)
        MyGUI.addColumns(2, lFrame)
        
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
        
        
        resultsFrame.grid(column=1, row=0, padx=10, pady=10, sticky="NSWE")

        #-------------ACCOMODATES----------------
        peopleFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(3, peopleFrame)

        peopleLabel = ctk.CTkLabel(master=lFrame, text="People", font=self.myfont)
        peopleLabel.grid(column=0, row=1, padx=10, pady=10, sticky='NSWE')

        
        valuePeopleLabel = ctk.CTkLabel(master=peopleFrame, text="0", font=self.myfont)
        valuePeopleLabel.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btnPeopleMinus = ctk.CTkButton(master=peopleFrame, text="-", font=self.myfont, command=lambda: decrease(valuePeopleLabel), fg_color="#FF385C", hover_color="#d72545")
        btnPeopleMinus.grid(column=0, row=0,padx=10, pady=10, sticky='NSWE')

        btnPeoplePlus = ctk.CTkButton(master=peopleFrame, text="+", font=self.myfont, command=lambda: increase(valuePeopleLabel), fg_color="#FF385C", hover_color="#d72545")
        btnPeoplePlus.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')
      
        peopleFrame.grid(column=1, row=1, padx=10, pady=10, sticky="NSWE")

        #---------------PRICE--------------------
        priceFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(2, priceFrame)
        priceLabel = ctk.CTkLabel(master=lFrame, text="Price", font=self.myfont)
        priceLabel.grid(column=0, row=2, padx=10, pady=20, sticky='NSWE')
        
        labelSlider = ctk.CTkLabel(master=priceFrame, text=None, font=self.myfont)
        slider = ctk.CTkSlider(master=priceFrame, from_=0, to=100, command=lambda x: slider_ev(slider.get(), labelSlider),button_hover_color=["#FF385C", "#FF385C"], button_color=["#d72545", "#d72545"])
        
        
        slider.grid(column=0, row=0,padx=10, pady=20, sticky='NSWE')
        labelSlider.grid(column=1, row=0, sticky='NSWE')
        
        priceFrame.grid(column=1, columnspan=2, row=2, padx=10, pady=10, sticky="NSWE")
        #--------------NEIGH-----------------------
        neighLabel = ctk.CTkLabel(master=lFrame, text="Neighborhood", font=self.myfont)
        neighLabel.grid(column=0, row=3, padx=5, pady=20, sticky='NSWE')

        scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=lFrame, height=2, width=200, item_list=[f"item {i}" for i in range(50)])
        scrollable_checkbox_frame.grid(column=1, row=3,  padx=15, pady=15, sticky='NSWE')
        
         #---------------BEDS--------------------
        bedsFrame = ctk.CTkFrame(lFrame, corner_radius=10)
        MyGUI.addColumns(3, bedsFrame)
        
        bedsLabel = ctk.CTkLabel(master=lFrame, text="Beds", font=self.myfont)
        bedsLabel.grid(column=0, row=4, padx=10, pady=10, sticky='NSWE')
        
        radioVar = ctk.StringVar(value="")
        
        btnBed1 = ctk.CTkRadioButton(master=bedsFrame, text="1", variable=radioVar, font=self.myfont, command=lambda: setResult(10),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btnBed1.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')

        btnBed2 = ctk.CTkRadioButton(master=bedsFrame, text="2",variable=radioVar,font=self.myfont,  command=lambda: setResult(15),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btnBed2.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btnBed3 = ctk.CTkRadioButton(master=bedsFrame, text="3+", variable=radioVar, font=self.myfont, command=lambda: setResult(20),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btnBed3.grid(column=2, row=0,padx=10, pady=10, sticky='NSWE')
        
        
        bedsFrame.grid(column=1, row=4, padx=10, pady=10, sticky="NSWE")

        #---------------BATHS--------------------
        bathsFrame = ctk.CTkFrame(lFrame)
        MyGUI.addColumns(3, bathsFrame)
        
        bathsLabel = ctk.CTkLabel(master=lFrame, text="Baths", font=self.myfont)
        bathsLabel.grid(column=0, row=5, padx=10, pady=10, sticky='NSWE')
        radioVar = ctk.StringVar(value="")
        
        btnBath1 = ctk.CTkRadioButton(master=bathsFrame, text="1", variable=radioVar, font=self.myfont, command=lambda: setResult(radioar),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"] )
        btnBath1.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')

        btnBath2 = ctk.CTkRadioButton(master=bathsFrame, text="2",variable=radioVar,font=self.myfont,  command=lambda: setResult(15),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btnBath2.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btnBath3 = ctk.CTkRadioButton(master=bathsFrame, text="3+", variable=radioVar, font=self.myfont, command=lambda: setResult(20),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btnBath3.grid(column=2, row=0,padx=10, pady=10, sticky='NSWE')
        
        
        bathsFrame.grid(column=1, row=5, padx=10, pady=10, sticky="NSWE")
            
        return lFrame

    @staticmethod
    def addColumns(ncolumn, obj):
        for i in range(ncolumn):
            obj.columnconfigure(i, weight=1)
    
    @staticmethod
    def addRows(nrow, obj):
        for i in range(nrow):
            obj.rowconfigure(i, weight=1)
    
'''
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

frameSearch = ctk.CTkFrame(master=frame)
frameSearch.columnconfigure(0, weight=1)
frameSearch.columnconfigure(1, weight=1)

entry = ctk.CTkEntry(master = frameSearch, width=400, placeholder_text="Search destinations...")
entry.grid(column=0, row=0,sticky=ctk.W+ctk.E,padx=10, pady=10)

button = ctk.CTkButton(master=frameSearch, text="SEARCH", command=cerca)
button.grid(column=1, row=0,sticky=ctk.W+ctk.E,padx=10, pady=10)

listbox = CTkListbox(master=frameSearch, listvariable=hotel_selezionato, height=500)
listbox.grid(column=0,columnspan=2, row=1,sticky=ctk.W+ctk.E,padx=10, pady=20)
frameSearch.grid(column=1, row=0)
frameFilter = ctk.CTkFrame(master=frame)
frameFilter.rowconfigure(0, weight=1)
frameFilter.rowconfigure(1, weight=2)
frameFilter.rowconfigure(2, weight=1)
frameFilter.rowconfigure(3, weight=1)
frameFilter.rowconfigure(4, weight=1)
frameFilter.rowconfigure(5, weight=1)
frameFilter.rowconfigure(6, weight=1)



frameResult = ctk.CTkFrame(master=frameFilter)
frameResult.columnconfigure(0, weight=10)
frameResult.columnconfigure(1, weight=1)
frameResult.columnconfigure(2, weight=1)
frameResult.columnconfigure(3, weight=1)

label1 = ctk.CTkLabel(master=frameResult, text="#RESULTS")
label1 = label1.grid(column=0, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)

btn10 = ctk.CTkButton(master=frameResult, text="10", command=setResult(10))
btn10.grid(column=1, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)

btn20 = ctk.CTkButton(master=frameResult, text="15", command=setResult(15))
btn20.grid(column=2, row=0,sticky=ctk.W+ctk.E, padx=10, pady=10)

btn30 = ctk.CTkButton(master=frameResult, text="20", command=setResult(20))
btn30.grid(column=3, row=0,sticky=ctk.W+ctk.E,padx=10, pady=10)


frameResult.grid(column=0, row=0)
frameFilter.grid(column=0, row=0)



root.mainloop()
'''

if __name__ == "__main__":
    
    gui = MyGUI()

    