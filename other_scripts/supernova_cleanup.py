# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:10:08 2018

@author: amena
"""
import pandas as pd 
from astropy.coordinates import Angle
from astropy import units as u

data = pd.read_csv(r'SupernovaeWithDistances.csv')
data = data.drop_duplicates(subset = 'dist', keep = False)
data = data[data.ra.notnull()]
#data = data[data.dec.notnull()]


"""ra_list = []
dec_list = []
z_list = []

for item in data['ra']:
    item = str(item).split(",")[0]
    if len(str(item).split(":")) == 3:
        ra = Angle(item, unit = u.hourangle).degree
        ra_list.append(ra)
    elif len(str(item).split(":")[0]) == 2:
        item = "00:" + item
        ra = Angle(item, unit = u.hourangle).degree
        ra_list.append(ra)

for item in data['dec']:
    item0 = str(item).split(",")[0]
    if len(str(item0).split(":")) == 3:
        dec = Angle(item0, unit = u.degree).degree
        dec_list.append(dec)
    elif len(str(item0).split(":")[0]) == 2:
        item = "00:" + item
        dec = Angle(item, unit = u.degree).degree
        dec_list.append(dec)
    elif len(str(item).split(",")) > 1:
        item1 = str(item).split(",")[1]  
        dec = Angle(item1, unit = u.degree).degree
        dec_list.append(dec)
        
for item in data['z']:
        z = item.split(",")[0]
        z_list.append(z)"""
    

new_data = pd.DataFrame({
            'objid': data['Name'],
            'host name': data['Host Name'],
            'ra':data['ra'],
            'dec':data['dec'],
            'date': data['date'],
            'dist': [abs(d) for d in data['dist']],
            'mabs': data['mabs'],
            'mapp': data['mapp'],
            'type':['supernova' for number in range(len(data))],
            'subtype': data['Type'],
            'z': data['z'],
                   
            })

new_data.to_csv('MoU_Supernovae(July_2018).csv')