

import streamlit as st
from pathlib import Path
from zoneinfo import ZoneInfo
from matplotlib.font_manager import FontProperties



IS_LIVE_BUILD = True

TABLE_DPI = 700
BACKGROUND_CENTER = 800
NEW_MONTH_DELAY = 3 * 24 * 3600   #Image text starts the next month 3 days in advance
TOURNAMENT_DOWNLOAD_LIMIT = 31 * 24 * 3600
TIME_TOURNAMENTS_ARE_SHOWN_AFTER_STARTING = 24 * 3600
ADRESS_COLUMN_WIDTH_ADJUSTMENT = -20
ALWAYS_SHOW_ONLINE_AFTER_PRESENCIAL = False


DATASHEET_LINK = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQC2ACINwhk_rmvTmliMETVqisjFDfOR5vg_glzDtyz_Vns6G3-0AvkWqmvthq-lQpxbUrt39AaTzRh/pub?output=csv'

ORGANIZATION_NAME = {'challenger': 'Challenger Chile', 
                     'catan_cyc': 'Torneo Catan CyC', 
                     'titanes': 'Titanes de Catan', 
                     'secata': 'La Secata del Catan', 
                     'catanium': 'Catanium', 
                     'juntas_cataneras': 'Juntas Cataneras', 
                     'catan_sur': 'Catan del Sur', 
                     'devir': 'Devir Chile', 
                     'adventure_dreams': 'Adventure Dreams Games', 
                     'guarida_goblins': 'La Guarida de Goblins'}

ORGANIZATION_LINK = {'challenger': 'https://www.instagram.com/challengercatanchile', 
                     'catan_cyc': 'https://www.instagram.com/torneocatancyc', 
                     'titanes': 'https://www.instagram.com/ligatitanesdecyc/', 
                     'secata': 'https://www.instagram.com/lasecatadelcatan/', 
                     'catanium': 'https://catanium.cl/', 
                     'juntas_cataneras': 'https://www.instagram.com/juntascatanerascl/', 
                     'catan_sur': 'https://www.instagram.com/catandelsur/', 
                     'devir': 'https://devir.cl/', 
                     'adventure_dreams': 'https://www.instagram.com/adventuredreamsgames/', 
                     'guarida_goblins': 'https://www.instagram.com/laguaridadegoblins/'}

EXPANSION = {'base': '🌾Base', 
             'cyc': '⚔️Ciudades y caballeros', 
             'incas': '🦙Auge de los incas', 
             'tm': '🐉Tierra maldita'}

ROOT_PATH = Path(__file__).resolve().parent.parent
IMG_PATH = ROOT_PATH / 'assets' / 'img'

CINZEL_PATH = ROOT_PATH / 'assets' / 'fonts' / 'Cinzel-VariableFont.ttf'
CINZEL = FontProperties(fname = CINZEL_PATH)
SOURCE_SANS_PATH = ROOT_PATH / 'assets' / 'fonts' / 'SourceSans3-Medium.ttf'

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
               '⚔️': IMG_PATH / 'swords.png', 
               '🦙': IMG_PATH / 'llama.png', 
               '🐉': IMG_PATH / 'dragon.png'}
BACKGROUND_PATH = IMG_PATH / 'catan_background.png'
TABLE_BACKGROUND_PATH = IMG_PATH / 'catan_table_background.jpg'

DISPLAYED_TOURNEY_INFO_COLUMNS = ['Fecha', 'Región', 'Expansión', 'Nombre', 'Organización', 'Precio', 'Cupos', 'Información', 'Inscripción', 'Dirección']
DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG = {'Precio': st.column_config.MarkdownColumn(alignment = 'right'), 
                                        'Organización': st.column_config.LinkColumn(display_text = '.*#(.*)'), 
                                        'Información': st.column_config.ImageColumn(), 
                                        'Inscripción': st.column_config.LinkColumn(display_text = '↗')} #↗
IMAGE_TOURNEY_INFO_COLUMNS = ['Fecha', 'Región', 'Expansión', 'Nombre', 'Precio', 'Organiza']

RECIEVED_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
DAYS_IN_SPANISH = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MONTHS_IN_SPANISH = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
SANTIAGO_TIMEZONE = ZoneInfo('America/Santiago')







