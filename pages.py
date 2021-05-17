import pandas as pd
from func import *
import streamlit as st
from streamlit_folium import folium_static


###########Data Import################

data = pd.read_csv('data/sintomaticos.csv')
data_ser = pd.read_csv('data/BDcomunitarioSeroprevalencia.csv')

###########Pages definitions##########
def page_resultados():
    st.sidebar.write('page options')#change sidebar
    fig = auto_apilado(data,'RESULTADO SEROLOGIA','MUNICIPIO',True)
    
    st.plotly_chart(fig)
    st.write('Esta es la descripción de la gráfica')


def page_exploration():
    st.markdown("""
    ## This is the exploratory area
    """)
    t_an = st.sidebar.selectbox('Seleciona tipo de Análisis',options=['Barras',
                                                                      'Mapas',
                                                                      'Correlaciones',
                                                                      '3D',
                                                                      'Lineas'])
    if t_an=='Barras':
        st.sidebar.markdown(
            """
            ### Opciones Gráfico de Barras
            """
        )
        target=st.sidebar.selectbox('Selecciona Objetivo',options=data.columns)
        agrupacion=st.sidebar.selectbox('Selecciona Agrupación',options=data.drop(target,axis=1).columns)
        porcent = st.sidebar.checkbox('Porcentaje')
        fig,tabla_aux = auto_apilado(data,target,agrupacion,porcent)
        st.plotly_chart(fig)
        st.write('Tabla: ',tabla_aux)

    elif t_an=='Mapas':
        st.sidebar.markdown(
            """
            ### Opciones del Mapa
            """
        )
        column = st.sidebar.selectbox('Variable Objetivo',options=data.columns)
        
        table = table_target(data,column)
        target_val = st.sidebar.selectbox('Valor',options=table.columns[3:])
        heat = st.sidebar.checkbox('Mapa de Calor')
        st.markdown('Tabla y Mapa de Conteo para '+str(column))
        st.write(table)
        
        folium_static(mapping_df(table,column,target_val,heat))
    
    elif t_an=='Correlaciones':
        st.sidebar.markdown(
            """
            ### Opciones de Correlación
            """
        )
        vari = data.columns
        var_to_corr = st.sidebar.multiselect('Variables para Correlacionar',
                                    options=[x for x in vari],)
                                    #default=['DO','EDAD'])#DO EDAD
        color_group= st.sidebar.selectbox('Agrupación de Color',
                                        options=vari,
                                        index=1)
        try:
            fig2=scatter_matrix(data,var_to_corr,color_group)#DO EDAD
            st.plotly_chart(fig2)
        except:
            fig2=scatter_matrix(data.dropna(),var_to_corr,color_group)#DO EDAD
            st.plotly_chart(fig2)

    elif t_an=='3D':
        st.sidebar.markdown(
            """
            ### Opciones de Grafico 3D
            """
        )
        vari = data.columns
        eje_x=st.sidebar.selectbox('Eje X',options=vari)
        eje_y=st.sidebar.selectbox('Eje Y',options=vari)
        eje_z=st.sidebar.selectbox('Eje Z',options=vari)

        color_group= st.sidebar.selectbox('Agrupación de Color',
                                        options=vari,
                                        index=1)
        try:
            fig3 = scatter_3d(data,[eje_x,eje_y,eje_z],color_group)
            st.plotly_chart(fig3)
        except:
            fig3 = scatter_3d(data.dropna(),[eje_x,eje_y,eje_z],color_group)
            st.plotly_chart(fig3)

    elif t_an=='Lineas':
        st.sidebar.markdown(
            """
            ### Opciones de Grafico de Líneas
            """
        )
        try:
            fig4 = line_chart(data)
            st.plotly_chart(fig4)
        except:
            fig4 = line_chart(data.dropna())
            st.plotly_chart(fig4)
