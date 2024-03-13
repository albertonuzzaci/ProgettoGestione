import customtkinter as ctk
from ..action import setResult


class ResultFrame(ctk.CTkFrame):
    def __init__(self, root, control, myfont):
        self.control = control
        self.myfont = myfont
        super().__init__(master=root)
        
        for i in range(3):
            self.columnconfigure(i, weight=1)
            
        radioVar = ctk.StringVar(value="")
        
        btn10 = ctk.CTkRadioButton(master=self, text="10", variable=radioVar, font=self.myfont, command=lambda: setResult(10, self.tree,self.control),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn10.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')

        btn20 = ctk.CTkRadioButton(master=self, text="15",variable=radioVar,font=self.myfont,  command=lambda: setResult(15, self.tree, self.control),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn20.grid(column=1, row=0, padx=10, pady=10, sticky='NSWE')

        btn30 = ctk.CTkRadioButton(master=self, text="20", variable=radioVar, font=self.myfont, command=lambda: setResult(20, self.tree, self.control),hover_color=["#d72545", "#d72545"],fg_color= ["#FF385C", "#FF385C"])
        btn30.grid(column=2, row=0,padx=10, pady=10, sticky='NSWE')
        
        btn10.select(True)

        
