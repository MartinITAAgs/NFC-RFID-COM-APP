import customtkinter as ctk
import serial
import sqlite3
import threading

# configuración de puerto
PUERTO_COM = 'COM3' 

class AppBiblioteca(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca Aña")
        self.geometry("700x500")
        
        # inicio
        self.init_db()

        # interfaz
        self.label_status = ctk.CTkLabel(self, text="Sistema listo", font=("Arial", 20, "bold"), text_color="gray")
        self.label_status.pack(pady=20)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(pady=10, padx=20, fill="x")

        self.label_libro = ctk.CTkLabel(self.info_frame, text="Libro: ---", font=("Arial", 16))
        self.label_libro.pack(pady=5)
        
        self.label_autor = ctk.CTkLabel(self.info_frame, text="Autor: ---", font=("Arial", 16))
        self.label_autor.pack(pady=5)

        self.historial_txt = ctk.CTkTextbox(self, width=600, height=200)
        self.historial_txt.pack(pady=20)

        # lectura serial
        threading.Thread(target=self.leer_serial, daemon=True).start()

    def init_db(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        # crear tabla
        cursor.execute("DROP TABLE IF EXISTS libros")
        cursor.execute('''CREATE TABLE libros 
                          (uid TEXT PRIMARY KEY, titulo TEXT, autor TEXT)''')
        
        # lista de libros basada en 6 tags existentes válidos
        # El tag 04D5EC05 -que venía con el rc550- NO se incluye aquí para que sea el "DENEGADO"
        #los valores AXXXXXX, BXXXXXXXXXXXXX, etc, no son reales, tendrán que ser reemplazados 
        # por los tags reales que sean escaneados e insertados en la base de datos.
        # En el video evidencia se utilizaron tarjetas bancarias para obtener los valores de dichos
        # tags para hacer funcionar el programa.
        libros_biblioteca = [
            ('AXXXXXX', '1984', 'George Orwell'),
            ('BXXXXXXXXXXXXX', 'El Principito', 'Antoine de Saint-Exupéry'),
            ('CXXXXXXXXXXXXX', 'Rayuela', 'Julio Cortázar'),
            ('DXXXXXXXXXXXXX', 'El Aleph', 'Jorge Luis Borges'),
            ('EXXXXXXXXXXXXX', 'Pedro Páramo', 'Juan Rulfo'),
            ('FXXXXXXXXXXXXX', 'La ciudad y los perros', 'Mario Vargas Llosa')
        ]
        
        cursor.executemany("INSERT INTO libros VALUES (?,?,?)", libros_biblioteca)
        conn.commit()
        conn.close()
        print("Base de datos actualizada con los nuevos identificadores.")

    def leer_serial(self):
        try:
            ser = serial.Serial(PUERTO_COM, 115200, timeout=1)
            while True:
                linea = ser.readline().decode('utf-8').strip()
                if linea:
                    self.after(0, self.consultar_libro, linea)
        except:
            self.after(0, lambda: self.label_status.configure(text="ERROR: MICROCONTROLADOR NO CONECTADO", text_color="red"))

    def consultar_libro(self, uid):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, autor FROM libros WHERE uid = ?", (uid,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            titulo, autor = resultado
            self.label_status.configure(text="ACCESO CONCEDIDO", text_color="green")
            self.label_libro.configure(text=f"Libro: {titulo}")
            self.label_autor.configure(text=f"Autor: {autor}")
            self.historial_txt.insert("0.0", f"[OK] Tag: {uid} -> {titulo}\n")
        else:
            self.label_status.configure(text="ACCESO DENEGADO", text_color="red")
            self.label_libro.configure(text="Libro: DESCONOCIDO")
            self.label_autor.configure(text="Autor: ---")
            self.historial_txt.insert("0.0", f"[ERROR] iDENFICADOR: {uid} no encontrado en la Biblioteca Aña\n")

if __name__ == "__main__":
    app = AppBiblioteca()
    app.mainloop()