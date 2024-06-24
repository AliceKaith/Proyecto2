import os
import calendar
import datetime
from typing import Dict, List
import customtkinter as ctk

class App(ctk.CTk):

    DATA_TEST = {
        "limite_inferior": "1231231.00",
        "limite superior": "13123123.00",
        "cuota_fija": "100,000.00",
        "porcentaje": "56.00"
    }
    TABS = [
        "Inicio",
        "Clientes",
        "Tablas",
        "Isr"
        ]
    
    
    def __init__(self, width, height):
        super().__init__()
        self.title("Aplicación de Ejemplo")
        self.geometry(f"{width}x{height}")
        ctk.set_appearance_mode('dark')

        # Crear frames para cada pantalla
        self.home_frame = ctk.CTkFrame(self)
        self.clients_frame = ClientsFrame(self)
        self.create_tabs(self.TABS)

        # Mostrar la pantalla inicial
        self.show_frame(self.home_frame)
        self.create_widgets()

    def create_widgets(self):
        # Crear el contenedor para la página de inicio
        self.home_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Crear el título de la página de inicio
        self.title_label = ctk.CTkLabel(self.tab_variables['Inicio'], text="Página de Inicio", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        # Crear botones
        self.clients_button = ctk.CTkButton(self.tab_variables['Clientes'], text="Clientes", command=self.show_clients, width=20)
        self.clients_button.grid(row=1, column=0, pady=10, sticky="w")

        self.monthly_tables_button = ctk.CTkButton(self.tab_variables['Tablas'], text="Tablas mensuales", command=self.show_monthly_tables, width=20)
        self.monthly_tables_button.grid(row=2, column=0, pady=10, sticky="w")

    def show_frame(self, frame):
        frame.tkraise()

    def show_clients(self):
        self.clients_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.show_frame(self.clients_frame)

    def show_monthly_tables(self):
        current_month = datetime.datetime.now().month
        choices = [calendar.month_name[month] for month in range(1, 13) if month <= current_month]

        combobox = ctk.CTkComboBox(master=self.home_frame,
                                   values=choices,
                                   command=self.combobox_callback)
        
        combobox.grid(row=2, column=1, pady=10, sticky="w")
        combobox.set("")
        
    def combobox_callback(self, choice):
        print("Combobox dropdown clicked:", choice)


    # Quiero que al llamar esta funcion el tipo de dato lista que revisa tenga el siguiente formato
    # [{"tab_name":"inicio"},{"tab_name":"isr"}]
    # de ese modo podemos acceder al nombre
    def create_tabs(self,tabs: List[str]):
        self.tab_variables = {}
        self.tabview = ctk.CTkTabview(master=self.home_frame)
        self.tabview.pack(fill='both', expand=True)
        
        for tab_name in tabs:
            self.tab_variables[tab_name] = self.tabview.add(tab_name)
            
    

class ClientsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Clientes", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        self.back_button = ctk.CTkButton(self, text="Volver", command=self.go_back, width=20)
        self.back_button.grid(row=1, column=0, pady=10, sticky="w")

    def go_back(self):
        self.pack_forget()
        self.master.show_frame(self.master.tab_variables['Clientes'])


