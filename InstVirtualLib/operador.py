# -*- coding: utf-8 -*-
"""
@author: Pablo, Ramiro

La idea es que esta clase tome un intrumento como entrada, junto con los datos
que necesita (como el canal de medición) y devuelva el valor solicitado 
utilizando la clase "mediciones".

Esta clase es un nivel de abstracción mas del osciloscopio donde podemos 
construir métodos de medición que utilicen varias mediciones en distintos
modos.

"""

import numpy as np
import mediciones
from InstVirtualLib.generadores_arbitrarios import generador_arbitrario


class Operador_osciloscopio(mediciones.Mediciones):
    
    def __init__(self,inst,operador):
        # nombre del equipo dado por el usuario
        self.operador	= operador
        # Clase de instrumento
        self.instrument	= inst


    def medir_Vrms(self, canal = 1, VERBOSE = False):

        if VERBOSE:
            print("metodo de medicion realizado por {}".format(self.operador))
            print("con el instrumento {}".format(self.instrument.print_ID()))

        tiempo,tension = self.instrument.get_trace(canal, VERBOSE)

        return self.Vrms(tiempo,tension)
    
    def medir_detaF(self, canal = 1, VERBOSE = False):
        pass

    def medir_indiceMod(self, canal = 1, VERBOSE = False):
        pass

    def get_espectro(self, canal = 1, ventan='uniforme', VERBOSE = False):
        # devolver eje en frecuencia
        pass

    def medir_thd(self,canal=1,VERBOSE= False):
        if VERBOSE:
            print("metodo de medicion realizado por {}".format(self.operador))
            print("con el instrumento {}".format(self.instrument.print_ID()))

        tiempo,tension = self.instrument.get_trace(canal, VERBOSE)

        return self.THD(tiempo,tension)


    def medir_RC(self, R, canal_Vg = "1", canal_Vr = "2", metodo="FFT", VERBOSE = False):
        """
        Esta funcion sirve para medir el valor de un capacitor. Para esto se debe armar
        un filtro RC pasa-altos con una resistencia conocida. A la entrada del filtro se
        debe aplicar una señal senoidal. La frecuencia exacta no es importante, pero debe
        ser lo suficientemente alta como para observar defasaje y atenuacion entra la señal
        de entrada y salida, pero no demasiado alta como para que la salida se encuentre muy
        atenuada.

        R: Resistencia que se utilizo para armar el circuito en ohms
        canal_Vg: Numero del canal conectado al generador
        canal_Vr: Numero del canal conectado a la salida del filtro (Deberia medir la caida de tension
        sbore R)
        metodo: Puede tomar los valores "FFT", "Potencia", "Lissajous", "Tiempo". Determina que metodo se
        utilizara para medir la capacitancia.
        VERBOSE: Imprime informacion de calculos intermedios

        Retorna: Valor del capacitor en faradios
        """


        if VERBOSE:
            print("Adquiriendo Vg")
        t,vg = self.instrument.get_trace(canal_Vg, VERBOSE)
        if VERBOSE:
            print("Adquiriendo Vr")
        t,vr = self.instrument.get_trace(canal_Vr, VERBOSE)

        if VERBOSE:
            print("Calculando mediante metodo " + metodo)

        if metodo == "FFT":
            C = self.medir_RC_fft(t, vg, vr, R, VERBOSE)

        elif metodo == "Potencia":
            C = self.medir_RC_potencia(t, vg, vr, R, VERBOSE)

        elif metodo == "Lissajous":
            C = self.medir_RC_lissajous(t, vg, vr, R, VERBOSE)

        elif metodo == "Tiempo":
            C = self.medir_RC_tiempo(t, vg, vr, R, VERBOSE)

        else:
            raise ValueError(metodo + " no es un argumento valido para \'metodo\'")

        if VERBOSE:
            print(f"C: {C}")

        return C

    def calculate_fft_response(self, channel1, channel2):
        t_filtro,v_filtro = self.instrument.get_trace(channel1, False)  # Canal del filtro
        t_gen,v_gen = self.instrument.get_trace(channel2, False)  # Canal del generador (señal pura)
        freq1_f, mag_f, fase_f = self.fft_componente_principal(t_filtro,v_filtro)
        freq_gen, mag_gen, fase_gen = self.fft_componente_principal(t_gen,v_gen)
        #   Obtenes mag2, Para darte una idea de que tan distinta es la tensin/freq
        #   Que pusiste en el generador, de la que REALMENTE hay

        diff_fase = fase_gen - fase_f

        return freq1_f, mag_gen, mag_f, diff_fase

class Operador_generador(mediciones.Mediciones):
    
    def __init__(self,inst: generador_arbitrario,operador):
        # nombre del equipo dado por el usuario
        self.operador	= operador
        # Clase de instrumento
        self.instrument	= inst

    def generar_FM(self, fc, fm, deltaF, cant_muestras, offset, sample_rate=100000):
        pass

    def generar_AM(self, fc, fm, M, cant_muestras, offset, sample_rate=100000):
        pass

    def generar_senoidal(self, channel, f, vpp):
        vp = vpp/2
        self.instrument.senoidal(self,f, vp, channel)

class Operador_analisis_espectral(mediciones.Mediciones):

    def __init__(self, generador:Operador_generador , osciloscopio:Operador_osciloscopio):
        self.generador = generador
        self.osciloscopio = osciloscopio

    def get_bode_for_freq(self, vpp, freq, channel_osc1,channel_osc2 , channel_gen):
        self.generador.generar_senoidal(channel_osc1, freq, vpp)

        print("Agregarle un delay de 10 periodos (ponele)")
        # await asyncio.sleep(10 * 1/freq)

        freq, mag_gen, mag_f, diff_fase = self.osciloscopio.calculate_fft_response(channel_osc1, channel_osc2)

        self.calculoIncertidumbreFft()

        return freq, mag_f/mag_gen, diff_fase

    def barrido_bode(self, freq_array, vpp, channel_osc, channel_gen):
        v_array = []
        freq_array = []
        phase_array = []

        for f in freq_array:
            freq, mag ,phase = self.get_bode_for_freq(vpp, f, channel_osc1=channel_osc[1], channel_osc2 =channel_osc[1], channel_gen = channel_gen)
            v_array.append(mag)
            freq_array.append(freq)
            phase_array.append(phase)

        return v_array, freq_array, phase_array

