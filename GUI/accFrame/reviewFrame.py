import customtkinter as ctk
from tkinter import ttk
import tkinter as tk   

class ReviewFrame(ctk.CTkFrame):
	def __init__(self, root, reviews):
		self.reviewsList=reviews
		super().__init__(master=root)
		self.cleanText()
		self.textbox = ctk.CTkTextbox(self, width=1260, height=150,wrap="word", fg_color="transparent")
		self.textbox.grid(row=0, column=0, sticky="nsew")
		self.textbox.insert("0.0",self.createReviews())
		self.textbox.configure(state="disabled")

	def createReviews(self):
		s=""
		for review in self.reviewsList:
			s+=review["name"]+"\n"+review["date"]+"\n"+review["review"]+"\n\n"
		return s

	def cleanText(self):
		char_to_replace = {'<br/>':'\n', '<b>':'', '</b>':''}
		for k,v in char_to_replace.items():
			for review in self.reviewsList:
				review["review"] = review["review"].replace(k,v)