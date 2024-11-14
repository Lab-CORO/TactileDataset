import tkinter
import tkinter.messagebox
import customtkinter
import os
import subprocess
from PIL import Image
import glob
import re
import pandas as pd
from functools import partial

dataset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dataset")
datatset_files= sorted(glob.glob(dataset_path + "/*.csv"))
Data_real = pd.read_csv(dataset_path + "/Flat_Real_Abaqus.csv")
Data_Simulation = pd.read_csv(dataset_path + "/Flat_Simulation_Abaqus.csv")

Data_real_Curved = pd.read_csv(dataset_path + "/Curved_Real_Abaqus.csv")
Data_Simulation_Curved = pd.read_csv(dataset_path + "/Curved_Simulation_Abaqus.csv")


############################################ Flat
Different_Path = Data_Simulation[['Path']].drop_duplicates().reset_index(drop=True)
Different_Path = Different_Path['Path'].tolist()

Different_names = []
Images_names = []

for followPathcop in Different_Path:
    guiones=[pos for pos, char in enumerate(followPathcop) if char == '/']
    capital = [pos for pos, char in enumerate(followPathcop[0:guiones[0]]) if char.isupper()]
    
    if len(capital) > 1:
        # name_partial =followPathcop[0:capital[1]] + ' ' + followPathcop[capital[1]:guiones[0]]
        Images_names.append(followPathcop[0:guiones[0]])
        Different_names.append(followPathcop[0:capital[1]] + ' ' + followPathcop[capital[1]:guiones[0]])
    else:
        # print(followPathcop[0:guiones[0]], guiones)
        Images_names.append(followPathcop[0:guiones[0]])
        Different_names.append(followPathcop[0:guiones[0]])

Images_names = list(dict.fromkeys(Images_names))
Different_names = list(dict.fromkeys(Different_names))
Images_names.sort()
Different_names.sort()
############################################ Curved
Different_Path_Curved = Data_Simulation_Curved[['Path']].drop_duplicates().reset_index(drop=True)
Different_Path_Curved = Different_Path_Curved['Path'].tolist()

Different_names_Curved = []
Images_names_Curved = []

for followPathcop_Curved in Different_Path_Curved:
    guiones_Curved=[pos for pos, char in enumerate(followPathcop_Curved) if char == '/']
    capital_Curved = [pos for pos, char in enumerate(followPathcop_Curved[0:guiones_Curved[0]]) if char.isupper()]
    
    if len(capital_Curved) > 1:
        # name_partial =followPathcop[0:capital[1]] + ' ' + followPathcop[capital[1]:guiones[0]]
        Images_names_Curved.append(followPathcop_Curved[0:guiones_Curved[0]])
        Different_names_Curved.append(followPathcop_Curved[0:capital_Curved[1]] + ' ' + followPathcop_Curved[capital_Curved[1]:guiones_Curved[0]])
    else:
        # print(followPathcop_Curved[0:guiones_Curved[0]], guiones_Curved)
        Images_names_Curved.append(followPathcop_Curved[0:guiones_Curved[0]])
        Different_names_Curved.append(followPathcop_Curved[0:guiones_Curved[0]])
Images_names_Curved = list(dict.fromkeys(Images_names_Curved))
Different_names_Curved = list(dict.fromkeys(Different_names_Curved))
Images_names_Curved.sort()
Different_names_Curved.sort()

Dataset_added=[]

global phrase_to_search
phrase_to_search = 'Empty'

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def startfile(filename):
  try:
    os.startfile(filename)
  except:
    subprocess.Popen(['xdg-open', filename])

