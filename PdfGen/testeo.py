#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 12:05:59 2025

@author: facu
"""
#%% Módulos externos
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from reportlab.lib import colors

#%% Funciones, métodos y constantes para la creación de reportes
from parametros import *
from clases_funciones_ import Instrument, Client, Equipo, Medicion, CrearReporte

# %%Generación de bodeplots de fase y módulo para testear
import numpy as np
from scipy import signal as sig

def graficar_H (H1, n=500):
    if(type(H1)!=None):
        w, mag_db, phase_deg = sig.bode(H1, n)  # w en rad/s
        fig, axes = plt.subplots(2,1)
        axes[0].semilogx(w, mag_db)
        axes[0].set_ylabel('Magnitud (dB)')
        axes[1].semilogx(w,phase_deg)
        axes[1].set_ylabel('Fase (deg)')
        axes[0].set_xlabel('Frecuencia (rad/s)')
        axes[1].set_xlabel('Frecuencia (rad/s)')
        axes[0].grid(True)
        axes[1].grid(True)
        plt.show()
        return axes
    else:
        raise TypeError("No es T.F.")
        
r=0;r1=1;r3=2;r4=3;r5=4
res=[20.,1.,1.,1.,1.]
c=0;c2=1
cap=[1.,1.]
res=np.array(res);
cap=np.array(cap);
num_des = np.array([ 1/(res[r]*cap[c]) *(1+res[r4]/res[r5]), 0.] )
den_des = np.array([ 1., 1/(res[r]*cap[c]), res[r4]/(res[r1]*res[r3]*res[r4]*cap[c2])*1/cap[c]])
H1_des = sig.TransferFunction( num_des, den_des )
axes1 = graficar_H(H1_des)
    
n=3
att_min=16
att_max=0.5
wc=1
ws=3
H_C_ba=sig.cheby1(n, att_max, wc, btype='lowpass', analog=True, output='ba', fs=None)
H_C = sig.TransferFunction(H_C_ba[0],H_C_ba[1])
axes2 = graficar_H(H_C)

#%% Testeo persé
name =["NOTCHN'T","CHEBY"] #Título de los gráficos
RL = [1, 2] #Valores de R de carga
n_points = [100, 100] #Cantidad de puntos utilizados
v_alim = [5,5] #Voltaje alimentación
v_s = [1e-3, 1e-3] #Valor pico de la señal senoidal de barrido
t=[1,10] # Tiempo de duración del estudio
osc_2102 = Instrument(name="SDS 2102", typ="Osciloscopio") #Osciloscopio a utilizar
gen_1032 = Instrument(name="SDG 1032X", typ="Generador de funciones") #Generador a utilizar
fuente_vcc = Instrument(name="FUENTE", typ="Fuente de alimentación") #Fuente a utilizar

equipo_de_jose = Equipo(name="Equipo de jose", typ="Fltro BP")#Equipo/circuito a medir
jose = Client(name="Juan",equipo = equipo_de_jose, date_sol = datetime.now().strftime("%d/%m/%Y"), number = 1123344556) #Datos del cliente
condiciones_amb = {"Temperatura":"22°C", "Humedad":"56%","Presion":"1atm"} #Condiciones ambientales (INTENAREMOS QUE SE BUSQUEN AUTOMÁTICAMENTE DESDE LA WEB)
medido = Medicion(fig_id=[axes1[0].figure,axes2[0].figure], axe_id=[axes1[0],axes2[0]], RL=RL, n_points=n_points, nombre=name, v_alim=v_alim, v_s=v_s, t=t) #Objeto medición
id_report = "FRA"
#CrearReporte(filter_f=True, magn_arr=None, phase_arr=None, client = None, emiter=None, instruments=None, id_report=None, cond_amb= None, mediciones = None):
CrearReporte(id_report = id_report, client = jose, emiter = Emisor, instruments=[osc_2102,gen_1032,fuente_vcc],cond_amb = condiciones_amb, mediciones= medido)        