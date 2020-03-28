# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:59:43 2018

@author: amena
"""

import numpy as np
import pandas as pd 
from astropy import units as u
from astropy import constants as const
from scipy.integrate import quad

data = pd.read_csv('2M++.csv')

dist = []
dates = []

"""Pulls dates from reference numbers in the 2M++ catalogue (when 
given, first 4 digits are the year of the survey)"""

for i in data['Ref']:
    year = str(i)[0:4]
    if year.isdigit() == True:
        dates.append('01/01/' + year)
    else:
        dates.append('')

"""Calculates distances in pc based on redshift(velocity/speed of light)"""
def integrand(x):
    md=0.3
    cc=0
    l=0.7
    E=np.sqrt(md*(1+x)**3+cc*(1+x)**2+l)
    return 1/E

for i in data['Vcmb']:
    z = (i*1000)/(const.c*(u.s/u.m))
    ans, err = quad(integrand, 0, z)
    dist.append(ans*1000000)     

new_data = pd.DataFrame({
        
        'name': data['Name'],
        'ra': data['RA'],
        'dec': data['DE'],
        'mapp': data['Ksmag'],
        'mabs': data['Ksmag'] + 5 -5*np.log10(dist),
        'HV': data['HV'],
        'e_HV': data['e_HV'],
        'Vcmb': data['Vcmb'],
        'z': (data['Vcmb']*1000)/(const.c*(u.s/u.m)),
        'dist': [4550*i*206264.80624548031 for i in dist],
        'type': ['galaxy' for x in range(len(data))],
        'date': dates,
               
        })
    
new_data.to_csv('2M++_dist.csv')
