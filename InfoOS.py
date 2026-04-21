"""InfoOS module

Recopila información del sistema operativo y hardware usando platform y la guarda
utilizando la utilidad GuardadoArchivos del paquete utils.

Función principal:
- info_sistema(): recaba datos sobre OS, versión, arquitectura y procesador y los
  escribe en el sistema de guardado de reportes.
"""
import platform, psutil, subprocess, os
from datetime import datetime
from utils.guardado_archivos import GuardadoArchivos

guardado_archivos = GuardadoArchivos()
def info_sistema():
    """
    Punto 1: Información del Sistema Operativo y Hardware.
    Uso de la libreria platform para recopilar y mostrar la siguiente información:
    """
    
    #Inicio del reporte 
    guardado_archivos.reporte("REPORTE DE AUDITORIA DEL SISTEMA")
    guardado_archivos.reporte("")

    #Uso de la libreria platafomr para extraer información del sistema operativo y el hardware
    #OS y versión 
    #arquitectura y modelo cpu 
    guardado_archivos.reporte("-*-*-*-*Información del sistema*-*-*-*-")
    guardado_archivos.reporte(f"Sistema operativo: {platform.system()}")
    guardado_archivos.reporte(f"Versión del sistema: {platform.release()} (Build: {platform.version()})")
    guardado_archivos.reporte(f"Arquitectura del CPU: {platform.architecture()[0]}") 
    guardado_archivos.reporte(f"Procesador del dispositivo: {platform.processor()}")
    guardado_archivos.reporte("---*---*---*---*---*---")


#Llamado de la función
info_sistema()