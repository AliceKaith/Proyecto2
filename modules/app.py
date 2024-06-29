import os
import calendar
import datetime
from typing import Dict, List
import customtkinter as ctk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import sqlite3

class App(ctk.CTk):

    DATA_TEST = {
        "limite_inferior": "1231231.00",
        "limite superior": "13123123.00",
        "cuota_fija": "100,000.00",
        "porcentaje": "56.00"
    }
    TABS = [
        {"tab_name": "Inicio"},
        {"tab_name": "Clientes"},
        {"tab_name": "Tablas"},
        {"tab_name": "Isr"}
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

        # Diccionario para almacenar selecciones
        self.selections = {}

        # Mostrar la pantalla inicial
        self.show_frame(self.home_frame)
        self.create_widgets()
        
        # Obtener la ruta del directorio actual del script
        modules = os.path.dirname(__file__)

        # Construir la ruta completa a la base de datos
        db_relative_path = os.path.join('..', 'db', 'main.db')  # '..' sube un nivel al directorio padre
        self.db_path = os.path.abspath(os.path.join(modules, db_relative_path))
        
        # Conectar a la base de datos
        self.db_connection = sqlite3.connect(self.db_path)

    def create_widgets(self):
        # Crear el contenedor para la página de inicio
        self.home_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Crear el título de la página de inicio
        self.title_label = ctk.CTkLabel(self.tab_variables['Inicio'], text="Página de Inicio", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        # Crear botones
        self.clients_button = ctk.CTkButton(self.tab_variables['Clientes'], text="Clientes", command=self.show_clients, width=20)
        self.clients_button.grid(row=1, column=0, pady=10, sticky="w")

        self.import_button = ctk.CTkButton(self.tab_variables['Clientes'], text="Importar XML", command=self.import_xml, width=20)
        self.import_button.grid(row=2, column=0, pady=10, sticky="w")

        self.monthly_tables_button = ctk.CTkButton(self.tab_variables['Tablas'], text="Tablas mensuales", command=self.show_monthly_tables, width=20)
        self.monthly_tables_button.grid(row=2, column=0, pady=10, sticky="w")

    def show_frame(self, frame):
        frame.tkraise()

    def show_clients(self):
        self.clients_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.show_frame(self.clients_frame)

    def show_monthly_tables(self):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        choices = [f"{calendar.month_name[month]} {current_year}" for month in range(1, 13) if month <= current_month]

        self.combobox = ctk.CTkComboBox(master=self.tab_variables['Tablas'],
                                        values=choices,
                                        command=self.combobox_callback)
        self.combobox.grid(row=3, column=0, pady=10, sticky="w")
        self.combobox.set("")

    def combobox_callback(self, choice):
        current_year = datetime.datetime.now().year
        self.selections[choice] = current_year
        print("Combobox dropdown clicked:", choice)
        print("Selections:", self.selections)
    
    #importar el XML y leerlo
    def import_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            print(f"Archivo importado: {file_path}")
            self.parse_and_insert_xml(file_path)

    def parse_and_insert_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Obtener la fecha actual

        # Iterar sobre cada elemento Fila
        for fila in root.findall('Fila'):
            try:
                ingresos = float(fila.find('ingresos').text)
                retencion_10 = float(fila.find('retencion_10').text)
                deducciones = float(fila.find('deducciones').text)
                base = float(fila.find('base').text)
                isr_o_favor = float(fila.find('isr_o_favor').text)
                
                self.insert_into_db(ingresos, retencion_10, deducciones, base, isr_o_favor, current_date)
                
            except AttributeError as e:
                print(f"Error: Elemento no encontrado en la fila. {e}")
            except ValueError as e:
                print(f"Error: Conversión a float fallida. {e}")
    
    #insertar datos en la base de datos
    def insert_into_db(self, ingresos, retencion_10, deducciones, base, isr_o_favor, fecha):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            INSERT INTO Regimen (ingresos, retencion_10, deducciones, base, isr_o_favor, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ingresos, retencion_10, deducciones, base, isr_o_favor, fecha))
        self.db_connection.commit()

    def create_tabs(self, tabs: List[Dict[str, str]]):
        self.tab_variables = {}
        self.tabview = ctk.CTkTabview(master=self.home_frame)
        self.tabview.pack(fill='both', expand=True)
        
        for tab in tabs:
            tab_name = tab["tab_name"]
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
