
import pandas as pd
import numpy as np

df_nutri=pd.read_csv('Data/nutrition_values.csv',sep=';')
def limpieza(df_nutri):
    df_nutri.fillna(value=0, inplace=True)
    df_nutri.replace({'-':int(0), ',':'.'}, inplace=True,regex=True)
    df_nutri=pd.concat([df_nutri.iloc[:,0:3],df_nutri.iloc[:,3:15].astype(float)],axis=1)
    return df_nutri

def filtro_de_salud(x='sodium'):
    
    sugar_safe=df_nutri[df_nutri['Total Sugar (g)']<=31.5]     
    fat_safe=sugar_safe[(sugar_safe['Trans Fat (g)']/sugar_safe['Total Fat (g)'])*sugar_safe['Calories from fat']<=sugar_safe['Calories']*0.01]    
    saturated_fat_safe=fat_safe[(fat_safe['Saturated Fat (g)']/fat_safe['Total Fat (g)'])*fat_safe['Calories from fat']<=fat_safe['Calories']*0.1]
    totalfat_safe=saturated_fat_safe[saturated_fat_safe['Calories from fat']/saturated_fat_safe['Calories']<=30] 
    if x is 'sodium':        
        sodium_safe=totalfat_safe[totalfat_safe['Sodium (mg)']<=2300]
        sodium_safe=sodium_safe[sodium_safe['Serving Size (g)']!=0]
        sodium_safe=sodium_safe[sodium_safe['Item']!=0]        
        sodium_safe['Protein (g)/g of portion']=sodium_safe['Protein (g)']/sodium_safe['Serving Size (g)'] 
        return sodium_safe
    elif x is 'fiber':
        fiber_good=saturated_fat_safe[(saturated_fat_safe['Dietary Fiber (g)']*1000/saturated_fat_safe['Calories'])>=14]
        fiber_good=fiber_good[fiber_good['Serving Size (g)']!=0]
        fiber_good=fiber_good[fiber_good['Item']!=0]        
        fiber_good['Protein (g)/g of portion']=fiber_good['Protein (g)']/fiber_good['Serving Size (g)']
        return fiber_good