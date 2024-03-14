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
        AccomodationFrame.addRows(5, self)
        
        nameLabel = ctk.CTkLabel(self, text=f'{self.name}', font=ctk.CTkFont(family="Montserrat", size=25, weight="bold"),cursor="hand2")
        nameLabel.bind("<Button-1>", lambda e: self.callback(self.link))
        nameLabel.grid(row=0, column=0, sticky="W", padx=10, pady=10)

        btnClose= ctk.CTkButton(self, text="X", command=lambda: self.delete(), fg_color="#FF385C", hover_color="#d72545")
        btnClose.grid(row=0, column=1, sticky="E", padx=10, pady=10)
        
        lFrame = self.setupLeftFrame()
        lFrame.grid(row=1, column=0, rowspan=2, sticky="NSEW", padx=10, pady=10)
        rFrame = self.setupRightFrame()
        rFrame.grid(row=1, column=1, rowspan=2, sticky="NSEW", padx=10, pady=10)
        
    # def setupTitleFrame(self):  
    #     tFrame = ctk.CTkFrame(self)
        
    #     return tFrame
  
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self)
        AccomodationFrame.addColumns(1, lFrame)
        AccomodationFrame.addRows(2, lFrame)
        
              
        imgFrame = imageFrame.ImageFrame(lFrame, self.data["listing_url"], self.data["id"])
        imgFrame.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)
        iFrame = infoFrame.InfoFrame(lFrame, self.data["property_type"],self.data["room_type"], self.data["bedrooms"], self.data["bathrooms"], self.myfont)
        iFrame.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)
        
        return lFrame
    
    def setupRightFrame(self):
        rFrame = ctk.CTkFrame(self)
        AccomodationFrame.addColumns(1, rFrame)
                
        map = mapFrame.MapFrame(rFrame, self.name, self.data["latitude"],self.data["longitude"])
        map.grid(row=1, column=1,sticky="nsew", padx=10, pady=10)
          
        #hostF = hostFrame.HostFrame(rFrame,self.data["host_name"], self.data["host_picture_url"], self.data["host_url"], self.myfont)
        #hostF.grid(row=2, column=1,sticky="nsew", padx=10, pady=10)
        return rFrame
    
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
