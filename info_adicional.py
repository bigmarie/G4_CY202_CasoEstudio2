import os

class InfoAdicional:
    """
    Clase para recopilar información adicional del sistema operativo utilizando la librería os.
    """

    def __init__(self):
        """
        Inicializa la clase InfoAdicional.
        """
        pass

    def obtener_directorio_actual(self):
        """
        Obtiene y retorna el directorio de trabajo actual.

        Returns:
            str: El directorio de trabajo actual.
        """
        try:
            directorio_actual = os.getcwd()
            return directorio_actual
        except OSError as e:
            return f"Error al obtener el directorio actual: {e}"

    def obtener_variables_entorno(self):
        """
        Obtiene y retorna todas las variables de entorno del sistema en un diccionario.

        Returns:
            dict: Diccionario con las variables de entorno (clave: nombre de la variable, valor: valor de la variable).
        """
        try:
            variables_entorno = dict(os.environ)
            return variables_entorno
        except Exception as e:
            return {"error": f"Error al obtener las variables de entorno: {e}"}

    def mostrar_informacion(self):
        """
        Recopila y organiza la información adicional en un diccionario para facilitar su uso en reportes.

        Returns:
            dict: Diccionario con la información recopilada.
        """
        info = {
            "directorio_actual": self.obtener_directorio_actual(),
            "variables_entorno": self.obtener_variables_entorno()
        }
        return info

    def generar_reporte_texto(self):
        """
        Genera una representación en texto de la información adicional para reportes.

        Returns:
            str: Cadena de texto con la información formateada.
        """
        info = self.mostrar_informacion()
        reporte = "=== Información Adicional del Sistema ===\n"
        reporte += f"Directorio de trabajo actual: {info['directorio_actual']}\n\n"
        reporte += "Variables de entorno:\n"
        for clave, valor in info['variables_entorno'].items():
            reporte += f"{clave}: {valor}\n"
        return reporte

    def guardar_reporte(self, guardado_archivos):
        """
        Genera el reporte de texto y lo guarda usando la utilidad GuardadoArchivos.

        Args:
            guardado_archivos (GuardadoArchivos): Instancia de la clase GuardadoArchivos para guardar el reporte.
        """
        texto_reporte = self.generar_reporte_texto()
        guardado_archivos.reporte(texto_reporte)