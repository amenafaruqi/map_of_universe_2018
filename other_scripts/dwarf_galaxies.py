# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:02:41 2018

@author: amena
"""
import pandas as pd
from astropy.coordinates import Angle
from astropy import units as u

data = pd.read_csv('dwarf_galaxies.csv')

ra_list = []
dec_list = []

for item in data['RA']:
    ra = Angle(item, unit = u.hourangle).degree
    ra_list.append(ra)

for item in data['DEC']:
    dec = Angle(item, unit = u.degree).degree
    dec_list.append(dec)

new_data = pd.DataFrame({
            'objid': data['Name'],
            'name': data['SimbadName'],
            'ra': ra_list,
            'dec': dec_list,
            'dist': [(x*1000*u.pc).to(u.au)/(u.au) for x in data['D']],
            'date': data['date'],
            'mapp': data['Vmag'],
            'mabs': data['VMag'],
            'type':['galaxy' for number in range(len(data))],
            'subtype': ['dwarf galaxy' for number in range(len(data))],
            'importance': [0 for x in range(len(data))],
                   
            })

new_data.to_csv('MoU_dwarfgalaxies.csv')