import customtkinter as ctk
from PIL import Image
import io
import webbrowser
import urllib.request

class HostFrame(ctk.CTkFrame):
    
	def __init__(self, root, name, link, profile, myfont):
		self.name = name
		self.imageURL = link
		self.profileURL = profile

		super().__init__(master=root)

		for i in range(2):
			self.columnconfigure(i, weight=1)
			
		for i in range(2):
			self.rowconfigure(i, weight=1)
			
		titleFont=ctk.CTkFont(family="Montserrat", size=17, weight="bold", slant="italic", underline=True)

		labelTitleHost = ctk.CTkLabel(self, text='Host\n', font=titleFont, cursor="hand2")
		labelHost = ctk.CTkLabel(self, text=f'{self.name}\n', font=myfont, cursor="hand2")
		hostImage = ctk.CTkImage(Image.open(io.BytesIO(self.readImage(self.imageURL))), size=(100, 100))
		labelImage = ctk.CTkLabel(self, image=hostImage, text="")

		labelTitleHost.grid(row=0, column=0, sticky="s", padx=5, pady=(10,5))
		labelHost.grid(row=1, column=0, sticky="n", padx=5, pady=(0,5))
		labelImage.grid(row=0, rowspan=2, column=1, sticky="nsewn", padx=5, pady=10)

		labelHost.bind("<Button-1>", lambda e: self.callback(self.profileURL))
		labelTitleHost.bind("<Button-1>", lambda e: self.callback(self.profileURL))
         
    
	@staticmethod
	def readImage(img):
		with urllib.request.urlopen(img) as u:
			return u.read()
    
    
	@staticmethod
	def callback(url):
		webbrowser.open_new_tab(url)  
        
        

            

 

