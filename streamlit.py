import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
from Utils import * 

st.set_page_config(page_title="Obesidad US", page_icon=":electric_plug:", layout="wide")

#variables y constantes
df_nutri=pd.read_csv('Data/nutrition_values.csv',sep=';')


menu = st.sidebar.selectbox("Selecciona la página", ['Home','Obesidad','Nutricion','Datos'])

#Cuando esta en Home
# if menu== 'Home':
#Cuando esta en Obesidad
# if menu=='obesidad':
#     st.write(obesidad_estados_restaurantes(Grafica='mapa'))
#     st.write(obesidad_estados_restaurantes(Grafica='correlacion'))
#     st.write(obesidad_estados_restaurantes(Grafica='obesidad-restaurantes'))
#     st.write(obesidad_ganancia(Grafica=True))
#Cuando esta en nutricion
# if menu=='Nutricion':
#     st.write(nutri_filtro_menu(Datos='sodium'))
#     st.write(nutri_filtro_menu(y=1))
#     st.write(nutri_filtro_menu(Datos='Fiber'))
#     st.write(nutri_filtro_menu(y=2))
#Cuando esta en datos
if menu=='Datos':
    st.write(obesidad_estados_restaurantes(Tabla=True))
    st.write(obesidad_ganancia(Tabla=True))
    st.write(print(df_nutri))
