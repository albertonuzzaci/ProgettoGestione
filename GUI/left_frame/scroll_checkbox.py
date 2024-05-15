import customtkinter as ctk
from GUI.action import neighToggle
from GUI.action import sentimentToggle
import tkinter as tk

class ScrollableCheckBoxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, tree, item_list, control, orientation="vertical", **kwargs):
        
        self.myorientation = orientation
        
        if self.myorientation == "horizontal":
            super().__init__(master, orientation="horizontal", **kwargs)
        else:
            super().__init__(master, **kwargs)
        
        self.tree=tree
        self.control = control
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbutton_var = tk.IntVar()
        checkbox = ctk.CTkCheckBox(self, text=item, hover_color="#d72545",fg_color= [ "gray90","#FF385C"], variable=checkbutton_var)
        if self.myorientation == "vertical":
            checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="nsew")
            checkbox.configure(command=lambda : neighToggle(checkbutton_var, checkbox, self.tree, self.control))
        else:
            checkbox.pack(side="left")
            checkbox.configure(command=lambda : sentimentToggle(checkbutton_var, checkbox, self.tree, self.control))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox for checkbox in self.checkbox_list if checkbox.get() == 1]
    