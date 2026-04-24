# G4_CY202_CasoEstudio2

## Descripción y Funcionamiento

Este es un programa de monitoreo del sistema operativo que permite al usuario obtener información detallada sobre el hardware, los recursos del sistema, procesos en ejecución, conexiones de red y más. El programa ofrece una interfaz de menú interactiva que facilita la navegación entre las diferentes funcionalidades.

### Funcionalidades principales:

- **Información del sistema**: Muestra datos del sistema operativo, arquitectura y procesador.
- **Monitoreo de recursos**: Visualiza el uso de CPU, memoria RAM, disco y conexiones de red.
- **Lista de procesos**: Enumera todos los procesos en ejecución con su PID, uso de CPU y memoria.
- **Variables de entorno**: Muestra las variables de entorno del sistema.
- **Comandos del sistema**: Ejecuta comandos para ver servicios y configuraciones de seguridad.
- **Reportes**: Genera archivos de reporte con toda la información recopilada.
- **Monitoreo en tiempo real**: Actualiza continuamente el uso de recursos cada X segundos.

---

## Requerimientos

Para ejecutar el programa, necesitas tener instalado Python 3.x y las siguientes librerías:

```bash
pip install psutil
```

---

## Cómo Ejecutar

1. Asegúrate de tener Python instalado en tu sistema.
2. Instala la librería requerida: `pip install psutil`
3. Navega al directorio del proyecto.
4. Ejecuta el programa principal:

```bash
python main.py
```

5. Selecciona una opción del menú interactivo:
   - **1**: Ver información del sistema operativo y hardware
   - **2**: Ver uso actual de recursos
   - **3**: Generar un reporte completo
   - **4**: Monitorear recursos en tiempo real
   - **5**: Salir del programa

---