#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import platform
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

PY = sys.executable


def run_script(script_name, extra_args=None):
    """Ejecuta un script Python del repositorio como proceso separado.

    Args:
        script_name (str): Nombre del archivo Python relativo a la raíz del repo.
        extra_args (list|None): Lista opcional de argumentos a pasar al script.

    Retorna el código de salida del proceso (int).
    """
    script_path = ROOT / script_name
    if not script_path.exists():
        print(f"Archivo no encontrado: {script_path}")
        return 1
    cmd = [PY, str(script_path)]
    if extra_args:
        cmd += extra_args
    try:
        return subprocess.call(cmd)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
        return 2
    except Exception as e:
        print(f"Error ejecutando {script_name}: {e}")
        return 3


def ejecutar_comandos_os_reporte():
    """Genera un reporte de comprobaciones del sistema usando ComandosOS.

    Ejecuta un pequeño comando embebido de Python que crea una instancia de
    ComandosOS y guarda su reporte mediante GuardadoArchivos. Se emplea un
    subproceso para evitar efectos secundarios al importar el módulo.
    """
    cmd = [PY, "-c",
           "from comandos_OS import ComandosOS; from utils.guardado_archivos import GuardadoArchivos; ComandosOS().guardar_reporte(GuardadoArchivos())",
          ]
    try:
        return subprocess.call(cmd)
    except Exception as e:
        print(f"Error generando reporte de comandos OS: {e}")
        return 1


def ejecutar_comandos_os_reporte_privileged():
    """Intenta generar el mismo reporte pero solicitando elevación cuando aplique.

    En sistemas Unix usa 'sudo' si está disponible en PATH. En Windows intenta
    ejecutar sin elevación (la elevación programática es compleja y depende del
    entorno). Si sudo no está disponible se intentará ejecutar sin privilegios y
    se informará al usuario.
    """
    cmd = [PY, "-c",
           "from comandos_OS import ComandosOS; from utils.guardado_archivos import GuardadoArchivos; ComandosOS().guardar_reporte(GuardadoArchivos())",
          ]
    sistema = platform.system().lower()
    if sistema != 'windows' and shutil.which('sudo'):
        full_cmd = ['sudo'] + cmd
        print('Ejecutando comprobaciones con sudo. Se puede solicitar la contraseña.')
    else:
        full_cmd = cmd
        if sistema != 'windows':
            print('sudo no disponible: intentando ejecutar sin elevación (algunas comprobaciones pueden fallar).')
        else:
            print('En Windows: intentando ejecutar comprobaciones sin elevación (pueden requerir permisos administrativos).')

    try:
        return subprocess.call(full_cmd)
    except Exception as e:
        print(f"Error generando reporte privilegiado: {e}")
        return 1


def generar_reporte_completo():
    """Orquesta la generación de un reporte completo ejecutando los módulos
    responsables: InfoOS, MonRecursos y ComandosOS. Cada módulo escribe su propio
    reporte mediante utils.guardado_archivos.

    Retorna la combinación OR de códigos de salida de los procesos ejecutados.
    """
    print("Generando reporte completo: InfoOS, MonRecursos, ComandosOS")
    rc = 0
    rc |= run_script('InfoOS.py')
    rc |= run_script('MonRecursos.py')
    rc |= ejecutar_comandos_os_reporte()
    print("Reporte completo finalizado.")
    return rc


def menu_interactivo():
    while True:
        print('\n--- Menú principal ---')
        print('1) Ver información del sistema y hardware')
        print('2) Ver uso actual de recursos')
        print('3) Generar reporte completo')
        print('4) Monitorear recursos en tiempo real')
        print('5) Ejecutar comprobaciones y reportes de comandos del OS (sin/sudo)')
        print('6) Ejecutar comprobaciones privilegiadas (requiere sudo en Unix)')
        print('7) Salir')
        try:
            op = input('Seleccione una opción (1-7): ').strip()
        except EOFError:
            print('\nEntrada finalizada. Saliendo.')
            return
        if op == '1':
            run_script('InfoOS.py')
        elif op == '2':
            run_script('MonRecursos.py')
        elif op == '3':
            generar_reporte_completo()
        elif op == '4':
            print('Iniciando monitoreo en tiempo real. Presione ENTER en esa ventana para detener.')
            run_script('monitoreo_tiempo_real.py')
        elif op == '5':
            ejecutar_comandos_os_reporte()
        elif op == '6':
            ejecutar_comandos_os_reporte_privileged()
        elif op == '7':
            print('Saliendo.')
            return
        else:
            print('Opción no válida. Intente de nuevo.')


def parse_args():
    """Parsea los argumentos de la línea de comandos para ejecutar acciones
    sin entrar al menú interactivo.

    Opciones principales (mutualmente excluyentes):
    --info, --recursos, --reporte, --monitoreo, --comandos, --comandos-priv, --interactive
    """
    p = argparse.ArgumentParser(description='Interfaz mixta para G4_CY202_CasoEstudio2')
    grp = p.add_mutually_exclusive_group()
    grp.add_argument('--info', action='store_true', help='Ver información del sistema y hardware')
    grp.add_argument('--recursos', action='store_true', help='Ver uso actual de recursos')
    grp.add_argument('--reporte', action='store_true', help='Generar reporte completo')
    grp.add_argument('--monitoreo', action='store_true', help='Monitorear recursos en tiempo real')
    grp.add_argument('--comandos', action='store_true', help='Ejecutar comprobaciones y generar reporte de comandos OS')
    grp.add_argument('--comandos-priv', dest='comandos_priv', action='store_true', help='Ejecutar comprobaciones con elevación (sudo en Unix)')
    grp.add_argument('--interactive', action='store_true', help='Abrir menú interactivo')
    return p.parse_args()


def main():
    args = parse_args()
    if args.info:
        return run_script('InfoOS.py')
    if args.recursos:
        return run_script('MonRecursos.py')
    if args.reporte:
        return generar_reporte_completo()
    if args.monitoreo:
        return run_script('monitoreo_tiempo_real.py')
    if getattr(args, 'comandos_priv', False):
        return ejecutar_comandos_os_reporte_privileged()
    if args.comandos:
        return ejecutar_comandos_os_reporte()
    # Default: interactive
    menu_interactivo()
    return 0


if __name__ == '__main__':
    sys.exit(main())
