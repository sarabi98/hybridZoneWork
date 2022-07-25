# -*- coding: utf-8 -*-
"""
new plants that flowered each day
"""
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


dire='C:/Users/ferad/OneDrive/Escritorio/hybridZone/WorkField/SheetsData/' #my directory
data=pd.read_csv(dire+'Growing_flowering_dataset.csv') #growing data file
ids=list(dict.fromkeys(data['ID'].tolist()))

data=data.loc[data.groupby('ID')['day'].agg(['idxmin']).stack()].drop_duplicates()

days= [*range(min(data['day']),max(data['day'])+1)]
histogram=[0]*len(days)
for i in data['day'].tolist():
    histogram[i-1]=histogram[i-1]+1
    
dictionary={'Day':days,'Plants':histogram}
floweringPerDay=pd.DataFrame(dictionary)
    
    
plt.figure()
plt.bar(days,histogram)
plt.title('Distribution of flowering plants per day')
plt.xlabel('Days')
plt.ylabel('Number of plants that first flowered per day')