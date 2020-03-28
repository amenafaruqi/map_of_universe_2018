# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:00:16 2018

@author: amena
"""

import pandas as pd 
from astropy.coordinates import Angle
from astropy import units as u
import numpy as np
from scipy.integrate import quad

data = pd.read_csv(r'blackholes.csv')

ra_list = []
dec_list = []
dists = []


for item in data['Right Ascension']:
    item = str(item).split(",")[0]
    if len(str(item).split(":")) == 3:
        ra = Angle(item, unit = u.hourangle).degree
        ra_list.append(ra)
    elif len(str(item).split(":")[0]) == 2:
        item = "00:" + item
        ra = Angle(item, unit = u.hourangle).degree
        ra_list.append(ra)

for item in data['Declination']:
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

def integrand(x):
    md=0.3
    cc=0
    l=0.7
    E=np.sqrt(md*(1+x)**3+cc*(1+x)**2+l)
    return 1/E

for z in data['Redshift']:
    dist, err = quad(integrand, 0, z)
    dists.append(4550*dist*1000000*206264.80624548031)
     

new_data = pd.DataFrame({
            'name': data['Object'],
            'ra': ra_list,
            'dec': dec_list,
            'date': data['date'],
            'dist': dists,
            'mabs': [0 for num in range(len(data))],
            'mapp': [0 for num in range(len(data))],
            'type':['blackhole' for number in range(len(data))],
            'z': data['Redshift'],
                   
            })

new_data.to_csv('MoU_blackholes(July_2018).csv')