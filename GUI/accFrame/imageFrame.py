import customtkinter as ctk
from PIL import Image
import io
import requests
import urllib.request
from bs4 import BeautifulSoup

import threading
import ssl

ssl._create_default_https_context = ssl._create_unverified_context 

N_THREADS=3

class ImageFrame(ctk.CTkFrame):
    
    def __init__(self, root,linkAcc, id):
        self.id = id
        self.url = linkAcc
        self.imgDict={}
        self.images=[]
        
        super().__init__(master=root)
        for i in range(3):
            self.columnconfigure(i, weight=1)
            
        
        self.threads=[]
        
        imagesURL=self.getImages()
        emptyImage = ctk.CTkImage(Image.open("./assets/empty.png"),size=(300, 200))
        
        for i,img in enumerate(imagesURL):
            if i<N_THREADS:
                self.threads.append(threading.Thread(target = self.readImages, args = (img, i)))
                emptyLabel=ctk.CTkLabel(self, image=emptyImage, text="")
                emptyLabel.grid(column=i, row=1, sticky="nsew", padx=5, pady=(0,10))


        # imgLabel = ctk.CTkLabel(master=self, text="Show Images", font=ctk.CTkFont(family="Montserrat", size=15, weight="bold"),cursor="hand2")
        # imgLabel.bind("<Button-1>", lambda e: self.callback(imgs, imgLabel))
        # imgLabel.grid(row=0, column=0, sticky="W", padx=10, pady=10)  


    def readImages(self,img,i):

        with urllib.request.urlopen(img) as u:
            self.imgDict[i] = u.read()
            
        self.images.append(ctk.CTkImage(Image.open(io.BytesIO(self.imgDict[i])), size=(300,200)))
        my_img = ctk.CTkLabel(self, image=self.images.pop() , text="")
        my_img.grid(column=i, row=1, sticky="nsew", padx=5, pady=5)
            
    def getImages(self):
        url = self.url
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
    
    def wait(self):
        for i in range(N_THREADS):
            self.threads[i].start()
    
   
        
    # def downloadImages(self):
    #     os.mkdir(f'./assets/{self.id}images')
        
    #     imagesLink = self.getImages()
        
    #     for c, img in enumerate(imagesLink):
    #         if c > 2:
    #             break
    #         img_data = requests.get(img).content
    #         with open(f'./assets/{self.id}images/{c}.jpg', "wb") as f:
    #             f.write(img_data)
    

