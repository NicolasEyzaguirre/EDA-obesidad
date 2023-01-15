import folium 
import os
from folium import plugins
import geocoder 
import geopy 
import numpy as np
import pandas as pd
from vega_datasets import data as vds 
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def nutri_filtro_menu(x='Tablas' , y= 0):
    df_nutri=pd.read_csv('Data/nutrition_values.csv',sep=';')
    df_nutri.fillna(value=0, inplace=True)
    df_nutri.replace({'-':int(0), ',':'.'}, inplace=True,regex=True)
    df_nutri=pd.concat([df_nutri.iloc[:,0:3],df_nutri.iloc[:,3:15].astype(float)],axis=1)

    sugar_safe=df_nutri[df_nutri['Total Sugar (g)']<=31.5]     
    fat_safe=sugar_safe[(sugar_safe['Trans Fat (g)']/sugar_safe['Total Fat (g)'])*sugar_safe['Calories from fat']<=sugar_safe['Calories']*0.01]    
    saturated_fat_safe=fat_safe[(fat_safe['Saturated Fat (g)']/fat_safe['Total Fat (g)'])*fat_safe['Calories from fat']<=fat_safe['Calories']*0.1]
    totalfat_safe=saturated_fat_safe[saturated_fat_safe['Calories from fat']/saturated_fat_safe['Calories']<=30] 
    sodium_safe=totalfat_safe[totalfat_safe['Sodium (mg)']<=2300]

    sodium_safe=sodium_safe[sodium_safe['Serving Size (g)']!=0]
    sodium_safe=sodium_safe[sodium_safe['Item']!=0]        
    sodium_safe['Protein (g)/g of portion']=sodium_safe['Protein (g)']/sodium_safe['Serving Size (g)']

    fiber_good=saturated_fat_safe[(saturated_fat_safe['Dietary Fiber (g)']*1000/saturated_fat_safe['Calories'])>=14]
    fiber_good=fiber_good[fiber_good['Serving Size (g)']!=0]
    fiber_good=fiber_good[fiber_good['Item']!=0]        
    fiber_good['Protein (g)/g of portion']=fiber_good['Protein (g)']/fiber_good['Serving Size (g)'] 

    if x == 'Tablas':        
 
        if y == 1:
            plt.figure()
            plt.rcParams.update({'font.size': 12}) 
            sodium_safe.sort_values(by='Protein (g)/g of portion').plot.barh(x='Item',y='Protein (g)/g of portion', figsize=(15,15), stacked=True);
        elif y ==2:
            fiber_good.sort_values(by='Protein (g)/g of portion').plot.barh(x='Item',y='Protein (g)/g of portion', figsize=(15,15), stacked=True);
        else:
            return print('seleccione una tabla')
    
    if x == 'sodium':        
                    
        return sodium_safe
        

    elif x == 'fiber':
        
        return fiber_good

