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
        self.home_frame = ctk.CTkFrame(self,fg_color="#0B0B0D")
        self.clients_frame = ClientsFrame(self)
        self.create_tabs(self.TABS)

        # Diccionario para almacenar selecciones
        self.selections = {}

        # Mostrar la pantalla inicial
        self.show_frame(self.home_frame)
        
        # Obtener la ruta del directorio actual del script
        modules = os.path.dirname(__file__)

        # Construir la ruta completa a la base de datos
        db_relative_path = os.path.join('..', 'db', 'main.db')  # '..' sube un nivel al directorio padre
        self.db_path = os.path.abspath(os.path.join(modules, db_relative_path))
        self.db_connection = sqlite3.connect(self.db_path)
        
        self.clients = ["karla","raul"]
        self.create_widgets()
        # Conectar a la base de datos

    def create_widgets(self):
        # Crear el contenedor para la página de inicio
        self.home_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Crear el título de la página de inicio
        # self.title_label = ctk.CTkLabel(self.tab_variables['Inicio'], text="Página de Inicio", font=("Arial", 16))
        # self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        # Crear botones
        

        self.show_monthly_tables()  

        
        self.home_frames(self.clients)
        self.client_frames()

    def home_frames(self,clients):
        self.frame_home_clients = ctk.CTkFrame(self.tab_variables['Inicio'],bg_color="transparent",fg_color="#474A56",width=1000,height=500,corner_radius=20)
        self.frame_home_clients.place(x=10,y=0)

        self.frame_home_selection = ctk.CTkFrame(self.tab_variables['Inicio'],bg_color="transparent",fg_color="#474A56",width=200,height=500,corner_radius=20)
        self.frame_home_selection.place(x=1030,y=0)

        self.combobox_home_clients =  ctk.CTkComboBox(master=self.frame_home_selection,
                                        values=clients,
                                        command=self.clients_combobox_callback)
        
        self.combobox_home_clients.place(x=35,y=10)
        self.combobox_home_clients.set("")

        self.button_import_file = ctk.CTkButton(self.tab_variables['Inicio'],bg_color="transparent",fg_color="#929AAB",text_color="black",hover_color="#D3D5FD",width=50,height=50,corner_radius=20,text="Insertar Clientes")
        self.button_import_file.place(x=10,y=550)

        # self.clients_button = ctk.CTkButton(self.tab_variables['Inicio'], bg_color="transparent",height=50,corner_radius=20,text="Clientes", command=self.show_clients, width=20)
        # self.clients_button.place(x=150,y=550)

        self.import_button = ctk.CTkButton(self.tab_variables['Inicio'], bg_color="transparent",fg_color="#929AAB",text_color="black",hover_color="#D3D5FD",height=50,corner_radius=20,text="Importar XML", command=self.import_xml, width=20)
        self.import_button.place(x=150,y=550)



    def client_frames(self):        
        
        self.frame_client_tabla1 = ctk.CTkFrame(self.tab_variables['Clientes'],bg_color="transparent",fg_color="#474A56",width=600,height=600,corner_radius=20)
        self.frame_client_tabla1.place(x=10,y=0)

        self.frame_client_tabla2 = ctk.CTkFrame(self.tab_variables['Clientes'],bg_color="transparent",fg_color="#474A56",width=600,height=600,corner_radius=20)
        self.frame_client_tabla2.place(x=620,y=0)

       
        
    def clients_combobox_callback(self,choice):
        self.client_selected = choice
        print("Combobox dropdown clicked:", self.client_selected)

    def show_frame(self, frame):
        frame.tkraise()

    def show_clients(self):
        self.clients_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.show_frame(self.clients_frame)

    def show_monthly_tables(self):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        choices = [f"{calendar.month_name[month]} {current_year}" for month in range(1, 13) if month <= current_month]

        # combobox del tab tablas
        self.combobox = ctk.CTkComboBox(master=self.tab_variables['Tablas'],
                                    values=choices,
                                    command=self.combobox_callback)
        self.combobox.grid(row=0, column=0, padx=30, pady=10, sticky="nw")
        self.combobox.set("")

    # frames del tab tablas
        self.frames_tablas = ctk.CTkFrame(self.tab_variables['Tablas'],bg_color="transparent",fg_color="#474A56",height=550,width=450,corner_radius=50)
        self.frames_tablas.place(x=10,y=60)

        self.frames_tablas = ctk.CTkFrame(self.tab_variables['Tablas'],bg_color="transparent",fg_color="#474A56",height=550,width=700,corner_radius=50)
        self.frames_tablas.place(x=500,y=60)


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

                iva_venta = 0 #float(fila.find('iva_venta').text)
                iva_retenido = 0 #float(fila.find('iva_retenido').text)
                iva_acreditable = 0 #float(fila.find('iva_acreditable').text)

                subsidio_acreditable = 0
                pagos_provisionales = 0
                credito_general = 0

                base = float(ingresos - deducciones) #float(fila.find('base').text)
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
        self.tabview = ctk.CTkTabview(master=self.home_frame,fg_color="#0B0B0D")
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
