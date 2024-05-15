import customtkinter as ctk
from ..action import bedsCommand
from ..action import bathsCommand

class BedsBathsFrame(ctk.CTkFrame):
    def __init__(self, root, tree, control, myfont):
        self.tree = tree
        self.control = control
        self.myfont = myfont
        super().__init__(master=root)
        
        for i in range(4):
            self.columnconfigure(i, weight=1)
            
        bedsLabel = ctk.CTkLabel(master=self, text="Beds", font=self.myfont)
        bedsLabel.grid(column=0, row=0, padx=10, pady=10, sticky='NSWE')
        
        beds_values = ["None","1","2","3+"]
        bedsButton = ctk.CTkSegmentedButton(master=self, 
                                            command=lambda x: bedsCommand(bedsButton, self.tree, self.control),  
                                            values=beds_values, corner_radius=150, 
                                            selected_color="#FF385C", 
                                            selected_hover_color="#d72545")
        bedsButton.set("None")
        bedsButton.grid(column=1, row=0, pady=10, sticky='NSWE')
    
        
        bathsLabel = ctk.CTkLabel(master=self, text="Baths", font=self.myfont)
        bathsLabel.grid(column=2, row=0, padx=10, pady=10, sticky='NSWE')

        baths_values = ["None","1","2","3+"]
        bathButton = ctk.CTkSegmentedButton(master=self, 
                                            command=lambda x: bathsCommand(bathButton,  self.tree, self.control), 
                                            values=baths_values, 
                                            corner_radius=150, 
                                            selected_color="#FF385C", 
                                            selected_hover_color="#d72545")
        
        bathButton.grid(column=3, row=0, pady=10, padx=10, sticky='NSWE')
        bathButton.set("None")
