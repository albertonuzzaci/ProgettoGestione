from tkintermapview import TkinterMapView
import customtkinter as ctk

class MapFrame(ctk.CTkFrame):
	def __init__(self, root, name, lat, long):
		self.lat = lat
		self.long = long
		self.name = name
  
		super().__init__(master=root)
  
		self.map = TkinterMapView(self, width=250, height=250)
       
		self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
		self.map.set_position(self.lat,self.long,marker=True, text=self.name)
		self.map.grid(row=0, column=0, padx=10,pady=10,sticky="nsew")
