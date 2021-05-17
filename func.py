import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap

###### Auxiliar Functions ##############

def pre_processing(df,nombre):
    """
    Recibe un DataFrame y lo entrega 
    listo para la aplicación.
    nombre: pcr, sero, anim, mur, air
    """
    if nombre=='pcr':

        df['RESULTADO PCR'] = df['RESULTADO PCR'].replace({'Pendiente':np.nan,
                                                                'NO LLEGO MUESTRA ':np.nan})#.astype(float)
        df['EDAD'] = df['EDAD'].replace({'NO REGISTRA':np.nan,'71,00':71}).astype(float).astype('Int16')
        df['MUNICIPIO'] = df['MUNICIPIO'].astype(object).replace({1:'Lorica',
                                                                    2:'Planeta Rica',
                                                                    3:'Tierralta',
                                                                    4:'Sahagun',
                                                                    5:'Montelibano',
                                                                    6:'Montería'})                                           
        #df['NOMBRE'] = df['PRIMER NOMBRE']+df['SEGUNDO NOMBRE']+df['PRIMER APELLIDO']+df['SEGUNDO APELLIDO']
    elif nombre=='sero':
        df['MUNICIPIO'] = df['MUNICIPIO'].astype(object).replace({1:'Lorica',
                                                                    2:'Planeta Rica',
                                                                    3:'Tierralta',
                                                                    4:'Sahagun',
                                                                    5:'Montelibano',
                                                                    6:'Montería'}) 
        df['RESULTADO SEROLOGIA'] = df['RESULTADO SEROLOGIA'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan,
                                                                'NO LLEGO MUESTRA ':np.nan}).astype(float)
        df['NOMBRE'] = df['PRIMER NOMBRE']+df['SEGUNDO NOMBRE']+df['PRIMER APELLIDO']+df['SEGUNDO APELLIDO']

    return df

def mun_to_coord(full_ser):
    """
    Recibe un Dataframe con municipios,
     añade sus coordenadas
    y regresa un Dataframe.
    """
    full_ser['lat']=0
    full_ser['lon']=0

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Montería'] = 8.7558921
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Montería'] = -75.887029

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Lorica'] = 9.2394583
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Lorica'] = -75.8139786

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = 8.4076739 
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = -75.5840456 

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Tierralta'] = 8.1717342
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Tierralta'] = -76.059376

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Sahagun'] = 8.9472964
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Sahagun'] = -75.4434972

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Montelibano'] = 7.9800534
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Montelibano'] = -75.4167198

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Cereté'] = 8.8852282
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Cereté'] = -75.7922421

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='San Antero'] = 9.373016
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='San Antero'] = -75.7595056

    return full_ser

def table_target(datos,target,agrupacion='MUNICIPIO',calculation='count'):
    """
    recibe datos, los agrupa por su agrupación, y
    calcula el conteo, o el promedio de los valores únicos asociados
    al target.
    calculation: mean, count.
    """
    
    tabla = pd.DataFrame([])
    datos=pre_processing(datos,'pcr')
    datos = mun_to_coord(datos)
    coords = datos[['lat','lon',agrupacion]].groupby(agrupacion).max()
    

    if calculation=='mean':
        for value in datos[target].unique():
            trace = datos[[target,agrupacion]].loc[datos[target]==value].groupby(agrupacion).mean()
                    
            trace.rename(columns={target:str(value)},inplace=True)

            tabla = pd.concat([tabla, trace],axis = 1)

    else:
        for value in datos[target].unique():
            trace = datos[[target,agrupacion]].loc[datos[target]==value].groupby(agrupacion).count()
                    
            trace.rename(columns={target:str(value)},inplace=True)

            tabla = pd.concat([tabla, trace],axis = 1)
    #
    total = datos[[target,agrupacion]].groupby(agrupacion).count()
    total.rename(columns={target:'total'},inplace=True)

    tabla = pd.concat([coords,tabla,total],axis=1)
    # tabla = tabla.dropna(axis=1)
    # tabla.rename(columns={'2.0':'Negativo','1.0':'Positivo'},inplace=True)
    tabla = tabla.reset_index()
    # print(tabla)
    return tabla


###### Ploting functions ############

