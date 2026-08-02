

import streamlit as st
import constants
from tourney_data import get_display_dataframe, get_cropped_dataframe, get_last_monday_string
from dataframe_to_image import convert_to_image_bytes, add_background_and_title


def tourney_data_table():
    data = st.session_state['tourney_data']
    st.dataframe(data = get_display_dataframe(data), 
                 hide_index = True, 
                 column_order = constants.DISPLAYED_TOURNEY_INFO_COLUMNS, 
                 column_config = constants.DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG, 
                 placeholder = '-')

def get_tourney_data_image_bytes():
    data = st.session_state['tourney_data']

    dataframe = get_cropped_dataframe(data)
    table_bytes = convert_to_image_bytes(dataframe, constants.IMAGE_STYLE, constants.EMOJI_PATHS)
    background_bytes = constants.TABLE_BACKGROUND_PATH.read_bytes()
    font_bytes = constants.CINZEL_PATH.read_bytes()

    title = 'Torneos activos de catan'
    subtitle = f'Semana del {get_last_monday_string()}'

    image_bytes = add_background_and_title(table_bytes, 
                                           background_bytes, 
                                           font_bytes, 
                                           title, 
                                           subtitle, 
                                           constants.BACKGROUND_CENTER)
        
    return(image_bytes)

def table_download_button():
    image_bytes = st.session_state['image_bytes']
    file_name = f'Torneos catan semana {get_last_monday_string()}.png'
    st.download_button('Compartir', 
                       image_bytes, 
                       file_name = file_name, 
                       mime = 'image/png', 
                       width = 'stretch')



