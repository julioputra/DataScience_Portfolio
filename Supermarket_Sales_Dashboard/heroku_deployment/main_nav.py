import dataviz
import hypotest
import homepage
import streamlit as st 

st.set_page_config(
    page_title="Julio's Milestone",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com/',
        'Report a bug': "https://www.github.com/julioputra",
        'About': "# This is my first milestone!"
    }
)

PAGES = {'Home': homepage,
         'Data Visualization': dataviz,
         'Hypothesis Testing': hypotest,
        }

selected = st.sidebar.selectbox('Pages', list(PAGES.keys()))

page = PAGES[selected]

page.app()