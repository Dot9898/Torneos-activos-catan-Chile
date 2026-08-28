

import streamlit as st
from style import set_style
from widgets import show_online_tournaments_checkbox, tourney_data_table, get_tourney_data_image_bytes, table_download_button
from tourney_data import fetch_tourney_data, get_processed_dataframe
from screen_mode import get_screen_mode


if 'screen_mode' not in st.session_state:
    st.session_state['screen_mode'] = get_screen_mode()
    st.rerun()
if 'tourney_data' not in st.session_state:
    st.session_state['tourney_data'] = fetch_tourney_data()
if 'processed_data' not in st.session_state:
    st.session_state['processed_data'] = get_processed_dataframe(st.session_state['tourney_data'])
if 'image_bytes' not in st.session_state:
    st.session_state['image_bytes'] = get_tourney_data_image_bytes()

st.set_page_config(layout = 'wide')
set_style()


if st.session_state['screen_mode'] == 'desktop':
    st.title('Torneos activos de catan en Chile', text_alignment = 'center')
else:
    st.header('Torneos activos de catan en Chile', text_alignment = 'center')

show_online_tournaments_checkbox()

tourney_data_table()

center_spot = st.columns([2, 1, 2])[1]
with center_spot:
    table_download_button()


st.title('')
st.caption('Por un nivel competitivo de catan en Chile  \nContacto para agregar torneos: +569 9439 1384', text_alignment = 'right')
