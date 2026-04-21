"""MonRecursos module

Proporciona funciones para recopilar métricas del sistema (CPU, memoria, disco),
conexiones de red y listado de procesos en ejecución. Usa psutil para obtener
esta información y la acumula en una cadena que luego se guarda mediante
GuardadoArchivos.

Función principal:
- monitoreo_recursos(): reune métricas y genera un reporte completo que se guarda
  usando utils.guardado_archivos.GuardadoArchivos.reporte().
"""
import psutil
import platform
import os
from datetime import datetime
from utils.guardado_archivos import GuardadoArchivos

guardado_archivos = GuardadoArchivos()

def monitoreo_recursos():
    """
    Punto 2: Monitoreo de Recursos.
    Se acumula todo en una variable para generar un solo archivo final.
    """
    #Se crea una variable para poder guardar todo en un solo reporte 
    contenido = ""

    contenido += "\n-*-*-*-* Recursos de sistema *-*-*-*-\n" #Se llena con el contenido del reporte
    # El intervalo de 1 segundo aquí es bueno para la precisión del CPU
    contenido += f"Porcentaje de uso de la CPU: {psutil.cpu_percent(interval=1)}%\n"
    #Muestra la memoria en uso
    memory = psutil.virtual_memory()
    contenido += f"Memoria en uso: {memory.percent}%\n" #se guarda en el reporte junto con su porcentaje
    #Disco
    disk = psutil.disk_usage('/')
    contenido += f"Uso de disco: {disk.percent}%\n"
    contenido += "---*---*---*---*---*---\n"

    #Analiza las conexiones de red 
    contenido += "\n-*-*-*-* Conexiones de Red *-*-*-*-\n"
    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
        contenido += f"Protocolo: {conn.type} | Local: {laddr} | Estado: {conn.status}\n"
    contenido += "---*---*---*---*---*---\n"

    #Lista todos los procesos en ejecución
    contenido += "\n-*-*-*-* Listado de Procesos *-*-*-*-\n"
    contenido += f"{'PID':<10} {'CPU%':<10} {'MEM%':<10} {'Nombre'}\n"
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            # Vamos sumando cada proceso a nuestra variable 'contenido'
            linea_proceso = f"{pinfo['pid']:<10} {pinfo['cpu_percent']:<10} {round(pinfo['memory_percent'], 2):<10} {pinfo['name']}\n"
            contenido += linea_proceso
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    contenido += "---*---*---*---*---*---\n"

    #Solo llama al reporte y vez para que no genere más de lo necesario a la hora de guardar
    guardado_archivos.reporte(contenido)


monitoreo_recursos()