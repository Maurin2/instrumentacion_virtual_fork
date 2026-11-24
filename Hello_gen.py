
import sys

import pyvisa as visa

from InstVirtualLib.generadores_arbitrarios import Siglent1032X

IP_GEN = "192.168.0.101"


def inicializar_generador(direccion=IP_GEN):
    """Abre el Siglent 1032X por IP (VXI-11) o por recurso VISA y lo devuelve listo para usar."""
    recurso = direccion if "::" in direccion else f"TCPIP::{direccion}::INSTR"
    rm = visa.ResourceManager()
    handler = rm.open_resource(recurso)
    return Siglent1032X(handler)


gen = inicializar_generador()
try:
    print("IDN     :", gen.INSTR_ID.strip())
    print("Conexion:", "USB" if gen.connector_is_usb else "LAN")
finally:
    gen.close()
