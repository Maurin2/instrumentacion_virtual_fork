#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 10:19:02 2025

@author: facu
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:33:38 2025

@author: facu
"""

"""
IDEA DE TABLA

https://docs.google.com/document/d/1VMYdzl9J-h5e4MDn2IjW-6AdnLMQeB59aEyGwQ72WYY/edit?usp=sharing
"""
# %% DEFINICIONES DE CLASES

class Instrument:
    id_ = 0
    list_ = []
    types_ = ("Osciloscopio", "Generador de funciones", "Fuente de alimentación")
    #Averiguar query para obtener datos de cada equipo (BW, Etc)
    def __init__(self, name, typ):
        
        if(type(name)!=str):
            return
        if(type(typ)!=str):
            return        
        self.name=name
        self.typ=typ
        type(self).list_.append(self)
    
"""
Clase para almacenar datos del equipo a medir
"""
        
class Equipo:
    id_ = 0
    list_ = []
    types_ = ("Filtro BP", "Filtro LP", "Filtro HP")
    
    def __init__(self, name, typ):
        
        if(type(name)!=str):
            return
        if(type(typ)!=str):
            return        
        self.name=name
        self.typ=typ
        type(self).list_.append(self)
        
""""
Clase para almacenar los datos del cliente.
Contiene un atributo donde almacena una instancia Equipo.
"""
class Client:
    id_ = 0
    list_ = []
    
    def __init__(self, name, equipo, date_sol, number):
    #Chequeo de tipos de dato
        if(type(name)!=str):
            return
        if(equipo!=None):
            if(type(equipo)!=Equipo):
                raise TypeError("Error de tipo")
        self.name = name
        self.date_sol = date_sol
        self.number = number
        self.equ = equipo
        
        self.id_ = type(self).id_
        type(self).id_ = type(self).id_ + 1
        
        # self.inst_list = []
        # self.inst_list.append(inst)

"""

Clase MEDICION:
    Contiene elemnto figure y axe de los gráficos a mostrar
    Debe contener tambien valor de RL, cantidad de puntos tomados en el barrido,
    ,nombre del gráfico, voltaje de alimentacion y valor pico de señal
    
    Se puede crear de a un objeto o de a varios, colocando un array en cada uno de los parámetros (menos ou_flag)
    
    Cada instancia tiene un atributo .list_, que es un array que contiene las distintas mediciones con las que fue instanciado
    Si se instancia con un único valor, igualmente se almacena en el atributo .list_ para mayor facilidad de lógica en la función crear reporte

"""
class Medicion:
    list_ = []
    def __init__(self, fig_id, axe_id, RL, n_points, nombre, v_alim, v_s,t,ou_flag = True):
    #Chequeo de tipos de dato
        cls = type(self)
        
        if(type(fig_id)==list and type(axe_id)==list and type(RL)==list and type(nombre)==list and type(n_points)==list and type(v_alim)==list and type(v_s)==list and type(t)==list and len(fig_id)==len(axe_id) == len(RL) == len(nombre) == len(n_points) == len(v_alim)==len(v_s)==len(t)):
            #En un atributo list_, almaceno una lista con las distintas instancias
            self.list_ = []
            for n in range (len(fig_id)):#Creo una instancia por cada grágico y datos pasados (en forma array)
                self.list_.append(Medicion(fig_id= fig_id[n], axe_id = axe_id[n], RL = RL[n], n_points = n_points[n],nombre = nombre[n], v_alim = v_alim[n],v_s = v_s[n],t = t[n],ou_flag = False))
            #A su vez, la clase Medicion posee un atributo list_ donde almacena CADA instancia
            cls.list_.append(self)
            self.id_=len(cls.list_)
            print("Se agregaron "+str(len(self.list_))+" mediciones")
        
        #En el caso de que no sean listas (puede ser objeto único o provenir del init de otro objeto)
        elif(type(fig_id)!=list and type(axe_id)!=list and type(RL)!=list and type(nombre)!=list and type(n_points)!=list and type(v_alim)!=list and type(v_s)!=list and type(t)!=list):
            #Almaceno atributos
            self.fig_id = fig_id
            self.axe_id = axe_id
            self.RL = RL
            self.nombre = nombre
            self.n_points = n_points
            self.v_alim = v_alim
            self.t = t
            self.v_s = v_s
            
            #Si es un objeto que NO se instanció a partir de otra instancia, le condiguro su propia lista y lo agrego a la lista de la clase
            if(ou_flag == True):
                #Para mantener formato de las instancias con múltiples mediciones, almaceno el objeto mismo en el atributo list_
                self.list_=[]
                self.list_.append(self) 
                #Lo agrego a la lista general de la CLASE
                cls.list_.append(self)
                self.id_=len(cls.list_)
                
                print("Se agregó 1 medición")

#%% DEFINICIÓN DE FUNCIÓN CREAR REPORTE
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from parametros import *
from datetime import datetime

"""
RESUMEN de lo módulos REPORTLAB.PLATYPUS:
Con SingleDocTemplate crea un handler al archivo pdf
Para efectivamente CREAR el archivo, se usa la propiedad .build, a la que se le entrega un array con los distintos "elementos" de la hoja
Los elementos son Image, Paragraph y Table
Image contiene la imágen, Paragraph para contener texto y darle estilo, Table para tablas (símil docs)
Table se crea a partir de un array, y con la propiedad TableStyle se la condifgura (alineación, unión de celdas,  bordes, color de fondo)
Por su lado, a los paragraph se le asignan estilos, creaods con ParagraphStyle, en su creación.

