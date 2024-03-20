import customtkinter as ctk
from ..action import changeLabel, slider_ev
import json

class PriceFrame(ctk.CTkFrame):
    def __init__(self, root, tree, control, myfont, priceLabel):
        self.tree = tree
        self.control = control
        self.myfont = myfont
        super().__init__(master=root)
        
        for i in range(2):
            self.columnconfigure(i, weight=1)
            
        
            
        with open('./dataset/information.json', "r") as f:
            data = json.load(f)
            min = round(data["min"], 2)
            max = round(data["max"], 2)
        labelPriceSlider = ctk.CTkLabel(master=self, text=f"{round(max, 2)}€", font=self.myfont)
        priceSlider = ctk.CTkSlider(master=self, 
                                    command=lambda value: changeLabel(value,labelPriceSlider),
                                    from_=float(min), 
                                    to=float(max), 
                                    button_hover_color=["#FF385C", "#FF385C"], 
                                    button_color=["#d72545", "#d72545"])
        
        priceSlider.bind("<ButtonRelease-1>", command=lambda event: slider_ev(priceSlider.get(), 
                                                                            labelPriceSlider, 
                                                                            priceLabel, 
                                                                            self.tree,
                                                                            self.control))

        priceSlider.grid(column=0, row=0,padx=10, pady=20, sticky='NSWE')
        labelPriceSlider.grid(column=1, row=0, sticky='NSWE')
        priceSlider.set(float(max))
        
