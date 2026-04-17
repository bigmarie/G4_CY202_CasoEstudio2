# G4_CY202_CasoEstudio2
## Requerimientos:

### 1. Información del Sistema Operativo y Hardware (Naza):
Usar la librería platform para recopilar y mostrar la siguiente información:
- Nombre del sistema operativo y su versión.
- Arquitectura del sistema (32 o 64 bits).
- Nombre y modelo del procesador (CPU).

### 2. Monitoreo de Recursos (Naza):
Usar la librería psutil para:
- Mostrar el porcentaje de uso de la CPU, memoria RAM y disco.
- Mostrar información sobre las conexiones de red activas (puertos abiertos, direcciones IP y protocolos en uso).
- Listar los procesos en ejecución, mostrando:
   - Nombre del proceso.
   - PID (identificador del proceso).
   - Uso de CPU y memoria de cada proceso.

### 3. Información Adicional del Sistema (Alex):
Usar la librería os para:
- Obtener y mostrar el directorio de trabajo actual.
- Mostrar todas las variables de entorno del sistema.
 
### 4. Ejecución de Comandos del Sistema Operativo (Alex):
Usar la librería subprocess (opcional) para ejecutar comandos específicos del sistema operativo que:
- Muestren los servicios en ejecución.
- Verifiquen configuraciones de seguridad del sistema (como la configuración del firewall, usuarios conectados, etc.).

### 5. Interacción con el Usuario (Nicole):
El programa presenta un menú con las siguientes opciones:
- Ver información del sistema operativo y hardware.
- Ver el uso actual de recursos.
- Generar un reporte completo.
- Monitorear recursos en tiempo real.
- Salir del programa.
- El usuario selecciona una opción y el programa responde mostrando la información en la consola o generando los archivos necesarios.


### 6. Función de Monitoreo en Tiempo Real (Nicole):
Implementar una opción que permita monitorear el uso de CPU, memoria y disco en intervalos de tiempo definidos por el usuario (por ejemplo, cada 5 segundos).
- Mostrar esta información en tiempo real en la consola hasta que el usuario detenga la ejecución.

## Tareas Adicionales (Dierick):

- Incluir manejo de errores para garantizar que el programa no falle si ocurre un problema al acceder a información del sistema o al ejecutar comandos.
- Usar estructuras de datos como listas y diccionarios para organizar la información antes de escribirla en los reportes.
- Incluir comentarios y documentación en el código para explicar el propósito de cada parte del programa.
 
(utils) Usar las librerías os y shutil para:
- Guardar la información recopilada en un archivo de texto o CSV con un formato claro.
- Incluir en el archivo:
   - Fecha y hora de generación del reporte.
   - Toda la información recopilada en los pasos anteriores.
   - Crear un directorio llamado reportes_sistema en el directorio actual para almacenar todos los reportes generados.
   - Los reportes generados son almacenados en el directorio reportes_sistema y tienen un nombre basado en la fecha y hora de creación, como reporte_2025_04_12_19_30.txt.

# Convenciones
- snake_case para variables y funciones.
- Una rama principal (main) y una rama por integrante.
- Cada módulo que sea un archivo aparte.