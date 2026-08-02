

import streamlit as st
from pathlib import Path
from zoneinfo import ZoneInfo
from matplotlib.font_manager import FontProperties



TABLE_DPI = 700
BACKGROUND_CENTER = 800


DATASHEET_LINK = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQC2ACINwhk_rmvTmliMETVqisjFDfOR5vg_glzDtyz_Vns6G3-0AvkWqmvthq-lQpxbUrt39AaTzRh/pub?output=csv'

EXPANSION = {'base': '🌾Base', 
             'cyc': '⚔️Ciudades y caballeros'}
ORGANIZATION_NAME = {'challenger': 'Challenger Chile', 
                     'titanes': 'Titanes de Catan'}
ORGANIZATION_LINK = {'challenger': 'https://www.instagram.com/challengercatanchile', 
                     'titanes': 'https://www.instagram.com/torneocatancyc'}

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'assets' / 'img'

CINZEL_PATH = ROOT_PATH / 'assets' / 'fonts' / 'Cinzel-VariableFont.ttf'
CINZEL = FontProperties(fname = CINZEL_PATH)

IMAGE_STYLE = {'header_background_color': '#F5E3A3', 
               'header_separator_color': '#e1d198', 
               'header_font': CINZEL, 
               'header_font_color': '#827c68', 
               'header_font_size': 12, 
               'header_font_weight': 600, 

               'cell_background_color': '#f6df82', 
               'cell_separator_color': '#e2cd7b', 
               'cell_font': CINZEL, 
               'cell_font_color': '#31333f', 
               'cell_font_size': 10, 
               'cell_font_weight': 500, 

               'separator_width': 1.0, 
               'row_height': 0.35, 
               'row_padding_x': 0.07, 
               'corner_radius': 0.1, 
               'emoji_text_spacing': 0.05, 
               'dpi': TABLE_DPI}

EMOJI_PATHS = {'🌾': IMG_PATH / 'wheat.png', 
               '⚔️': IMG_PATH / 'swords.png'}
BACKGROUND_PATH = IMG_PATH / 'catan_background.png'
TABLE_BACKGROUND_PATH = IMG_PATH / 'catan_table_background.jpg'

DISPLAYED_TOURNEY_INFO_COLUMNS = ['Fecha', 'Región', 'Expansión', 'Nombre', 'Organización', 'Precio', 'Cupos', 'Información', 'Inscripción', 'Dirección']
DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG = {'Precio': st.column_config.NumberColumn(format = 'dollar'), 
                                        'Organización': st.column_config.LinkColumn(display_text = '.*#(.*)'), 
                                        'Información': st.column_config.ImageColumn(), 
                                        'Inscripción': st.column_config.LinkColumn(display_text = '↗')} #↗
IMAGE_TOURNEY_INFO_COLUMNS = ['Fecha', 'Región', 'Expansión', 'Nombre', 'Precio', 'Cupos', 'Organiza']

RECIEVED_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
DAYS_IN_SPANISH = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MONTHS_IN_SPANISH = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
SANTIAGO_TIMEZONE = ZoneInfo('America/Santiago')







