"""Utils: guardado_archivos

Provee GuardadoArchivos, una utilidad simple para crear un directorio de
reportes (reportes_sistema), imprimir reportes por consola y anexarlos a
archivos con nombre basado en timestamp. Está pensada para ser usada por los
módulos del proyecto que generan contenido para reporte.
"""
import os
from datetime import datetime

class GuardadoArchivos():
    """Clase encargada de gestionar la creación y el guardado de reportes.

    Comportamiento:
    - Crea el directorio 'reportes_sistema' al inicializar si no existe.
    - Método reporte(texto): añade fecha/hora al texto, lo imprime por consola y
      lo guarda en un archivo de texto con nombre basado en la fecha/hora.
    """

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
        """Genera un reporte: lo imprime y lo anexa a un archivo timestamped.

        Args:
            texto (str): Contenido del reporte (puede incluir varias líneas).

        El archivo se crea (o se abre en modo append) dentro de 'reportes_sistema'
        con un nombre del tipo reporte_YYYY-MM-DD HH-MM-SS.txt.
        """
        # Marca del tiempo 
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # Ruta archivos
        ruta_reporte = os.path.join(self.carpeta_Reportes, f"reporte_{timestamp}.txt")
        # Agregar fecha y hora al inicio del texto del reporte
        texto_completo = f"Fecha y hora de generación: {timestamp}\n\n{texto}"
        print(texto_completo)  # Muestra en terminal
        with open(ruta_reporte, "a", encoding="utf-8") as archivo:
            archivo.write(texto_completo + "\n")  # Guarda en el .txt