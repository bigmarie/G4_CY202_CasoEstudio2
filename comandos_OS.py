"""comandos_OS module

Clase ComandosOS: encapsula la ejecución de comandos del sistema (via subprocess)
para obtener información sobre servicios y configuraciones de seguridad. La clase
expone métodos para obtener datos y generar un reporte de texto que puede ser
almacenado mediante GuardadoArchivos.

Este módulo soporta Windows y sistemas tipo Unix (Linux). Se seleccionan comandos
adecuados según la plataforma y se usan herramientas disponibles (systemctl, ufw,
iptables, who, etc.) cuando están presentes.
"""
import subprocess
import platform
import shutil


class ComandosOS:
    """Encapsula la ejecución de comandos del sistema y la generación de reportes.

    Métodos principales:
    - ejecutar_comando(comando): ejecuta un comando y devuelve su salida o error.
    - obtener_servicios_ejecucion(): obtiene una lista de servicios en ejecución.
    - verificar_configuraciones_seguridad(): verifica firewall y usuarios conectados.
    - generar_reporte_texto(): formatea la información para guardarla.
    - guardar_reporte(guardado_archivos): genera y guarda el reporte usando GuardadoArchivos.
    """

    def __init__(self):
        pass

    def ejecutar_comando(self, comando):
        """Ejecuta un comando y retorna su salida.

        Args:
            comando (list): lista con el comando y sus argumentos.

        Returns:
            str: salida (stdout) del comando o un mensaje de error.
        """
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True, timeout=15)
            if resultado.returncode == 0:
                return resultado.stdout.strip()
            else:
                return f"Error al ejecutar el comando: {resultado.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "Error: El comando tardó demasiado en ejecutarse."
        except FileNotFoundError as e:
            return f"Comando no encontrado: {e}"
        except Exception as e:
            return f"Error inesperado: {e}"

    def obtener_servicios_ejecucion(self):
        """Obtiene información sobre servicios en ejecución según la plataforma.

        En Windows usa 'sc query'. En Linux/Unix intenta 'systemctl', luego 'service',
        y como último recurso muestra procesos con 'ps -ef'.
        """
        sistema = platform.system().lower()
        if sistema == 'windows':
            comando = ["sc", "query"]
        else:
            if shutil.which('systemctl'):
                comando = ["systemctl", "list-units", "--type=service", "--state=running"]
            elif shutil.which('service'):
                comando = ["service", "--status-all"]
            else:
                comando = ["ps", "-ef"]
        return self.ejecutar_comando(comando)

    def verificar_configuraciones_seguridad(self):
        """Verifica configuraciones de seguridad (firewall) y usuarios conectados.

        Devuelve un diccionario con claves 'firewall' y 'usuarios_conectados'.
        Selecciona herramientas disponibles según la plataforma y presencia en PATH.
        """
        info_seguridad = {}
        sistema = platform.system().lower()

        if sistema == 'windows':
            # Windows
            comando_firewall = ["netsh", "advfirewall", "show", "allprofiles"]
            comando_usuarios = ["query", "user"]
            info_seguridad['firewall'] = self.ejecutar_comando(comando_firewall)
            info_seguridad['usuarios_conectados'] = self.ejecutar_comando(comando_usuarios)
        else:
            # Linux/Unix
            if shutil.which('ufw'):
                info_seguridad['firewall'] = self.ejecutar_comando(["ufw", "status", "verbose"])
            elif shutil.which('firewall-cmd'):
                info_seguridad['firewall'] = self.ejecutar_comando(["firewall-cmd", "--list-all"]) 
            elif shutil.which('iptables'):
                info_seguridad['firewall'] = self.ejecutar_comando(["iptables", "-L", "-n", "-v"])  
            else:
                info_seguridad['firewall'] = "No se encontró herramienta de firewall conocida en el sistema"

            if shutil.which('who'):
                info_seguridad['usuarios_conectados'] = self.ejecutar_comando(["who"])
            elif shutil.which('w'):
                info_seguridad['usuarios_conectados'] = self.ejecutar_comando(["w"])
            else:
                info_seguridad['usuarios_conectados'] = "No se encontró comando 'who' o 'w'"

        return info_seguridad

    def mostrar_informacion(self):
        """Recopila y retorna la información relevante en un diccionario."""
        return {
            'servicios_ejecucion': self.obtener_servicios_ejecucion(),
            'configuraciones_seguridad': self.verificar_configuraciones_seguridad()
        }

    def generar_reporte_texto(self):
        """Formatea la información obtenida en texto para incluir en reportes."""
        info = self.mostrar_informacion()
        reporte = "=== Información de Comandos del Sistema Operativo ===\n"
        reporte += "Servicios en ejecución:\n"
        reporte += (info.get('servicios_ejecucion') or '') + "\n\n"
        reporte += "Configuraciones de seguridad:\n"
        cfg = info.get('configuraciones_seguridad', {})
        reporte += f"Firewall:\n{cfg.get('firewall', '')}\n"
        reporte += f"Usuarios conectados:\n{cfg.get('usuarios_conectados', '')}\n"
        return reporte

    def guardar_reporte(self, guardado_archivos):
        """Genera el reporte y lo guarda usando una instancia de GuardadoArchivos."""
        texto_reporte = self.generar_reporte_texto()
        guardado_archivos.reporte(texto_reporte)