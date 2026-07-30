

import streamlit as st
from widgets import tourney_data_table
from style import set_style


st.set_page_config(layout = 'wide')
set_style()

tourney_data_table()

st.write('test')
st.markdown('tt')