def auto_apilado(datos,target,agrupacion,porcentaje=False):
    """
    Esta función recibe un set de datos DataFrame, 
    una variable target, y la variable 
    sobre la que se desean agrupar los datos (eje X).
    Retorna un grafico de barras apilado.
    """
    
    total = datos[[target,agrupacion]].groupby(agrupacion).count()
    tabla = pd.DataFrame([])
    fig = go.Figure()

    #Creamos una traza 
    for value in datos[target].unique():
        trace = datos[[target,agrupacion]].loc[datos[target]==value].groupby(agrupacion).count()
    
        if porcentaje: #Las columnas deben tener el mismo nombre
            trace = 100*trace/total
            y_title ='Porcentaje (Individuos)'
            
        trace.rename(columns={target:str(value)},inplace=True)

        tabla = pd.concat([tabla, trace],axis = 1)

        #Creación de la figura
        fig.add_trace(go.Bar(
            x = tabla.index,
            y = tabla[str(value)],
            name=str(value),
            # marker_color='rgb(26, 118, 255)'
        ))
    y_title='Conteo (Individuos)'
    fig.update_layout(
    title='Conteo de '+str(target)+' agrupado por '+str(agrupacion),
    xaxis_tickfont_size=14,
    yaxis=dict(
        title=y_title,
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title=str(agrupacion)
    ))

    fig.update_layout(barmode='stack')
    return fig, tabla


def mapping_df(df,target,target_value='1.0',heat=False):
    """
    Recibe un Dataframe con Coordenadas y lo grafica
    en un mapa. retorna un html para usar con Iframe.

    Prueba es el tipo de prueba, Serologia o PCR
    an: Booleano para verificar si corresponde a animales
    """
    # df = table_target(full_ser, target)
    
    #Mapa:

    # folium_hmap = folium.Figure(width=500, height=500) No se necesita en st
    m = folium.Map(location=[8.3344713,-75.6666238],
                            width='100%',
                            height='100%',
                            zoom_start=8,#Por defecto es 10
                            tiles="CartoDB positron" #stamentoner#CartoDB positron #dark_matter #OpenSteetMap ,Stamen Toner(Terrain, Watercolor)
                            )#.add_to(folium_hmap)
    data = df
    if heat:
        data['weight'] = data[target_value]/data['total']
        HeatMap(data[['lat','lon','weight']].dropna(),radius=40,blur=25).add_to(m)
    else:
        for i in range(0,len(data)):
            html = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> {target.split(' ')[-1]}: </p>
                    <p>{target_value}: {data.iloc[i][target_value]}</p>
                    <p> Total: {data.iloc[i]['total']}</p>
                    """
            iframe = folium.IFrame(html=html,width=130, height=160)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup,
                radius=float(data.iloc[i]['total'])*500,
                color='lightgray',
                fill=True,
                fill_color='lightgray'
            ).add_to(m)
        # for i in range(0,len(data)): #redundante
            html2 = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> {target.split(' ')[-1]}: </p>
                    <p>{target_value}: {data.iloc[i][target_value]}</p>
                    <p> Total: {data.iloc[i]['total']}</p>
                    """
            iframe2 = folium.IFrame(html=html2,width=130, height=160)
            popup2 = folium.Popup(iframe2, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup2,
                radius=float(data.iloc[i][target_value])*500,
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
    return m

def scatter_matrix(df,dimensions=['SEXO','EDAD'],color='MUNICIPIO'):


    fig = px.scatter_matrix(df,
    dimensions=dimensions,
    color=color,#symbol="MUNICIPIO",
    color_continuous_scale=px.colors.diverging.Temps,#Temps Tropic
    title="Scatter matrix",
    labels={col:col.replace('_', ' ') for col in df[dimensions].columns}) # remove underscore
    fig.update_traces(diagonal_visible=False)
    
    return fig

def scatter_go(df,dimensions=['SEXO','EDAD'],for_text='MUNICIPIO'):
    index_vals = df[for_text].astype('category').cat.codes

    data=go.Splom(
        dimensions=[dict(label=dimension,
                         values=df[dimension]) for
                         dimension in dimensions],
        text=df[for_text],
        marker=dict(color=index_vals,
                    showscale=False, # colors encode categorical variables
                    line_color='white', line_width=0.5)
        )

    fig = go.Figure(data)
    fig.update_layout(
        title='Iris Data set',
        dragmode='select',
        width=600,
        height=600,
        hovermode='closest',
    )
    return fig

def scatter_3d(df,dimensions=['SEXO','EDAD','RESULTADO PCR'],color='MUNICIPIO'):
    fig = px.scatter_3d(df, x=dimensions[0], y=dimensions[1], z=dimensions[2],
              color=color)
    return fig

def line_chart(df,dimensions=['FECHA DE NACIMIENTO ','EDAD'],color='MUNICIPIO'):
    fig = px.line(df, x=dimensions[0], y=dimensions[1], color=color)
    return fig