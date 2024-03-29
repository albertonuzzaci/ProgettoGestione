import tkinter as tk    
from tkinter import ttk
import customtkinter as ctk

import json
from GUI.action import *
from GUI.leftFrame import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MyGUI():
    def __init__(self, control):
        self.control = control
        self.root = ctk.CTk()
        self.root.after(1000, self.update)
        
        self.root.geometry("1325x750")
        
        self.root.resizable(False, False)

        self.myfont = ctk.CTkFont(family="Montserrat", size=15) # PER CAMBIARE FONT
        
        self.mainView =  self.setupTabView()
        searchTab = self.mainView.add("Search Tab") # tab principale per effettuare la ricerca, contiene il mainFrame
    
        self.mainFrame = ctk.CTkFrame(searchTab, corner_radius=10)
        self.mainFrame.pack(pady=20, padx=15, fill="both")

        MyGUI.addColumns(2, self.mainFrame)
        
        
        self.rightFrame = self.setupRightFrame()
        self.rightFrame.grid(column=1, row=0, sticky='nsew',padx=30, pady=10)
        
        self.leftFrame = self.setupLeftFrame()
        self.leftFrame.grid(column=0, row=0, sticky='nsew', padx=30, pady=10)
        
        self.root.mainloop()

    def update(self):
        if self.control.inputSearch != self.searchField.get():
            self.control.updateInputSearch(self.searchField.get())
            searchFunction(self.tree, self.control)
            updateDidYouMean(self.didYouMeanLabel, self.control)
        self.root.after(100, self.update)
        
    def setupTabView(self):
        mainView = ctk.CTkTabview(self.root,
                                  segmented_button_selected_color="#FF385C",
                                  segmented_button_selected_hover_color="#d72545",
                                  segmented_button_unselected_hover_color="#d72545",
                                  anchor='W' # Parametro da modificare in base alle preferenze, posizione del gestore delle tab
                                  )
        mainView.pack(pady=20, padx=10, fill="both", expand=True)
        return mainView

    def setupRightFrame(self):

        rFrame = ctk.CTkFrame(self.mainFrame, corner_radius=10)
        
        #MyGUI.addRows(4, rFrame)
        rFrame.rowconfigure(0, weight=30)
        rFrame.rowconfigure(1, weight=1)
        rFrame.rowconfigure(2, weight=30)
        rFrame.rowconfigure(3, weight=30)
        
        #-------------SEARCH----------------
        self.searchField = ctk.CTkEntry(master=rFrame, placeholder_text="Search destinations...", font=('Roboto', 18))
        self.searchField.grid(column=0, row=0, sticky='nsew', pady=(10,0), padx=10)
        
        
        #-------------RESULTS----------------
        treeFrame = ctk.CTkFrame(master=rFrame)
        MyGUI.addColumns(2,treeFrame)
        
        s = ttk.Style()
        columns = ('id','accomodation', 'price')
        self.tree = ttk.Treeview(master=treeFrame, selectmode="extended", columns=columns, show='')
        self.tree["displaycolumns"] = ['accomodation', 'price']
        self.tree.column("accomodation", minwidth=500, width=500, stretch=False)
        self.tree.column("price", minwidth=0, width=100, stretch=False)
        s.theme_use("clam")
        s.configure('Treeview', rowheight=40, fieldbackground='#333333', background='#333333', foreground="#DCE4EE", font=("Roboto",15))    

        self.tree.bind('<<TreeviewSelect>>', lambda x: item_selected(mainView=self.mainView, valueList=self.tree))
        self.tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(master=treeFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='nswe')
        
        treeFrame.grid(row=3, column=0)
        
        
        #-------------SENTIMENT--------------

        sentimentFrame = scrollCheckBox.ScrollableCheckBoxFrame(master=rFrame,
                                                                item_list=sorted(["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]), 
                                                                tree=self.tree,
                                                                orientation="horizontal",
                                                                control=self.control,
                                                                height=30,
                                                                fg_color= "#333333")

        sentimentFrame.grid(column=0, row=2, sticky='nsew')
        
        #----------DID YOU MEAN--------------
        self.didYouMeanLabel = ctk.CTkLabel(
            master=rFrame,
            text="Type something for suggetions...",
            anchor="w",
            text_color="#a3a2a0",
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold")
        )
        self.didYouMeanLabel.bind("<Button-1>", lambda v: correctText(self.searchField, self.control))
        
        self.didYouMeanLabel.grid(column=0, row=1, sticky="ew", padx=(18,0))

        return rFrame
    
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self.mainFrame)
        MyGUI.addRows(7, lFrame)
        MyGUI.addColumns(3, lFrame)
        #---------------RESULT--------------------
        resFrame = resultFrame.ResultFrame(lFrame, self.tree, self.control, self.myfont)
        resLabel = ctk.CTkLabel(master=lFrame, text="#Results", font=self.myfont)
        resLabel.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')
        resFrame.grid(column=1, row=0, padx=10, pady=10, sticky="NSWE")

        #-------------ACCOMODATES----------------
        accFrame = peopleFrame.PeopleFrame(lFrame, self.tree, self.control, self.myfont)
        
        peopleLabel = ctk.CTkLabel(master=lFrame, text="People", font=self.myfont)
        peopleLabel.grid(column=0, row=1, padx=10, pady=10, sticky='NSWE')
      
        accFrame.grid(column=1, row=1, padx=10, pady=10, sticky="NSWE")

        #---------------PRICE--------------------        
        priceLabel = ctk.CTkLabel(master=lFrame, text="Price Max", font=self.myfont)
        priceLabel.grid(column=0, row=2, padx=10, pady=20, sticky='NSWE')
        prFrame = priceFrame.PriceFrame(lFrame, self.tree, self.control, self.myfont, priceLabel)
        prFrame.grid(column=1, row=2, padx=10, pady=10, sticky="NSWE")
        
         #---------------SCORE--------------------
        scoreLabel = ctk.CTkLabel(master=lFrame, text="Score Min", font=self.myfont)
        scoreLabel.grid(column=0, row=3, padx=10, pady=20, sticky='NSWE')
        scFrame = scoreFrame.ScoreFrame(lFrame, self.tree, self.control, self.myfont, scoreLabel)
        scFrame.grid(column=1, row=3, padx=10, pady=10, sticky="NSWE")
        
        #--------------NEIGH-----------------------
        neighLabel = ctk.CTkLabel(master=lFrame, text="Neighborhood", font=self.myfont)
        neighLabel.grid(column=0, row=4, padx=5, pady=20, sticky='NSWE')
        
        with open("./dataset/information.json", "r") as f:
            data = json.load(f)
            neighFrame = scrollCheckBox.ScrollableCheckBoxFrame(master=lFrame, 
                                                                height=2, 
                                                                width=200, 
                                                                item_list=sorted(data["neighbourhood"].keys()), 
                                                                tree=self.tree,
                                                                control=self.control)

        neighFrame.grid(column=1, row=4,  padx=15, pady=15, sticky='NSWE')
        
        #---------------BEDS & BATHS--------------------
        bbFrame = bedsBathsFrame.BedsBathsFrame(lFrame, self.tree, self.control, self.myfont)
        bbFrame.grid(column=0,columnspan=2, row=5, padx=10, pady=10, sticky="NSWE")    
        
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