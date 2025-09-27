#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 12:08:45 2025

@author: facu
"""
from reportlab.lib.styles import  ParagraphStyle


Emisor = {'nombre':'Grupo2', 'id_report':'AA00'}
EMITER_NAME = "Grupo 2"
COL_W = 150
ROW_H= 20
ID_REPORT = "AA00"
TEXT_SIZE = 9
SUBT_SIZE = 10
TIT_SIZE = 20
TEXT_FONT = "Times-Roman"
SUBT_FONT = "Times-Bold"
TIT_FONT = "Times-Bold"
SPACE_BEFORE = 5
SPACE_AFTER = 0
SPACE = "&nbsp;&nbsp;&nbsp;&nbsp;"
IMG_W = 300
IMG_H = IMG_W*3/4


Texto_style = ParagraphStyle(
    'Texto Normal',
    fontName=TEXT_FONT,
    alignment = 0,
    spaceBefore=0,
    spaceAfter=0,
    fontSize=TEXT_SIZE
    )
Titulo_style = ParagraphStyle(
    'Titulo',
    fontName=TIT_FONT,
    alignment = 1,
    spaceBefore=0,
    spaceAfter=30,
    fontSize=TIT_SIZE
    )
Subtitulo_style = ParagraphStyle(
    'Subitulo',
    fontName=SUBT_FONT,
    alignment = 0,
    spaceBefore=0,
    spaceAfter=0,
    fontSize=SUBT_SIZE
    )

Subtitulo2_style = ParagraphStyle(
    'Subitulo',
    fontName=SUBT_FONT,
    alignment = 1,
    spaceBefore=0,
    spaceAfter=0,
    fontSize=SUBT_SIZE
    )