import customtkinter as ctk
from PIL import Image
import requests
from bs4 import BeautifulSoup
import os

class ImageFrame(ctk.CTkFrame):
    
    def __init__(self, root,linkAcc, id):
        self.id = id
        self.linkAcc = linkAcc
        
        super().__init__(master=root)
        self.columnconfigure(0, weight=1)
        

        self.downloadImages()
        
        for i, img in enumerate(os.listdir(f'./assets/{self.id}images')):       
            my_image = ctk.CTkImage(Image.open(f'./assets/{self.id}images/{img}'), text="", size=(300,200))
            button = ctk.CTkLabel(self, image=my_image)
            button.grid(column=i, row=0, sticky="nsew")

    def getImages(self):
        url = self.linkAcc
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        response = requests.request("GET", url, headers=headers, data={})
        soup = BeautifulSoup(response.text, 'html.parser')
        imagesLink = []
        for i in soup.find_all("picture", {"class":"dir dir-ltr"}):
            for k in i.findChildren("source"): 
                imagesLink.append(k.get('srcset')[0:k.get('srcset').find('?')])
        return set(imagesLink)
    
    def downloadImages(self):
        os.mkdir(f'./assets/{self.id}images')
        
        imagesLink = self.getImages()
        
        for c, img in enumerate(imagesLink):
            if c > 2:
                break
            img_data = requests.get(img).content
            with open(f'./assets/{self.id}images/{c}.jpg', "wb") as f:
                f.write(img_data)