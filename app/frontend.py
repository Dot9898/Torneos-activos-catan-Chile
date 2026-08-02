

import streamlit as st
from style import set_style
from widgets import tourney_data_table, get_tourney_data_image_bytes, table_download_button
from tourney_data import fetch_tourney_data


if 'tourney_data' not in st.session_state:
    st.session_state['tourney_data'] = fetch_tourney_data()
if 'image_bytes' not in st.session_state:
    st.session_state['image_bytes'] = get_tourney_data_image_bytes()

st.set_page_config(layout = 'wide')
set_style()

st.title('Torneos activos de catan en Chile', text_alignment = 'center')

tourney_data_table()

center_spot = st.columns([4, 1, 4])[1]
with center_spot:
    table_download_button()

