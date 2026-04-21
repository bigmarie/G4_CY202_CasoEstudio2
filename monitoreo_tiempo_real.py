"""Módulo de monitoreo en tiempo real (sin guardado a disco).
Funciones en español:
- monitorear_tiempo_real
- iniciar_monitoreo_cli
- imprimir_actualizacion_amigable

Diseñado para ser importable desde main.py sin modificarlo.
"""

from datetime import datetime
import threading
import json
import sys
from typing import TextIO

import psutil


def _formato_bytes(num: int) -> str:
    """Convierte bytes a una cadena legible (KB/MB/GB)."""
    try:
        n = float(num)
    except Exception:
        return "0B"
    for unidad in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024.0:
            return f"{n:.1f}{unidad}"
        n /= 1024.0
    return f"{n:.1f}PB"


def imprimir_actualizacion_amigable(linea_json: str, flujo_salida: TextIO = sys.stdout) -> None:
    """Parsea la línea JSON y la imprime en formato humano.

    Ejemplo: [12:34:56] CPU: 12.3% | MEM: 45.6% (1.2GB/4.0GB) | DISCO: 78.9%
    """
    try:
        registro = json.loads(linea_json)
        ts = registro.get("ts")
        if isinstance(ts, str) and ts.endswith("Z"):
            ts_parsed = datetime.fromisoformat(ts[:-1])
        else:
            ts_parsed = datetime.fromisoformat(ts)
        hora = ts_parsed.strftime("%H:%M:%S")

        cpu = registro.get("cpu", 0.0)
        mem = registro.get("mem", {})
        mem_percent = mem.get("percent", 0.0)
        mem_used = _formato_bytes(mem.get("used", 0))
        mem_total = _formato_bytes(mem.get("total", 0))
        disk = registro.get("disk", {})
        disk_percent = disk.get("percent", 0.0)

        flujo_salida.write(f"[{hora}] CPU: {cpu:.1f}% | MEM: {mem_percent:.1f}% ({mem_used}/{mem_total}) | DISCO: {disk_percent:.1f}%\n")
        flujo_salida.flush()
    except Exception as e:
        sys.stderr.write(f"Error al formatear actualización: {e}\n")


def monitorear_tiempo_real(intervalo_segundos: int,
                           evento_detener: threading.Event,
                           flujo_salida: TextIO = sys.stdout,
                           imprimir_formateado: bool = True) -> None:
    """Bucle de monitoreo en tiempo real que no persiste datos en disco.

    Args:
        intervalo_segundos: tiempo entre muestras en segundos.
        evento_detener: threading.Event para detener el bucle desde otro hilo.
        flujo_salida: stream donde escribir las líneas JSON (por defecto sys.stdout).
        imprimir_formateado: si True también imprime versión amigable.
    """
    while not evento_detener.is_set():
        try:
            timestamp = datetime.utcnow().isoformat() + "Z"
            cpu = psutil.cpu_percent(interval=None)
            vm = psutil.virtual_memory()
            du = psutil.disk_usage("/")

            registro = {
                "ts": timestamp,
                "cpu": float(cpu),
                "mem": {"percent": float(vm.percent), "used": int(vm.used), "total": int(vm.total)},
                "disk": {"percent": float(du.percent), "used": int(du.used), "total": int(du.total)},
            }

            linea = json.dumps(registro, ensure_ascii=False)

            # Escribir línea JSON en el flujo
            try:
                flujo_salida.write(linea + "\n")
                flujo_salida.flush()
            except Exception as e:
                sys.stderr.write(f"No se pudo escribir en flujo_salida: {e}\n")

            # Imprimir versión legible si se requiere
            if imprimir_formateado:
                try:
                    imprimir_actualizacion_amigable(linea, flujo_salida)
                except Exception:
                    pass

        except (psutil.AccessDenied, psutil.NoSuchProcess) as e:
            sys.stderr.write(f"Error al obtener métricas (permiso/proceso): {e}\n")
        except Exception as e:
            sys.stderr.write(f"Error inesperado en monitoreo: {e}\n")

        if evento_detener.wait(intervalo_segundos):
            break


def iniciar_monitoreo_cli(intervalo_segundos: int = 5) -> None:
    """Inicia el monitoreo en un hilo y espera que el usuario presione ENTER para detener.

    Este módulo no guarda archivos en disco.
    """
    evento_detener = threading.Event()

    hilo = threading.Thread(target=monitorear_tiempo_real,
                            args=(intervalo_segundos, evento_detener, sys.stdout, True),
                            daemon=True)
    hilo.start()

    try:
        print("Presione ENTER para detener el monitoreo")
        input()
    except KeyboardInterrupt:
        print("Interrupción recibida. Deteniendo monitoreo...")
    finally:
        evento_detener.set()
        hilo.join(timeout=2 * max(1, intervalo_segundos))

    # Fin: no se escribe nada en disco
    return

iniciar_monitoreo_cli()