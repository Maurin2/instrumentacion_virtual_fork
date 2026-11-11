# -*- coding: utf-8 -*-
"""
Created on Thu May 17 09:39:36 2018

@author: Pablo, Ramiro

"""

class Instrument:

    '''
    Representa tanto un instrumento de medición como de control.
    Esta clase debe contener solo la implementación de funciones VISA básicas.
    '''

    def __init__(self, instrument_handle):

        # Variables o definiciones de la clase
        self.COMMAND_ID = "*IDN?"#"ID?;"
        self.COMMAND_COMM_ADDRESS = ""
        self.instrument_handle = instrument_handle

        # Desambiguamos el transporte a partir del recurso VISA ya abierto:
        # "TCPIP::<ip>::INSTR" (VXI-11), "TCPIP::<ip>::hislip0::INSTR" y
        # "TCPIP::<ip>::<puerto>::SOCKET" son LAN; el resto (USB, GPIB, serie) no.
        self.connector_is_usb = not instrument_handle.resource_name.upper().startswith("TCPIP")

        # Hacemos un query del ID y lo guardamos
        self.INSTR_ID = self.query(self.COMMAND_ID)

    def close(self):
        # pyvisa ya llama a before_close() dentro de close()
        self.instrument_handle.close()

    def print_ID(self):
        idn = self.INSTR_ID
        print(idn)
        return idn


    def write(self, command_string):
        """ Implement visa write command """

        self.instrument_handle.write(command_string)

    def query(self, command_string):
        """ Implement visa query command """

        return self.instrument_handle.query(command_string)

    def read(self):
        """ Implement visa read command """

        return self.instrument_handle.read()

    def read_raw(self):
        """ Implement visa read raw command """

        return self.instrument_handle.read_raw()

    def read_bytes(self, bytes_read, break_term=True):
        """ Implement visa read bytes command """

        return self.instrument_handle.read_bytes(bytes_read , break_on_termchar=break_term) if self.connector_is_usb else self.instrument_handle.read_raw()