RESUMEN CREARREPORTE():
La función utiliza pdf como handler del archivo de salida y elementos[] como array contenedor de los elementos
Todo el contenido mostrado en el pdf se contiene en Tablas
Todo el texto de las tablas se escribe primero en un array, con elementos Paragraph como texto
Las imágenes también se colocan en la el vector generador de la tabla

"""

def CrearReporte(filter_f=True, magn_arr=None, phase_arr=None, client = None, emiter=None, instruments=None, id_report=None, cond_amb= None, mediciones = None):
    #Revisión tipo de datos
    # -------
    #Creo objeto PDF
    if(id_report == None):
        id_report = emiter['id_report']
    pdf_name = "Reporte_"+str(id_report) + ".pdf"
    pdf = SimpleDocTemplate(pdf_name, pagesize=A4)
    col_w = pdf.pagesize[0] - pdf.leftMargin-pdf.rightMargin #En cada tabla, dividir por cantidad de columnas
    elementos = [] #Encapsula los elementos platypus del pdf
    
    #CREO LAS DISTINTAS PARTES DEL DOCUMENTO
    
    #Titulo  = TÍTULO
    Titulo = Paragraph("<u>REPORTE FRA</u>", Titulo_style)
    elementos.append(Titulo)
    
    #Tabla1 = DATOS EMISOR
    datos_t1 = [
            [Paragraph("Datos emisor:",Subtitulo_style) ],
            [Paragraph("Organismo emisor: "+emiter['nombre'], Texto_style), Paragraph("Id_certificado: "+str(id_report), Texto_style)]
            ]
    Tabla1 = Table(datos_t1, colWidths=col_w/len(datos_t1[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE,splitByRow=0)
    Tabla1.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    #El KeepTogether es para que no lo separe en hojas diferentes si no cabe
    elementos.append(KeepTogether([Tabla1]))
    
    
    #Tabla2 = DATOS SOLICITANTE
    datos_t2 = [
            [Paragraph("Datos solicitante:", Subtitulo_style)]
            ,[Paragraph("Nombre: "+client.name, Texto_style), Paragraph("Fecha solicitud: "+client.date_sol, Texto_style), Paragraph("Contacto: "+str(client.number), Texto_style)]
            ]
    Tabla2 = Table(datos_t2, colWidths=col_w/len(datos_t2[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla2.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    elementos.append(KeepTogether([Tabla2]))
    
    #Tabla3 = DATOS EQUIPO
    datos_t3 = [
            [Paragraph("Datos equipo a medir:", Subtitulo_style)]
            ,[Paragraph("Nombre: "+client.equ.name, Texto_style), Paragraph("Tipo: "+client.equ.typ, Texto_style)]
            ]
    Tabla3 = Table(datos_t3, colWidths=col_w/len(datos_t3[1]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla3.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ]))
    elementos.append(KeepTogether([Tabla3]))
    
    #Tabla4 = DATOS MEDICION
    datos_t4 = [
            [Paragraph("Datos medición:", Subtitulo_style)]
            ,[Paragraph("Modelo "+instruments[0].typ+":<br/>"+instruments[0].name, Texto_style), Paragraph("Modelo "+instruments[1].typ+":<br/>"+instruments[1].name,Texto_style), Paragraph("Modelo "+instruments[2].typ+":<br/>"+instruments[2].name, Texto_style)]
            ,[Paragraph("Temperatura ambiente:"+str(cond_amb['Temperatura']), Texto_style), Paragraph("Humedad relativa:"+cond_amb["Humedad"],Texto_style), Paragraph("Presion atmosférica"+ cond_amb["Presion"], Texto_style)]
            ,[Paragraph("Fecha de realización: "+datetime.now().strftime("%d/%m/%Y"),Texto_style), Paragraph("Fecha de emisión: "+ datetime.now().strftime("%d/%m/%Y"),Texto_style)]
            ]
    
    Tabla4 = Table(datos_t4, colWidths=col_w/len(datos_t4[1]), rowHeights=[25, None, None, None],  hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE, splitByRow=0)
    Tabla4.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
        ('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)                
        ,('VALIGN',(0,0),(-1,-1),'TOP')
        ,('TOPPADDING', (0,0), (-1,-1),0)
        ,('BOTTOMPADDING', (0,0), (-1,-1),0)
        ,('TOPPADDING', (0,2), (-1,-1),4)
        ]))
    elementos.append(KeepTogether([Tabla4]))
    elementos.append(PageBreak())
   
    #TablaN = MEDICIONES
    if(mediciones != None):
        i = 0
        for medicion in mediciones.list_:
            string = "foto"+str(i)+".png"
            i+=1
            medicion.axe_id.figure.savefig(string)
            img = Image(string, width=IMG_W, height=IMG_H)

            datos_tN = [
                [Paragraph(str(medicion.nombre),Subtitulo2_style)]
                ,[Paragraph("Valimentación: "+str(medicion.v_alim)+"V"+SPACE+"Vseñal: "+str(medicion.v_s)+"V"+SPACE+"Tiempo de toma: "+str(medicion.t)+"s"+SPACE+"Numero de puntos: "+str(medicion.n_points)+"pts"+SPACE+"Resistencia de carga: "+str(medicion.RL)+"ohm", Texto_style)]
                ,[Paragraph("Fci:"+"FrecCorteInf"+"Hz",Texto_style),Paragraph("Fcs: "+"FrecCorteSup"+"Hz", Texto_style)]
                ,[img]
                ]
            TablaN = Table(datos_tN, colWidths=col_w/len(datos_tN[2]), hAlign='CENTER', spaceAfter=SPACE_AFTER, spaceBefore=SPACE_BEFORE)
            TablaN.setStyle(TableStyle([ #SE ANOTA (COL,ROW)
                ('BACKGROUND',(0,0),(-1,0),colors.lightblue)
                ,('SPAN', (0,0), (-1,0)) #Uno celda principal (titulo de tabla)
                ,('SPAN', (0,1), (-1,1)) #Uno segunda fila (especificaciones)
                ,('SPAN', (0,-1), (-1,-1)) 
                ,('VALIGN',(0,0),(-1,-1),'TOP')
                ,('ALIGN',(0,0),(-1,-1),'CENTER')
                ,('TOPPADDING', (0,0), (-1,-1),0)
                ,('BOTTOMPADDING', (0,0), (-1,-1),0)
                ,('TOPPADDING', (0,2), (-1,-1),4)
                ,("BOX", (0,0), (-1,-1), 2, colors.black)  
               ]))
            elementos.append(KeepTogether([TablaN]))
    
    pdf.build(elementos)
    return print("Terminado el documento "+str(pdf_name))

#%% Ejemplo para probaro
"""
En python cuando importas un archivo, lo ejecuta todo... con esto lo evito.
"""
if __name__ == "__main__":

    
    osc_2102 = Instrument(name="SDS 2102", typ="Osciloscopio")
    gen_1032 = Instrument(name="SDG 1032X", typ="Generador de funciones")
    fuente_vcc = Instrument(name="FUENTE", typ="Fuente de alimentación")
    
    equipo_de_jose = Equipo(name="Equipo de jose", typ="Fltro BP")
    jose = Client(name="Juan",equipo = equipo_de_jose, date_sol = datetime.now().strftime("%d/%m/%Y"), number = 1123344556)
    
    condiciones_amb = {"Temperatura":"22°C", "Humedad":"56%","Presion":"1atm"}
    
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
    medido = Medicion(fig_id=[axes1[0].figure,axes2[0].figure], axe_id=[axes1[0],axes2[0]], RL=RL, n_points=n_points, nombre=name, v_alim=v_alim, v_s=v_s, t=t) #Objeto medición
    
    
    CrearReporte(client = jose, emiter = Emisor, instruments=[osc_2102,gen_1032,fuente_vcc],cond_amb = condiciones_amb, mediciones= medido)        