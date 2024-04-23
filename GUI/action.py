from GUI.accomodationFrame import AccomodationFrame

def searchFunction(valueList, control):
    valueList.delete(*valueList.get_children())
    
    results = control.callSearch()
    print(results)
    for k,elem in results.items():
        valueList.insert("",'end', values=(str(k), elem[0],elem[1]))

def setResult(var, valueList, control):
    control.updateResult(var)
    searchFunction(valueList, control)

def updateDidYouMean(label, control):
    if(len(control.getSuggestion()) > 0):   
        label.configure(text=f"Did you mean \'{control.getSuggestion()}\'?", cursor="hand2")
    else:
        label.configure(text=f"Nothing to suggest.", cursor="")


def correctText(searchField, control):
    if(len(control.getSuggestion()) > 0):
        searchField.delete(0, 'end')
        searchField.insert(0,f"{control.getSuggestion()}")
        
    


def updateInputsearch(value, valueList, control):
    control.updateInputSearch(value)
    searchFunction(valueList, control)
    
def increase(lbl, valueList, control):
    lbl.configure(text=int(lbl.cget("text"))+1)
    control.updatePeople(int(lbl.cget("text")))
    #if(control.inputSearch != ""): 
    searchFunction(valueList, control)
    
def decrease(lbl, valueList, control):
    if(int(lbl.cget("text"))>0):
        lbl.configure(text=int(lbl.cget("text"))-1)
        control.updatePeople(int(lbl.cget("text"))) 
        #if(control.inputSearch != ""):
        searchFunction(valueList, control)
    
def onselect(evt, listbox, mainView):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        try:
            newTab = mainView.add(f'{selected_item.strip()[:10]}{"..." if len(selected_item)>10 else ""}')
        except ValueError:
            print("Pagina già aperta") # METTERSI D'ACCORDO SU COME GESTIRE IL CASO
        
def slider_ev(sliderValue, label, info, valueList, control):
    if info.cget("text")=="Price Max":
        control.updatePrice(round(sliderValue, 2))
    else:
        label.configure(text=f"{round(sliderValue,2)} ☆")
        control.updateScore(round(sliderValue, 2))
    searchFunction(valueList, control)
        
def changeLabel(value, label):
    if "€" in label.cget("text"):
        label.configure(text=f"{round(value,2)}€")
    else:
        label.configure(text=f"{round(value,2)}☆")
        

def neighToggle(checkbutton_var, checkbox, valueList, control):
    if checkbutton_var.get():
        control.updateNeighborhood(f"\"{checkbox.cget('text')}\"")
    else:
        control.removeNeighborhood(f"\"{checkbox.cget('text')}\"")
    searchFunction(valueList, control)
    
def sentimentToggle(checkbutton_var, checkbox, valueList, control):
    if checkbutton_var.get():
        control.addSentiment(f"{checkbox.cget('text')}")
    else:
        control.removeSentiment(f"{checkbox.cget('text')}")
    searchFunction(valueList, control)

def bedsCommand(button, valueList, control):
    if button.get() != "None":
        control.updateBeds(button.get())
    else:
        control.updateBeds()
    searchFunction(valueList, control)

def bathsCommand(button, valueList, control):
    
    if button.get() != "None":
        control.updateBaths(button.get())
    else:
        control.updateBaths()
    searchFunction(valueList, control)

def item_selected(mainView, valueList):
    for selectedItem in valueList.selection():
        item = valueList.item(selectedItem)
        record = item['values']
        try:
            newTab = mainView.add(str(record[0])+" "+record[1] if len(record[1])<15 else str(record[0])+" "+record[1][:15]+"...")
            newFrame = AccomodationFrame(newTab, record[0],record[1], mainView)
            newFrame.pack()
            newFrame.imgFrame.wait()
        except ValueError:
            mainView.set(str(record[0])+" "+record[1]  if len(record[1])<15 else str(record[0])+" "+record[1][:15]+"...")    