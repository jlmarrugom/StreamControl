import pandas as pd
from func import *
import streamlit as st
from streamlit_folium import folium_static
###########Data Import################


# data_ser = pd.read_csv('data/BDcomunitarioSeroprevalencia.csv')
def data_selector():
    which = st.sidebar.selectbox('Set de Datos',['Pacientes',
                                                 'Animales',
                                                 'Aire',
                                                 'Murcielagos'])
    
    if which =='Pacientes':
        return pd.read_csv('data/sintomaticos.csv')
        # return pd.read_csv('data/asintomáticas_05_26_2021.csv',sep=';',error_bad_lines=False,encoding='latin-1')
    elif which=='Animales':
        return pd.read_csv('data/animales_domesticos.csv')
        # return pd.read_csv('data/Animales domésticos_05_26_2021.csv',sep=';',error_bad_lines=False,encoding='latin-1')
    elif which=='Aire':
        # return pd.read_csv('data/aire(IPS)_05_26_2021.csv',sep=';',error_bad_lines=False,encoding='latin-1')
        cual = st.sidebar.selectbox('Campaña:',['Primera',
                                                'Segunda',
                                                'Exteriores'])
        if cual=='Primera':#de comas a puntos, NA a ' ' y negativo a 0
            return pd.read_csv('data/bdmp_primera.csv')
        elif cual=='Segunda':
            return pd.read_csv('data/bdmp_segunda.csv')
        else:
            return pd.read_csv('data/bdmp_exteriores.csv')#,sep=';'
    else:
        return pd.read_csv('data/BasedeDatosMurcielagosCórdoba_Dic2020.csv')
    
###########Pages definitions##########

def page_exploration():
    file = st.sidebar.file_uploader('Sube aquí los datos para Analizar',type=["csv"])

    if file!=None:
        try:
            file.seek(0)
            data = pd.read_csv(file,index_col=0,error_bad_lines=False)
        except:
            file.seek(0)
            data = pd.read_csv(file,index_col=0,error_bad_lines=False,sep=';',encoding='latin-1')

    else:
        data = data_selector()

    st.markdown("""
    ## This is the exploratory area
    """)
    t_an = st.sidebar.selectbox('Seleciona tipo de Análisis',options=['Barras',
                                                                      'Mapas',
                                                                      'Relaciones',
                                                                      '3D',
                                                                      'Lineas'])
    if t_an=='Barras':
        st.sidebar.markdown(
            """
            ### Opciones Gráfico de Barras
            """
        )
        target=st.sidebar.selectbox('Selecciona Objetivo',options=data.columns,index=4)
        agrupacion=st.sidebar.selectbox('Selecciona Agrupación',options=data.drop(target,axis=1).columns,index=3)
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
        mun = st.sidebar.selectbox('Variable Lugar',data.columns)
        column = st.sidebar.selectbox('Variable Objetivo',options=data.columns,index=3)
        table = table_target(data,column,mun)
        target_val = st.sidebar.selectbox('Valor',options=table.columns[3:])
        heat = st.sidebar.checkbox('Mapa de Calor')
        st.markdown('Tabla y Mapa de Conteo para '+str(column))
        st.write(table)
        
        try:
            #st.plotly_chart(map_express(data))
            folium_static(mapping_df(table,column,target_val,heat))
        except:
            st.write('No se encuentra Ubicación')
    
    elif t_an=='Relaciones':
        st.sidebar.markdown(
            """
            ### Opciones de Relación
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
            fig2=scatter_matrix(data.dropna(subset=var_to_corr),var_to_corr,color_group)#DO EDAD
            st.plotly_chart(fig2)
        col1,col2 = st.beta_columns(2)
        with col1:
            c,p =corrs(data.dropna(subset=var_to_corr),var_to_corr)
            st.write('Pearson (Lineal) Correlation')
            st.write(c)
            st.write('Pearson (Lineal) P-value')
            st.write(p)
        with col2:   
            cs,ps = corrs(data.dropna(subset=var_to_corr),var_to_corr,method='spearman',json=False)
            st.write('Spearman (Monotonic) Correlation')
            st.write(cs)
            st.write('Spearman (Monotonic) P-value')
            st.write(ps)
        


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
            fig3 = scatter_3d(data.dropna(subset=[eje_x,eje_y,eje_z]),[eje_x,eje_y,eje_z],color_group)
            st.plotly_chart(fig3)

    elif t_an=='Lineas':
        st.sidebar.markdown(
            """
            ### Opciones de Grafico de Líneas
            """
        )
        vari = data.columns
        ejex=st.sidebar.selectbox('X',options=vari)
        ejey=st.sidebar.selectbox('Y',options=vari)
        color_group2= st.sidebar.selectbox('Agrupación',
                                        options=vari,
                                        index=1)
        try:
            fig4 = line_chart(data,[ejex,ejey],color_group2)
            st.plotly_chart(fig4)
        except:
            fig4 = line_chart(data.dropna(subset=[ejex,ejey]),[ejex,ejey],color_group2)
            st.plotly_chart(fig4)
        st.write(data[[ejex,ejey,color_group2]].head(10))