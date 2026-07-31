

import streamlit as st
from zoneinfo import ZoneInfo


DATASHEET_LINK = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQC2ACINwhk_rmvTmliMETVqisjFDfOR5vg_glzDtyz_Vns6G3-0AvkWqmvthq-lQpxbUrt39AaTzRh/pub?output=csv'

EXPANSION = {'base': '🌾Base', 
             'cyc': '⚔️Ciudades y caballeros'}
ORGANIZATION_NAME = {'challenger': 'Challenger Chile', 
                     'titanes': 'Titanes de Catan'}
ORGANIZATION_LINK = {'challenger': 'https://www.instagram.com/challengercatanchile', 
                     'titanes': 'https://www.instagram.com/torneocatancyc'}

DISPLAYED_TOURNEY_INFO_COLUMNS = ['Fecha', 'Región', 'Expansión', 'Nombre', 'Organización', 'Precio', 'Cupos', 'Información', 'Inscripción', 'Dirección']
DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG = {'Precio': st.column_config.NumberColumn(format = 'dollar'), 
                                        'Organización': st.column_config.LinkColumn(display_text = '.*#(.*)'), 
                                        'Información': st.column_config.ImageColumn(), 
                                        'Inscripción': st.column_config.LinkColumn(display_text = '↗')} #↗

RECIEVED_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'
DAYS_IN_SPANISH = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
SANTIAGO_TIMEZONE = ZoneInfo('America/Santiago')























