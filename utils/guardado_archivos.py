import os
from datetime import datetime

class GuardadoArchivos():

    def __init__(self):
        # Creación de la carpeta
        self.carpeta_Reportes = "reportes_sistema"
        if not os.path.exists(self.carpeta_Reportes):
            os.mkdir(self.carpeta_Reportes)
            print("Carpeta creada")
        else:
            print("La carpeta ya existe")

    # --- FUNCIÓN PARA GENERAR EL REPORTE ---
    # Esta función hace el trabajo doble: consola y archivo
    def reporte(self, texto):
        # Marca del tiempo 
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # Ruta archivos
        ruta_reporte = os.path.join(self.carpeta_Reportes, f"reporte_{timestamp}.txt")
        print(texto) # Muestra en terminal
        with open(ruta_reporte, "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n") # Guarda en el .txt