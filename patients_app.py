import pandas as pd
import streamlit as st
from func import *
from pages import page_exploration, page_resultados

st.title("Prototipo Pacientes")
# data_ser = pd.read_csv('data/BDcomunitarioSeroprevalencia.csv')
# data_mol = pd.read_csv('data/pat_df2021GATEWAY.csv')

play = st.sidebar.checkbox('Exploration mode')
if play:
    page_exploration()
else:
        
    page = st.sidebar.selectbox('Pagina',['Serologia Comunitario',
                                'Resultados Moleculares',
                                'Resultados de Sintomáticos',
                                'Encuesta CAP'])

    if page =='Resultados de Sintomáticos':
        page_resultados()
    elif page=='Encuesta CAP':
        page_resultados()