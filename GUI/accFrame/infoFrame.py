import customtkinter as ctk
import math
from PIL import ImageTk, Image

class InfoFrame(ctk.CTkFrame):
	def __init__(self, root, propType, roomType, beds, baths, myfont):
		self.propType = propType
		self.roomType = roomType
		self.beds = beds
		self.baths = int(baths) if baths==int(baths) else baths
  
		super().__init__(master=root)
		
		for i in range(4):
			self.columnconfigure(i, weight=1)
   
		for i in range(2):
			self.rowconfigure(i, weight=1)

		titleFont=ctk.CTkFont(family="Montserrat", size=17, weight="bold", slant="italic", underline=True)
  	
		labelTitleBaths = ctk.CTkLabel(self, text='Bathrooms\n', font=titleFont)
		labelTitleRooms = ctk.CTkLabel(self, text='Rooms\n', font=titleFont)
		labelTitlePT = ctk.CTkLabel(self, text='Property type\n', font=titleFont)
		labelTitleRT = ctk.CTkLabel(self, text='Rooms type\n', font=titleFont)

		
		labelBaths = ctk.CTkLabel(self, text=f'{self.baths}', font=myfont)
		labelRooms= ctk.CTkLabel(self, text=f'{self.beds}', font=myfont)
		labelPT = ctk.CTkLabel(self, text=f'{self.propType}', font=myfont)
		labelRT = ctk.CTkLabel(self, text=f'{self.roomType}', font=myfont)
	
		labelTitlePT.grid(row=0, column=0, sticky="s", padx=5, pady=(5,0))
		labelTitleRT.grid(row=0, column=1, sticky="s", padx=5, pady=(5,0))
		labelTitleRooms.grid(row=0, column=2, sticky="s", padx=5, pady=(5,0))
		labelTitleBaths.grid(row=0, column=3, sticky="s", padx=5, pady=(5,0))
  
		labelRT.grid(row=1, column=1, sticky="n", padx=5, pady=(0,5))
		labelPT.grid(row=1, column=0, sticky="n", padx=5, pady=(0,5))
		labelRooms.grid(row=1, column=2, sticky="n", padx=5, pady=(0,5))
		labelBaths.grid(row=1, column=3, sticky="n", padx=5, pady=(0,5))
  
class RateFrame(ctk.CTkFrame):
	def __init__(self, root, price,score, nReviews, guests, myfont):
		self.guests=guests
		self.price=price
		self.score = score if not math.isnan(score) else "?"
		self.reviews=nReviews
		super().__init__(master=root)
  
		for i in range(4):
			self.columnconfigure(i, weight=1)
   
		for i in range(2):
			self.rowconfigure(i, weight=1)
		
		titleFont=ctk.CTkFont(family="Montserrat", size=17, weight="bold")
		labelScore = ctk.CTkLabel(self, text=f'{self.score}/5.0 ☆', font=titleFont)
		labelReviews = ctk.CTkLabel(self, text=f'{int(self.reviews)} reviews', font=myfont)
		labelNight = ctk.CTkLabel(self, text=f'per night', font=myfont)
		labelPrice = ctk.CTkLabel(self, text=f'{self.price}€', font=titleFont)
  
		guestImage = ctk.CTkImage(dark_image=Image.open("./assets/person.png"),size=(20, 20))
  
		labelGuests = ctk.CTkLabel(self, text=f'x{int(self.guests)} ', image=guestImage, font=myfont, compound="right")
		labelScore.grid(row=0, column=0, sticky="e", padx=5, pady=5)
		labelReviews.grid(row=0, column=1, sticky="w", padx=5, pady=5)
		labelPrice.grid(row=1, column=0, sticky="e", padx=5, pady=5)
		labelNight.grid(row=1, column=1, sticky="w")
		labelGuests.grid(row=0, rowspan=2, column=2, sticky="nsew", padx=5, pady=5)