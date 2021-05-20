import streamlit as st
from pages import page_exploration#, page_resultados

st.title("Prototipo Pacientes")

# play = st.sidebar.checkbox('Exploration mode')
try:
    page_exploration()
  
except:
    st.write("""
    Ups!, Algo salió mal.
    """)
    pass

