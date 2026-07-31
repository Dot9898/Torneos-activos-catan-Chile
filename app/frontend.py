

import streamlit as st
from widgets import tourney_data_table
from style import set_style


st.set_page_config(layout = 'wide')
set_style()



st.title('Torneos activos de catan en Chile', text_alignment = 'center')

tourney_data_table()

