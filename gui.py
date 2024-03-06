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

default_font_size = config_data["GUI"]["FONTSIZE"]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def cerca(campo, lista):
    print(campo)
    print(lista)
    lista.insert("end", campo)

def setResult(var):
    print(f"set result {var}")

def onselect(evt):
    pass

def slider_event(value):
    print(value)

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
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

        self.mainFrame = ctk.CTkFrame(self.root)

        self.mainFrame.pack(pady=20, padx=60, fill="both", expand=True)
        MyGUI.addColumns(2, self.mainFrame)
        
        self.rightFrame = self.setupRightFrame()
        self.rightFrame.grid(column=1, row=0)
        
        self.leftFrame = self.setupLeftFrame()
        self.leftFrame.grid(column=0, row=0)
        
        self.root.mainloop()
    
    def setupRightFrame(self):
        hotel = [f"Elem{x}\n\n" for x in range(15)]
        hotel_selezionato = tkinter.StringVar(value=hotel)
        
        rFrame = ctk.CTkFrame(self.mainFrame)
        MyGUI.addColumns(2, rFrame)
        
        searchField = ctk.CTkEntry(master=rFrame, width=400, placeholder_text="Search destinations...")
        listbox = CTkListbox(master=rFrame, listvariable=hotel_selezionato, height=500)
        listbox.bind('<<ListboxSelect>>', onselect)

        searchButton = ctk.CTkButton(master=rFrame, text="SEARCH", command = lambda: cerca(searchField.get(), listbox))
        
        searchField.grid(column=0, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        searchButton.grid(column=1, row=0, sticky=ctk.W+ctk.E, padx=10, pady=10)
        listbox.grid(column=0,columnspan=2, row=1, sticky=ctk.W+ctk.E, padx=10, pady=20)
        return rFrame
    
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self.mainFrame)
        MyGUI.addRows(7, lFrame)
        
        #---------------RESULT--------------------
        frameResult = ctk.CTkFrame(master=lFrame)
        MyGUI.addColumns(4, frameResult)
        
        resLabel = ctk.CTkLabel(master=frameResult, text="#RESULTS", font=("Roboto", default_font_size))
        resLabel.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')
        
        radioVar = ctk.StringVar(value="")
        
        btn10 = ctk.CTkRadioButton(master=frameResult, text="10", variable=radioVar, font=("Roboto", default_font_size), command=lambda: setResult(10))
        btn10.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btn20 = ctk.CTkRadioButton(master=frameResult, text="15",variable=radioVar,font=("Roboto", default_font_size),  command=lambda: setResult(15))
        btn20.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')

        btn30 = ctk.CTkRadioButton(master=frameResult, text="20", variable=radioVar, font=("Roboto", default_font_size), command=lambda: setResult(20))
        btn30.grid(column=3, row=0,padx=10, pady=10, sticky='NSWE')
        frameResult.grid(column=0, row = 0, sticky='NSWE')
       
        #---------------PRICE--------------------
        framePrice = ctk.CTkFrame(master=lFrame)
        MyGUI.addColumns(2, framePrice)
        
        priceLabel = ctk.CTkLabel(master=framePrice, text="PRICE", font=("Roboto", default_font_size))
        priceLabel.grid(column=0, row=0, padx=10, pady=20, sticky='NSWE')
        
        slider = ctk.CTkSlider(master=framePrice, from_=0, to=100 ,command=slider_event)

        slider.grid(column=1, row=0,padx=10, pady=20, sticky='NSWE')
        
        framePrice.grid(column=0, row = 1, sticky='NSWE')

        #--------------NEIGH-----------------------
        neighFrame = ctk.CTkFrame(master=lFrame)
        MyGUI.addColumns(1, neighFrame)
        neighLabel = ctk.CTkLabel(master=neighFrame, text="NEIGHBORHOOD", font=("Roboto", default_font_size))
        neighLabel.grid(column=0, row=0, padx=10, pady=20, sticky='NSWE')

        scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=neighFrame, height=2, width=200, item_list=[f"item {i}" for i in range(50)])
        scrollable_checkbox_frame.grid(column=1, row=0,  padx=15, pady=15, sticky='NSWE')
        
        neighFrame.grid(column=0, row=2, sticky='NSWE') 
            
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

    