import customtkinter as ctk

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