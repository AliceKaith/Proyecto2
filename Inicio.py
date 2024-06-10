import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Ejemplo")
        self.geometry("400x300")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Cambiar el tema

        # Crear frames para cada pantalla
        self.home_frame = ttk.Frame(self)
        self.clients_frame = ClientsFrame(self)

        # Mostrar la pantalla inicial
        self.show_frame(self.home_frame)
        self.create_widgets()

    def create_widgets(self):
        # Crear el contenedor para la página de inicio
        self.home_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear el título de la página de inicio
        self.title_label = ttk.Label(self.home_frame, text="Página de Inicio", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        # Crear botones
        self.clients_button = ttk.Button(self.home_frame, text="Clientes", command=self.show_clients, width=20)
        self.clients_button.grid(row=1, column=0, pady=10, sticky="w")

        self.monthly_tables_button = ttk.Button(self.home_frame, text="Tablas mensuales", command=self.show_monthly_tables, width=20)
        self.monthly_tables_button.grid(row=2, column=0, pady=10, sticky="w")

    def show_frame(self, frame):
        frame.tkraise()

    def show_clients(self):
        self.clients_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.show_frame(self.clients_frame)

    def show_monthly_tables(self):
        messagebox.showinfo("Tablas mensuales", "Aquí se mostrarían las tablas mensuales.")

class ClientsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self, text="Clientes", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, pady=10, sticky="w")

        self.back_button = ttk.Button(self, text="Volver", command=self.go_back, width=20)
        self.back_button.grid(row=1, column=0, pady=10, sticky="w")

    def go_back(self):
        self.pack_forget()
        self.master.show_frame(self.master.home_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
