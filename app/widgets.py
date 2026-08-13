

import streamlit as st
import constants
from tourney_data import get_display_dataframe, get_cropped_dataframe, get_current_month_string, get_column_width
from dataframe_to_image import convert_to_image_bytes, add_background_and_title


def add_column_width(config, dataframe, column_name, adjustment = 0):
    width = get_column_width(dataframe[column_name])
    if width is None:
        return
    config[column_name] = st.column_config.MarkdownColumn(width = width + adjustment)

def tourney_data_table():
    data = st.session_state['processed_data']
    display = get_display_dataframe(data)
    config = constants.DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG
    add_column_width(config, display, 'Dirección', adjustment = constants.ADRESS_COLUMN_WIDTH_ADJUSTMENT)

    st.dataframe(data = display, 
                 hide_index = True, 
                 column_order = constants.DISPLAYED_TOURNEY_INFO_COLUMNS, 
                 column_config = config, 
                 placeholder = '-', 
                 width = 'stretch', 
                 height = 'content')

def get_tourney_data_image_bytes():
    data = st.session_state['processed_data']

    dataframe = get_cropped_dataframe(data)
    table_bytes = convert_to_image_bytes(dataframe, constants.IMAGE_STYLE, constants.EMOJI_PATHS)
    background_bytes = constants.TABLE_BACKGROUND_PATH.read_bytes()
    font_bytes = constants.CINZEL_PATH.read_bytes()

    title = 'Torneos activos de catan'
    subtitle = f'{get_current_month_string(delay = constants.NEW_MONTH_DELAY)} 2026'

    image_bytes = add_background_and_title(table_bytes, 
                                           background_bytes, 
                                           font_bytes, 
                                           title, 
                                           subtitle, 
                                           constants.BACKGROUND_CENTER)
    
    return(image_bytes)

def table_download_button():
    image_bytes = st.session_state['image_bytes']
    file_name = f'Torneos catan {get_current_month_string(delay = constants.NEW_MONTH_DELAY)} 2026.png'
    st.download_button('Compartir', 
                       image_bytes, 
                       file_name = file_name, 
                       mime = 'image/png', 
                       width = 'stretch')



