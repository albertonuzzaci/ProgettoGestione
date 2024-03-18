import customtkinter as ctk
from tkinter import ttk
import tkinter as tk   
from functools import reduce

class DescriptionFrame(ctk.CTkFrame):
	def __init__(self, root, desc, myfont):
		self.description=desc
		super().__init__(master=root)
		
		self.cleanText()
		
		self.textbox = ctk.CTkTextbox(self, width=930, height=85,wrap="word", fg_color="transparent")
		self.textbox.grid(row=0, column=1, sticky="nsew")
		self.textbox.insert("0.0",self.description)
		self.textbox.configure(state="disabled")
	
	def cleanText(self):
		char_to_replace = {'<br />':'\n', '<b>':'', '</b>':''}
		for k,v in char_to_replace.items():
			self.description = self.description.replace(k,v)
		