def obesidad_estados_restaurantes(Grafica='nada',Tabla=False):
    df_USA=pd.read_csv('Data/National_Obesity_By_State.csv')
    Res_estado=pd.read_csv('Data/Cantidad_Res.csv')
    Pob_estado=pd.read_csv('Data/NST-EST2022-ALLDATA.csv')
    df_GDP_Ob=pd.read_csv('Data/Obesity_GDP_PanelData.csv')

    Pob_estado.rename(columns = {'NAME':'State'}, inplace = True)  
    Pob_estado.rename(columns = {'ESTIMATESBASE2020':'Population'}, inplace = True)
    df_USA.rename(columns = {'NAME':'State'}, inplace = True)
    Res_estado.replace({'State': {'Idaho\t': 'Idaho', 'Maine\t': 'Maine'}},inplace=True)
    Res_estado.rename(columns = {'All Fast Food RES':'All-Fast-Food-RES per-100k'}, inplace = True)
    df1=df_GDP_Ob[df_GDP_Ob['Year'] == 2017]
    
    df_Usa_GDP_Ob=pd.merge(df_USA, df1)
    df_Usa_GDP_Ob.rename(columns = {'Population':'POP'}, inplace = True)

    pob_res_estado=pd.merge(Pob_estado, Res_estado)
    Data_1=pd.merge(df_Usa_GDP_Ob, pob_res_estado)
    
    Data_1.drop(['Obesity','SHAPE_Area','FID','Real.GDP.Growth','YearFE','SHAPE_Length','Region.Encoding','Region','POP',
            'Real.GDP.Growth*100','Unit','Real.Personal.Income','Average.Age','Full-service Res',
            'SUMLEV', 'REGION', 'DIVISION', 'STATE','POPESTIMATE2021','POPESTIMATE2020', 'POPESTIMATE2022', 'NPOPCHG_2020',
            'NPOPCHG_2021', 'NPOPCHG_2022', 'BIRTHS2020', 'BIRTHS2021',
            'BIRTHS2022', 'DEATHS2020', 'DEATHS2021', 'DEATHS2022',
            'NATURALCHG2020', 'NATURALCHG2021', 'NATURALCHG2022',
            'INTERNATIONALMIG2020', 'INTERNATIONALMIG2021', 'INTERNATIONALMIG2022',
            'DOMESTICMIG2020', 'DOMESTICMIG2021', 'DOMESTICMIG2022', 'NETMIG2020',
            'NETMIG2021', 'NETMIG2022', 'RESIDUAL2020', 'RESIDUAL2021',
            'RESIDUAL2022', 'RBIRTH2021', 'RBIRTH2022', 'RDEATH2021', 'RDEATH2022',
            'RNATURALCHG2021', 'RNATURALCHG2022', 'RINTERNATIONALMIG2021',
            'RINTERNATIONALMIG2022', 'RDOMESTICMIG2021', 'RDOMESTICMIG2022',
            'RNETMIG2021', 'RNETMIG2022'], axis=1,inplace=True)
   
    Data_1['Population with obesity']=round(Data_1['Population']*Data_1['Adult.Obesity']) 
    Data_1['All fast food']=round(pob_res_estado['Population']*pob_res_estado['All-Fast-Food-RES per-100k']/100000)
    
    if Tabla == True:

        return Data_1

    if Grafica== 'mapa':
        m = folium.Map(location=[40, -95], zoom_start=4)
        folium.Choropleth(
            geo_data='Data/us-state-boundaries.json',
            name="choropleth",
            data=Data_1,
            columns=['State','Population with obesity'],
            key_on='feature.properties.name',
            fill_color="YlGn",
            fill_opacity=0.7,
            legend_name="restaurantes (%)",
        ).add_to(m)

        folium.LayerControl().add_to(m)

        print(m)
    elif Grafica== 'correlacion':
        Data_state_1=Data_1.set_index('State')
        plt.figure(figsize=(15,15))
        sns.heatmap(Data_state_1.corr(),
            vmin=-1,
            vmax=1,
            cmap=sns.diverging_palette(145, 280, s=85, l=25, n=7),
            square=True,
            annot=True);
            
    elif Grafica== 'obesidad-restaurantes':
       Data_1_ord=Data_1.sort_values('Population with obesity',ascending=False)
       ax = sns.relplot(data=Data_1_ord,
                x="All fast food",
                y="State",
                hue="Population with obesity", size="Population",
                sizes=(100, 1000),
                alpha=.8, palette="autumn",
                legend='brief',
                height=10);
def obesidad_ganancia(Grafica=False,Tabla=False):
    df_adults_Ob=pd.read_csv('Data/percent_of_adults_with_obesity_usafacts.csv')
    df_adults_Ob.drop_duplicates('Years', keep="last",inplace=True)
    Df1_adult_ob=df_adults_Ob.set_index('Years')
    obesidad_ganancia_anual=Df1_adult_ob.iloc[17:22,16:]
    obesidad_ganancia_anual=obesidad_ganancia_anual.reset_index()
    if Tabla == True:

        return obesidad_ganancia_anual

    if Grafica== True:
        Obesidad_G_anual=obesidad_ganancia_anual.set_index('Years')
        Obesidad_G_anual.plot(kind='barh',figsize=(20,7))

        plt.ylabel("2017")
        plt.xlabel("Ratio Obesidad")