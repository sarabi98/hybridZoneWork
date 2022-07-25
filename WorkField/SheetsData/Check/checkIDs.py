"""
CHECK DATA PHOTOS, GROWING DATA, VEG TRAITS

c=list((set(a).difference(b)))  #in a not in b
c=list(set(a).intersection(set(b))) #in both a and b


PCs=flowered[x=='yes' for x in PCs]
 recordPCs=PCs['ID'].value_counts() 
recordVeg=veg['ID'].value_counts()        #checking duplicates in veg

"""

import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

####################################################from terminal
# dire = input("Copy and paste file's directory: ")
# dire=dire.replace('/', '\\') #check change in directory writting
# print('All files most be in the same directory, enter the name of the files (include .csv):')
# veg_original =input("Veg trait data: ")
# growingData=input("Growing Data: ")
# photo=input("This year pictures: ")
# photo2021=input("Last year pictures: ")


# mi directorio
dire='C:/Users/ferad/OneDrive/Escritorio/hybridZone/WorkField/SheetsData/'
veg_original=pd.read_csv(dire+'2022_veg_trait_data_new_coords_habitat.csv')
growingData=pd.read_csv(dire+'Growing_flowering_dataset.csv')
photo=pd.read_csv(dire+'HZPhotoscores2022.csv')
photo2021=pd.read_csv(dire+'20210801_HZphotoscores2021.csv')

veg=veg_original.copy()

photoId=photo['Plant No'].tolist()
photoId2021=photo2021['Plant No'].tolist()

justVeg=list((set(veg['ID'].tolist()).difference(growingData['ID'].tolist()))) #for never flowered

photoId=[x for x in photoId if not(pd.isna(x))==True] #remove without name
photoPC=[]
photoPB=[] #last year and this year photos with pb
for i in range(len(photoId)):
    photoId[i] = photoId[i].lower()
    if photoId[i][1]=='c':
        photoPC.append(photoId[i])
    if photoId[i][1]=='b':
        photoPB.append(photoId[i])
photoId2021=[x for x in photoId2021 if not(pd.isna(x))==True]
for i in range(len(photoId2021)):
    photoId2021[i] = photoId2021[i].lower()
    if photoId2021[i][1]=='b':
        photoPB.append(photoId2021[i]) #add last year to pbs photos

photos=photoPC+photoPB #photos of both pbs and pcs
"""
In veg and photos (just this year) but not in growing_data
"""
vegAndPhoto=list(set(justVeg).intersection(set(photoId)))

"""
All plants never flowered comparing with growing data and photos both years
"""
photosIds=photoId+photoId2021
justVeg=list((set(justVeg).difference(photosIds)))

"""
In photoID2022 not in growing or veg, possible voluntiers
"""
justPhoto=list((set(photoId).difference(growingData['ID'].tolist()))) #in photoID2022 not in growingData
justPhoto=list((set(justPhoto).difference(veg['ID'].tolist())))  

"""
In growing and with photo this year but not in veg
"""
missingVeg=list(set(growingData['ID'].tolist()).intersection(set(photoId)))
missingVeg=list((set(missingVeg).difference(veg['ID'].tolist()))) 


#Remove non flowered plants
ids=list(dict.fromkeys(growingData['ID'].tolist())) #uniques
flowered=[]
notFlowered=[]
for i in ids:
    flor=growingData.loc[lambda growingData: (growingData['ID']==i),'TotFl'].tolist()
    flor=np.sum(flor)
    if flor>0: 
        flowered.append(i)
    else:
        notFlowered.append(i)

"""
In growing data while flowering not anywhere else (all veg, photos both years)
"""
just_Fl_Data=list((set(flowered).difference(veg['ID'].tolist())))
just_Fl_Data=list((set(just_Fl_Data).difference(photosIds)))

comprobation=list(set(notFlowered).intersection(set(justVeg))) #not flowered in growing data are not in Veg and Veg without flowering are not in growing data
vegFlowered=list(set(veg['ID'].tolist()).intersection(set(flowered))) #appears in veg and has flowered in growing

#Getting just pcs and pbs
PCBs=[]
for i in flowered: #get rid of not PCs
    if i[1]=='c' or i[1]=='b':
        PCBs.append(i)
        
PCBsVeg=[]
for i in veg['ID']: #get rid of not PCs
    if i[1]=='c' or i[1]=='b':
        PCBsVeg.append(i)

"""
Pcs and Pbs in growing data, veg and photos 
"""
floweredAndVeg=list(set(PCBs).intersection(set(PCBsVeg))) #both pcbs in growing data and Veg
completePCBs=list(set(floweredAndVeg).intersection(set(photos))) #complete in growing data, flowered in veg and with photo PCs

"""
Flowered in growing data and named in veg, not photo available
"""
noPhotos=list((set(floweredAndVeg).difference(photos))) #in veg and growing not in photos

x=[]
y=[]
h=[]
for i in noPhotos:
    x.append(float(veg_original.loc[lambda veg_original: (veg_original['ID']==i),'x']))
    y.append(float(veg_original.loc[lambda veg_original: (veg_original['ID']==i),'y']))
    h.append(float(veg_original.loc[lambda veg_original: (veg_original['ID']==i),'h']))


################################################################################
#Writting csv files

dictionary={'ID':completePCBs}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('CompletedPCBs.csv')

dictionary={'ID':noPhotos,'X':x,'Y':y,'H':h}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('MissingPhoto.csv')

dictionary={'ID':just_Fl_Data}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('JustFL_Data.csv')

dictionary={'ID':justVeg}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('NeverFloweredVeg.csv')

dictionary={'ID':justPhoto}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('VoluntiersPhotos.csv')

dictionary={'ID':vegAndPhoto}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('Missing_Fl_Data.csv')

dictionary={'ID':missingVeg}
dataframe=pd.DataFrame(dictionary)
dataframe.to_csv('Missing_Veg.csv')

###############################################################################

record=growingData['ID'].value_counts() 

print('All the files should be in the same directory as this python code')

print('CompletedPCs.csv: contains the plants tagged with c and b recorded in growing data, veg and photos')
print('Number of IDs: '+ str(len(completePCBs)))
print('MissingPhoto.csv: Flowered in growing data and named in veg, not photo available')
print('Number of IDs: '+ str(len(noPhotos[0])))
print('JustFL_Data.csv: In growing data while flowering not anywhere else (all veg, photos both years), possible mistyped')
print('Number of IDs: '+ str(len(just_Fl_Data)))
print('NeverFloweredVeg.csv: All plants that never flowered, present just in veg comparing with growing data and photos of both years' )
print('Number of IDs: '+ str(len(justVeg)))
print('VoluntiersPhotos.csv: Just in photos from 2022 not in growing or veg, possible from voluntiers')
print('Number of IDs: '+ str(len(justPhoto)))
print('Missing_Fl_Data.csv: In veg and photos (just this year) but not in growing_data')
print('Number of IDs: '+ str(len(vegAndPhoto)))
print('Missing_Veg.csv: In growing data and with photo this year but not in veg')
print('Number of IDs: '+ str(len(missingVeg)))