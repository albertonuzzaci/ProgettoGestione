import customtkinter as ctk
from ..action import slider_ev, changeLabel

class ScoreFrame(ctk.CTkFrame):
    def __init__(self, root, tree, control, myfont, scoreLabel):
        self.tree = tree
        self.control = control
        self.myfont = myfont
        super().__init__(master=root)
        
        for i in range(2):
            self.columnconfigure(i, weight=1)

    
        labelScoreSlider = ctk.CTkLabel(master=self, text="0☆", font=self.myfont)
        scoreSlider = ctk.CTkSlider(master=self, 
                                    from_=0, to=5, 
                                    command=lambda value: changeLabel(value,labelScoreSlider),
                                    button_hover_color=["#FF385C", "#FF385C"], 
                                    button_color=["#d72545", "#d72545"])
    
        scoreSlider.bind("<ButtonRelease-1>", command=lambda event: slider_ev(scoreSlider.get(), 
                                                                            labelScoreSlider, 
                                                                            scoreLabel, 
                                                                            self.tree,
                                                                            self.control))

        scoreSlider.grid(column=0, row=0,padx=10, pady=20, sticky='NSWE')
        scoreSlider.set(0)

        labelScoreSlider.grid(column=1, row=0, sticky='NSWE')