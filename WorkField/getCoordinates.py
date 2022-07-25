"""
Get coordinates from previous day to form new sheet
"""
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

dire='C:/Users/ferad/OneDrive/Escritorio/hybridZone/WorkField/SheetsData/'
ids=pd.read_csv(dire+'day60.csv') #ñprevious day file
ids=ids['ID'].tolist()
veg=pd.read_csv(dire+'2022_veg_trait_data_new_coords_habitat.csv')

x=[]
y=[]
h=[]
missing=[]
dis=[]
prev=0
for i in ids:
    try:
        new=float(veg.loc[veg['ID']==i]['x'])
        x.append(new)
        dis.append(round(abs(new-prev),2))
        prev=new
        # y.append(float(veg.loc[veg['ID']==i]['y']))
        # h.append(float(veg.loc[veg['ID']==i]['h']))
    except:
        x.append(' ')
        dis.append(' ')
        missing.append(i)
        # y.append('missing')
        # h.append('missing')
        # print(veg['ID']==i)
        # print(veg.loc[veg['ID']==i]['x'])

notSheet=[]        
for i in veg['ID']:
    if not i in ids:
        notSheet.append(i)
        
        
    
dictionary={'ID':ids,'x':dis}
# dictionary={'ID':ids,'x':x,'y':y,'h':h}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('IDsCoordinates.csv')
