import customtkinter as ctk
import json
from GUI.accFrame import *
import webbrowser

class AccomodationFrame(ctk.CTkFrame):
    
    def __init__(self, root, id, name, mView):
        self.name = name
        self.mView = mView
        self.id = id
        self.myfont = ctk.CTkFont(family="Montserrat", size=15) 
        super().__init__(master=root)

        with open(f'./dataset/json/{self.id}.json','r') as f:
            self.data = json.load(f)

        AccomodationFrame.addColumns(2, self)
        AccomodationFrame.addRows(10, self)
        
        lFrame = self.setupLeftFrame()
        lFrame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        
        btnClose= ctk.CTkButton(master=self, text="X", command=lambda: self.delete(), fg_color="#FF385C", hover_color="#d72545")
        btnClose.grid(row=9, column=0, sticky="NSEW", padx=10, pady=10)
    
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self)
        AccomodationFrame.addColumns(1, lFrame)
        
        nameLabel = ctk.CTkLabel(master=lFrame, text=f'{self.data['name']}', font=ctk.CTkFont(family="Montserrat", size=15, weight="bold"),cursor="hand2")
        nameLabel.bind("<Button-1>", lambda e: AccomodationFrame.callback(self.data['listing_url']))
        nameLabel.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        
        imgFrame = imageFrame.ImageFrame(lFrame, self.data["listing_url"], self.data["id"])
        imgFrame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        return lFrame
    
    def delete(self):
        self.mView.delete(self.name)
    
    
    @staticmethod
    def callback(url):
        webbrowser.open_new_tab(url)    
    
    @staticmethod
    def addColumns(ncolumn, obj):
        for i in range(ncolumn):
            obj.columnconfigure(i, weight=1)
    
    @staticmethod
    def addRows(nrow, obj):
        for i in range(nrow):
            obj.rowconfigure(i, weight=1)
