# -*- coding: utf-8 -*-
"""
Hello world del osciloscopio Rigol DS2202: lo inicializa y le pide el *IDN?.

Uso (desde la raiz del repo):
    python Hello_osc.py                      -> por LAN, IP por defecto
    python Hello_osc.py 10.42.0.47           -> por LAN, otra IP
    python Hello_osc.py "USB0::...::INSTR"   -> recurso VISA completo (ej: por USB)
"""

import sys

import pyvisa as visa

from InstVirtualLib.osciloscopios import RIGOL_DS2202

# La misma IP que usan la GUI y SweepConfig para el osciloscopio
IP_OSC = "192.168.0.100"


def inicializar_osciloscopio(direccion=IP_OSC):
    """Abre el Rigol DS2202 por IP (VXI-11) o por recurso VISA y lo devuelve listo para usar."""
    recurso = direccion if "::" in direccion else f"TCPIP::{direccion}::INSTR"
    rm = visa.ResourceManager()
    # Timeout de 10 s: el default de pyvisa (2 s) puede cortar la lectura de trazas largas
    handler = rm.open_resource(recurso, timeout=10000)
    return RIGOL_DS2202(handler)


if __name__ == "__main__":
    direccion = sys.argv[1] if len(sys.argv) > 1 else IP_OSC

    print(f"Conectando al osciloscopio en {direccion} ...")
    osc = inicializar_osciloscopio(direccion)
    try:
        print("Conexion:", "USB" if osc.connector_is_usb else "LAN")
        print("IDN     :", osc.INSTR_ID.strip())
    finally:
        osc.close()
