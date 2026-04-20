import subprocess

class ComandosOS:
    """
    Clase para ejecutar comandos del sistema operativo utilizando la librería subprocess.
    Incluye comandos para mostrar servicios en ejecución y verificar configuraciones de seguridad.
    """

    def __init__(self):
        """
        Inicializa la clase ComandosOS.
        """
        pass

    def ejecutar_comando(self, comando):
        """
        Ejecuta un comando del sistema operativo y retorna su salida.

        Args:
            comando (list): Lista con el comando y sus argumentos.

        Returns:
            str: Salida del comando o mensaje de error.
        """
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True, timeout=10)
            if resultado.returncode == 0:
                return resultado.stdout
            else:
                return f"Error al ejecutar el comando: {resultado.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: El comando tardó demasiado en ejecutarse."
        except Exception as e:
            return f"Error inesperado: {e}"

    def obtener_servicios_ejecucion(self):
        """
        Obtiene y retorna información sobre los servicios en ejecución.

        Returns:
            str: Información sobre los servicios en ejecución.
        """
        # Comando para Windows: sc query (lista servicios)
        comando = ["sc", "query"]
        salida = self.ejecutar_comando(comando)
        return salida

    def verificar_configuraciones_seguridad(self):
        """
        Verifica y retorna configuraciones de seguridad del sistema, como firewall y usuarios conectados.

        Returns:
            dict: Diccionario con información de configuraciones de seguridad.
        """
        info_seguridad = {}

        # Configuración del firewall
        comando_firewall = ["netsh", "advfirewall", "show", "allprofiles"]
        info_seguridad["firewall"] = self.ejecutar_comando(comando_firewall)

        # Usuarios conectados
        comando_usuarios = ["query", "user"]
        info_seguridad["usuarios_conectados"] = self.ejecutar_comando(comando_usuarios)

        return info_seguridad

    def mostrar_informacion(self):
        """
        Recopila y organiza la información de comandos del sistema operativo en un diccionario.

        Returns:
            dict: Diccionario con la información recopilada.
        """
        info = {
            "servicios_ejecucion": self.obtener_servicios_ejecucion(),
            "configuraciones_seguridad": self.verificar_configuraciones_seguridad()
        }
        return info

    def generar_reporte_texto(self):
        """
        Genera una representación en texto de la información de comandos del sistema operativo para reportes.

        Returns:
            str: Cadena de texto con la información formateada.
        """
        info = self.mostrar_informacion()
        reporte = "=== Información de Comandos del Sistema Operativo ===\n"
        reporte += "Servicios en ejecución:\n"
        reporte += info['servicios_ejecucion'] + "\n\n"
        reporte += "Configuraciones de seguridad:\n"
        reporte += f"Firewall:\n{info['configuraciones_seguridad']['firewall']}\n"
        reporte += f"Usuarios conectados:\n{info['configuraciones_seguridad']['usuarios_conectados']}\n"
        return reporte

    def guardar_reporte(self, guardado_archivos):
        """
        Genera el reporte de texto y lo guarda usando la utilidad GuardadoArchivos.

        Args:
            guardado_archivos (GuardadoArchivos): Instancia de la clase GuardadoArchivos para guardar el reporte.
        """
        texto_reporte = self.generar_reporte_texto()
        guardado_archivos.reporte(texto_reporte)