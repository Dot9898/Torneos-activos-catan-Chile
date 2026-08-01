

import streamlit as st
from style import set_style
from widgets import tourney_data_table#, get_tourney_data_image
from tourney_data import fetch_tourney_data


if 'tourney_data' not in st.session_state:
    st.session_state['tourney_data'] = fetch_tourney_data()


st.set_page_config(layout = 'wide')
set_style()

st.title('Torneos activos de catan en Chile', text_alignment = 'center')

tourney_data_table()








import streamlit.components.v1 as components


def dataframe_download_button(styled_df):

    table_html = styled_df.to_html()

    components.html(
        f"""
        <div id="export-container">
            {table_html}
        </div>

        <button onclick="downloadImage()">
            Download PNG
        </button>

        <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>

        <script>
        async function downloadImage() {{
            const element = document.getElementById("export-container");

            const canvas = await html2canvas(element, {{
                scale: 2
            }});

            const link = document.createElement("a");
            link.download = "dataframe.png";
            link.href = canvas.toDataURL("image/png");
            link.click();
        }}
        </script>
        """,
        height=200,
    )


def style_df(dataframe):

    dataframe = dataframe.style.set_properties(
        **{
            "background-color": "#FF0000",
            "color": "#3D3024",
        }
    )

    return(dataframe)



from tourney_data import get_cropped_dataframe
data = st.session_state['tourney_data']
dataframe = get_cropped_dataframe(data)
#styled_df = style_df(dataframe)
#dataframe_download_button(styled_df)

from dataframe_to_image import convert_to_image_bytess
from constants import IMAGE_STYLE
image = convert_to_image_bytess(dataframe, IMAGE_STYLE)
st.image(image)