class ToplevelWindowSucess(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("320x240")
        self.title("Dataset created")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.label_indenter = customtkinter.CTkLabel(self, text="   Dataset created successfully.", fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_indenter.grid(row=1, column=2,  padx=(22, 2), pady=(15, 2))   
        self.image_indenter = customtkinter.CTkLabel(self, text="", 
                                                image=  customtkinter.CTkImage(Image.open(os.path.join(image_path, "Sucess" + ".png")), size=(170, 170)))
        self.image_indenter.grid(row=3, column=2, padx=(35, 20), pady=(2, 2))

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("320x380")
        self.title("Define data")
        # print(phrase_to_search)
        # print(Different_Path)
        row_pos = 2
        self.label_test_t= customtkinter.CTkLabel(self, text="Tests available", fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_test_t.grid(row=0, column=2,  padx=(20, 2), pady=(2, 2))
        item_total_test = 0
        for item in Different_Path:
            if isinstance(item, str) and re.search(phrase_to_search, item):
                # print(item)
                globals()['self.' + item] = customtkinter.CTkCheckBox(self, text=item, onvalue=item, offvalue="off", font=customtkinter.CTkFont(size=14, weight="bold"))
                globals()['self.' + item].grid(row=row_pos, column=1, padx=(7, 5), pady=(7, 5))
                
                temporal_simulation = Data_Simulation[Data_Simulation['Path'] == item]
                row, col = temporal_simulation.shape
                item_total_test = item_total_test + round(row/57)
                self.label_test = customtkinter.CTkLabel(self, text=str(round(row/57)), fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
                self.label_test.grid(row=row_pos, column=2,  padx=(20, 2), pady=(2, 2))
                row_pos += 1
            row_pos += 1
                # break
        globals()['self.AddALL'] = customtkinter.CTkCheckBox(self, text='Add All', onvalue=item, offvalue="off", font=customtkinter.CTkFont(size=14, weight="bold"))
        globals()['self.AddALL'].grid(row=row_pos, column=1, padx=(7, 5), pady=(15, 15))
        self.label_test = customtkinter.CTkLabel(self, text=str(round(item_total_test)), fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_test.grid(row=row_pos, column=2,  padx=(20, 2), pady=(2, 2))
        row_pos += 1
        self.Add_to = customtkinter.CTkButton(self, command=self.Add_data, width = 140, text="Add tests")
        self.Add_to.grid(row=row_pos, column=1, padx=(2, 2), pady=(2, 2))
        self.protocol("WM_DELETE_WINDOW", self.closed)

    def Add_data(self):
        seleccionados =[]
        self.Add_to.configure(state="disabled")
        if globals()['self.AddALL'].get() != "off":
            for index, item in enumerate(Different_Path):
                if isinstance(item, str) and re.search(phrase_to_search, item):
                    seleccionados.append(index)
                    Dataset_added.append(item)
                    app.textbox.insert("0.0", item + " \n")
            globals()['self.' + 'addIndenter_' + phrase_to_search].configure(state = 'disabled')
        else:
            for index, item in enumerate(Different_Path):
                if isinstance(item, str) and re.search(phrase_to_search, item):
                    if globals()['self.' + item].get() != "off":
                        # print(f"The sentence containing is at index '{index}'!")
                        seleccionados.append(index)
                        Dataset_added.append(item)
                        app.textbox.insert("0.0", item + " \n")
        seleccionados.sort(reverse = True)
        for index in seleccionados:
            del Different_Path[index]
        app.Generate_Data.configure(state="enabled")
        self.destroy()
            
    def closed(self):
        print("I've been closed!")
        self.destroy()
        # print(locals()[0])

class toplevel_window_curved(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x380")
        self.title("Define data")
        # print(phrase_to_search)
        # print(Different_Path)
        row_pos =1 
        self.label_test_t= customtkinter.CTkLabel(self, text="Tests available", fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_test_t.grid(row=0, column=2,  padx=(20, 2), pady=(2, 2))
        item_total_test = 0
        for item in Different_Path_Curved:
            if isinstance(item, str) and re.search(phrase_to_search, item):
                # print(item)
                globals()['self.' + item] = customtkinter.CTkCheckBox(self, text=item, onvalue=item, offvalue="off", font=customtkinter.CTkFont(size=14, weight="bold"))
                globals()['self.' + item].grid(row=row_pos, column=1, padx=(7, 5), pady=(7, 5))
                
                temporal_simulation = Data_Simulation_Curved[Data_Simulation_Curved['Path'] == item]
                row, col = temporal_simulation.shape
                item_total_test = item_total_test + round(row/57)
                self.label_test = customtkinter.CTkLabel(self, text=str(round(row/57)), fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
                self.label_test.grid(row=row_pos, column=2,  padx=(20, 2), pady=(2, 2))
                row_pos += 1
                # break
        globals()['self.AddALL'] = customtkinter.CTkCheckBox(self, text='Add All', onvalue=item, offvalue="off", font=customtkinter.CTkFont(size=14, weight="bold"))
        globals()['self.AddALL'].grid(row=row_pos, column=1, padx=(7, 5), pady=(15, 15))
        self.label_test = customtkinter.CTkLabel(self, text=str(round(item_total_test)), fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
        self.label_test.grid(row=row_pos, column=2,  padx=(20, 2), pady=(2, 2))
        row_pos += 1
        self.Add_to = customtkinter.CTkButton(self, command=self.Add_data, width = 140, text="Add tests")
        self.Add_to.grid(row=row_pos, column=1, padx=(2, 2), pady=(20, 2))
        self.protocol("WM_DELETE_WINDOW", self.closed)

    def Add_data(self):
        seleccionados =[]
        self.Add_to.configure(state="disabled")

        if globals()['self.AddALL'].get() != "off":
            for index, item in enumerate(Different_Path_Curved):
                if isinstance(item, str) and re.search(phrase_to_search, item):
                    seleccionados.append(index)
                    Dataset_added.append(item)
                    app.textbox.insert("0.0", item + " \n")
            globals()['self.' + 'addIndenter_' + phrase_to_search].configure(state = 'disabled')
        else:
            for index, item in enumerate(Different_Path_Curved):
                if isinstance(item, str) and re.search(phrase_to_search, item):
                    if globals()['self.' + item].get() != "off":
                        seleccionados.append(index)
                        Dataset_added.append(item)
                        app.textbox.insert("0.0", item + " \n")
        seleccionados.sort(reverse = True)
        for index in seleccionados:
            del Different_Path_Curved[index]
        app.Generate_Data.configure(state="enabled")
        self.destroy()

    def closed(self):
        print("I've been closed!")
        self.destroy()

class Frame_Flat(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window = None

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        indenter_number = 1
        row = 1
        column = 1
        for Indenter_name, Image_name in zip(Different_names, Images_names):
            self.label_indenter = customtkinter.CTkLabel(self, text=Indenter_name, fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_indenter.grid(row=row, column=column,  padx=(2, 2), pady=(15, 2))    
            self.image_indenter = customtkinter.CTkLabel(self, text="", 
                                                  image=  customtkinter.CTkImage(Image.open(os.path.join(image_path, Image_name + ".JPG")), size=(170, 170)))
            self.image_indenter.grid(row=row+1, column=column, padx=(20, 20), pady=(2, 2))
            action_with_arg = partial(self.add_Indenter, Image_name)
            globals()['self.' + 'addIndenter_' + Image_name] = customtkinter.CTkButton(self, command=action_with_arg, width = 140, text="Add Indenter")
            globals()['self.' + 'addIndenter_' + Image_name].grid(row=row+2, column=column, padx=(2, 2), pady=(10, 10))  
            column += 2
            if indenter_number % 6 == 0:
                row += 4
                column = 1  
            indenter_number += 1 



    def add_Indenter(self, jar):
        # print(jar)
        global phrase_to_search
        phrase_to_search =  jar
        # globals()['self.' + 'addIndenter_' + jar].configure(state="disabled")
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.grab_set()
        

class Frame_Curved(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toplevel_window_curved = None

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        indenter_number = 1
        row = 1
        column = 1
        for Indenter_name, Image_name in zip(Different_names_Curved, Images_names_Curved):
            self.label_indenter = customtkinter.CTkLabel(self, text=Indenter_name, fg_color="transparent", font=customtkinter.CTkFont(size=15, weight='bold'))
            self.label_indenter.grid(row=row, column=column,  padx=(2, 2), pady=(15, 2))    
            self.image_indenter = customtkinter.CTkLabel(self, text="", 
                                                  image=  customtkinter.CTkImage(Image.open(os.path.join(image_path, Image_name + ".JPG")), size=(170, 170)))
            self.image_indenter.grid(row=row+1, column=column, padx=(20, 20), pady=(2, 2))
            action_with_arg = partial(self.add_Indenter, Image_name)
            globals()['self.' + 'addIndenter_' + Image_name] = customtkinter.CTkButton(self, command=action_with_arg, width = 140, text="Add Indenter")
            globals()['self.' + 'addIndenter_' + Image_name].grid(row=row+2, column=column, padx=(2, 2), pady=(10, 10))  
            column += 2
            if indenter_number % 6 == 0:
                row += 4
                column = 1  
            indenter_number += 1 
            
    def add_Indenter(self, jar):
        # print(jar)
        global phrase_to_search
        phrase_to_search =  jar
        # globals()['self.' + 'addIndenter_' + jar].configure(state="disabled")
        if self.toplevel_window_curved is None or not self.toplevel_window_curved.winfo_exists():
            self.toplevel_window_curved = toplevel_window_curved(self)  # create window if its None or destroyed
        else:
            self.toplevel_window_curved.focus()  # if window exists focus it
            self.toplevel_window_curved.grab_set()

        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        global phrase_to_search
        # configure window
        self.title("Create dataset.py")
        self.geometry(f"{1540}x{750}")

        # configure grid layout (4x4)
        self.grid_rowconfigure(18, weight=1)
        self.grid_columnconfigure(11, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, height=530, corner_radius=4)
        self.sidebar_frame.grid(row=0, column=3, rowspan=19, sticky="nsew", padx=5, pady=(20, 20))
        self.sidebar_frame.grid_rowconfigure(17, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Actual Dataset", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, height=380, width=200)
        self.textbox.grid(row=2, column=0, padx=(10, 10), pady=(5, 5))

        check_Abaqus = customtkinter.CTkCheckBox(self.sidebar_frame, text="Abaqus Dataset", onvalue="Abaqus", offvalue="off", font=customtkinter.CTkFont(size=13, weight="bold"))
        check_Abaqus.grid(row=33, column=0, padx=0, pady=(7, 5), sticky="nsew")

        check_Issac = customtkinter.CTkCheckBox(self.sidebar_frame, text="Issac Dataset", onvalue="Issac", offvalue="off", font=customtkinter.CTkFont(size=13, weight="bold"))
        check_Issac.grid(row=34, column=0, padx=0, pady=(7, 5), sticky="nsew")

        check_Issac = customtkinter.CTkCheckBox(self.sidebar_frame, text="Real Dataset", onvalue="Issac", offvalue="off", font=customtkinter.CTkFont(size=13, weight="bold"))
        check_Issac.grid(row=35, column=0, padx=0, pady=(7, 5), sticky="nsew")

        self.name_label = customtkinter.CTkLabel(self.sidebar_frame, text="Name of the dataset:", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.name_label.grid(row=36, column=0, padx=20, pady=(20, 5))

        self.entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Dataset_01")
        self.entry.grid(row=37, column=0, padx=(20, 0), pady=(5, 10))
          
        self.Generate_Data = customtkinter.CTkButton(self.sidebar_frame, command=self.create_dataset_final, font=customtkinter.CTkFont(size=17, weight="bold"))
        self.Generate_Data.grid(row=38, column=0, padx=0, pady=(10,15))
        self.Generate_Data.configure(text="Generate")


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview._segmented_button.configure(font=customtkinter.CTkFont(size=17, weight='bold'))

        self.tabview.grid(row=1, column=1, padx=(10, 10), pady=(20, 20), sticky="nsew")

        tab_Flat = self.tabview.add("    Indenters    ")
        tab_Curved = self.tabview.add("    Objects    ")
        tab_Flat.grid_columnconfigure(2, weight=1)  # configure grid of individual tabs
        tab_Curved.grid_columnconfigure(2, weight=1)

        self.Frame_Flat = Frame_Flat(master=tab_Flat, width=1250, height=640, corner_radius=0, fg_color="transparent", orientation = 'vertical')
        self.Frame_Flat.grid(row=0, column=0, sticky="nsew")

        self.Frame_Curved = Frame_Curved(master=tab_Curved, width=1250, height=640, corner_radius=0, fg_color="transparent", orientation = 'vertical')
        self.Frame_Curved.grid(row=0, column=0, sticky="nsew")

        self.Generate_Data.configure(state="disabled")


    def create_dataset_final(self):
        self.Generate_Data.configure(state="disabled")
        Dataset_name = self.entry.get()
        Data_real_Super = pd.DataFrame()
        Data_simu_Super = pd.DataFrame()
        for i in range(len(Dataset_added)):
            s = Dataset_added[i]
            # print(s)
            temporal_simulation = Data_Simulation[Data_Simulation['Path'] == s]
            temporal_real = Data_real[Data_real['Path'] == s]
            Data_real_Super = pd.concat([Data_real_Super, temporal_real], axis=0)
            Data_simu_Super = pd.concat([Data_simu_Super, temporal_simulation], axis=0)

        path_save_data = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DatasetGenerated")
        Data_simu_Super.to_csv(path_save_data + '/' + Dataset_name + '_Simulation_Abaqus.csv', encoding='utf-8', index=False)
        Data_real_Super.to_csv(path_save_data + '/' + Dataset_name + '_Real_Abaqus.csv', encoding='utf-8', index=False)
        self.textbox.delete("0.0", "end") 

        
        startfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "DatasetGenerated"))

        self.ToplevelWindowSucess = ToplevelWindowSucess(self)

if __name__ == "__main__":

    app = App()
    app.mainloop()
