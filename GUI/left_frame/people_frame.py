import customtkinter as ctk
from ..action import decrease, increase

class PeopleFrame(ctk.CTkFrame):
	def __init__(self, root, tree, control, myfont):
		self.control = control
		self.myfont = myfont
		self.tree = tree
		super().__init__(master=root)

		for i in range(3):
			self.columnconfigure(i, weight=1)
           
		valuePeopleLabel = ctk.CTkLabel(master=self, text="0", font=self.myfont)
		valuePeopleLabel.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

		btnPeopleMinus = ctk.CTkButton(master=self, text="-", font=self.myfont, command=lambda: decrease(valuePeopleLabel, self.tree, self.control), fg_color="#FF385C", hover_color="#d72545")
		btnPeopleMinus.grid(column=0, row=0,padx=10, pady=10, sticky='NSWE')

		btnPeoplePlus = ctk.CTkButton(master=self, text="+", font=self.myfont, command=lambda: increase(valuePeopleLabel, self.tree, self.control), fg_color="#FF385C", hover_color="#d72545")
		btnPeoplePlus.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')