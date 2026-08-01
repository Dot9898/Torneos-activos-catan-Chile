

import streamlit as st
from constants import DISPLAYED_TOURNEY_INFO_COLUMNS, DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG
from tourney_data import get_display_dataframe, get_cropped_dataframe, get_as_image


def tourney_data_table():
    data = st.session_state['tourney_data']
    st.dataframe(data = get_display_dataframe(data), 
                 hide_index = True, 
                 column_order = DISPLAYED_TOURNEY_INFO_COLUMNS, 
                 column_config = DISPLAYED_TOURNEY_INFO_COLUMN_CONFIG, 
                 placeholder = '-')

def get_tourney_data_image():
    data = st.session_state['tourney_data']
    dataframe = get_cropped_dataframe(data)
    return(get_as_image(dataframe))


