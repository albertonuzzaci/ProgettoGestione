import customtkinter as ctk
import json
from gui.acc_frame import image_frame, info_frame, map_frame, review_frame, description_frame, host_frame
import webbrowser
from PIL import Image

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
        nameLabel.bind("<Button-1>", lambda e: self.callback(self.data["listing_url"]))  #self.link
        nameLabel.grid(row=0, column=0, sticky="W", padx=10, pady=10)

       
        icon = ctk.CTkImage(Image.open("./assets/xIcon.png"),size=(20, 20))

        btnClose= ctk.CTkButton(self, image=icon, command=lambda: self.delete(), text="", fg_color="#FF385C", hover_color="#d72545")
        btnClose.grid(row=0, column=1, sticky="E", padx=10, pady=10)
        
        lFrame = self.setupLeftFrame()
        lFrame.grid(row=1, column=0, rowspan=2, sticky="NEW", padx=10, pady=10)
        rFrame = self.setupRightFrame()
        rFrame.grid(row=1, column=1, rowspan=2, sticky="SEW", padx=10, pady=10)
        
        reviewF = review_frame.ReviewFrame(self, self.data["reviews"])
        reviewF.grid(row=3, column=0, columnspan=2, sticky="SEW", padx=10, pady=10)
    # def setupTitleFrame(self):
    #     tFrame = ctk.CTkFrame(self)s
    #     return tFrame
  
    def setupLeftFrame(self):
        lFrame = ctk.CTkFrame(self)
        AccomodationFrame.addColumns(2, lFrame)
        AccomodationFrame.addRows(3, lFrame)
      
        self.imgFrame = image_frame.ImageFrame(lFrame, self.data["listing_url"], self.data["id"])
        self.imgFrame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        infoF = info_frame.InfoFrame(lFrame, self.data["property_type"],self.data["room_type"], self.data["beds"], self.data["bathrooms"],self.myfont)
        infoF.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        rateF = info_frame.RateFrame(lFrame, self.data["price"], self.data["review_scores_rating"],self.data["numbers_of_review"], self.data["accommodates"], self.myfont)
        rateF.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        descF = description_frame.DescriptionFrame(lFrame, self.data["description"], self.myfont)
        descF.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        return lFrame

    def setupRightFrame(self):
        rFrame = ctk.CTkFrame(self)
        AccomodationFrame.addColumns(1, rFrame)
        
        map = map_frame.MapFrame(rFrame, self.name, self.data["latitude"],self.data["longitude"])
        map.grid(row=1, column=1,sticky="nsew", padx=10, pady=10)
        
        hostF = host_frame.HostFrame(rFrame,self.data["host_name"], self.data["host_picture_url"], self.data["host_url"], self.myfont)
        hostF.grid(row=2, column=1,sticky="nsew", padx=10, pady=10)
        return rFrame

    def delete(self):
        self.mView.delete(str(self.id)+" "+self.name if len(self.name)<15 else str(self.id)+" "+self.name[:15]+"...")

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
