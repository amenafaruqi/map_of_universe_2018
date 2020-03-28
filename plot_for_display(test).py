# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:37:32 2017

@author: gwyli_000
"""
import pandas as pd
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import Angle,Distance
import numpy as np
import os

directory = os.path.dirname(os.path.realpath(__file__)) + '\data'

def plot_data_large(dataset,groupname):
    """
    Plots datapoints for non solar system objects from the called dataset on a graph of right ascension (hours) vs. logarithmic distance (Earth radii).
    It calls the columns of the .csv file and obtains the relevant columns.
    Any column of the database can be called by using data.column.tolist() where column refers to the name within the .csv file.
    Units can easily be changed by changing the suffix of u.
    
    Key Arguments:
        - dataset: Pandas dataframe of the dataset from .csv file. Can be obtained from download_database.py
        - colour: Colour of the data points on the graph (string).
        - groupname: Name of the data collection that will appear in annotations (string).
    """
    X = []
    Y = []
    colours = []
    DIST = dataset.dist.tolist()
    RA = dataset.ra.tolist()  
    TEMPS = dataset.teff_val.tolist()
    for d in DIST:
        dist = Distance(d, u.pc)
        Y.append(dist.R_earth)
    for ra in RA:
        ra = Angle(ra, u.degree)
        X.append(-ra.hour)
    for temp in TEMPS:
        if temp < 3500:
            colours.append('red')
        elif temp < 5000:
            colours.append('orange')
        elif temp < 6000:
            colours.append('yellow')
        elif temp < 7500:
            colours.append('white')
        elif temp < 10000:
            colours.append('blue')
        else:
            colours.append('yellow')
        
    plt.scatter(X,Y,marker='.',s=0.7, edgecolor='none',color=colours,label=groupname)


plt.rcParams['axes.facecolor']='black'

for num in range(0,2000):
    plot_data_large(pd.read_csv(directory + '\gaia_%s.csv' %num, delimiter = ','), 'stars')


plt.yscale('log')
plt.xticks([-24,-18,-12,-6,0],[24,18,12,6,0],fontsize = 10)
plt.yticks([1,10**3,10**6,10**9,10**12,10**15,10**18,10**21, 10**24],fontsize=10)
plt.gca().set_xlim([-24,0])
plt.gca().set_ylim([1,10.**24.])
plt.ylabel('Distance from Earth center (R-earth)',fontsize = 8)
plt.xlabel('Right ascension (h)',fontsize=10)
plt.axhline(10**8,linestyle='--',color='k',linewidth=0.4)
plt.axhline(2*10**9,linestyle='--',color='k',linewidth=0.4)
plt.annotate('The Oort Cloud',xy=(-14.3,3.3*10**8),color='k',fontsize=4)
plt.axhline(3*10**6,linestyle='-',linewidth=0.2,color='k')
plt.annotate('Heliopause',xy=(-13.1,3.5*10**6),color='k',fontsize=3)
def milky_way_disk(ra):
    RA = Angle(ra + 17.76, u.hour)
    r = (2.6 * np.cos(RA.radian) + np.sqrt(6.76 * np.cos(RA.radian)**2. + 18.24)) * 10**4
    dist = Distance(r, u.lightyear)
    return dist.R_earth
def milky_way_halo(ra):
    RA = Angle(ra + 17.76, u.hour)
    r = (2.6 * np.cos(RA.radian) + np.sqrt(6.76 * np.cos(RA.radian)**2. + 1593.24)) * 10**4
    dist = Distance(r, u.lightyear)
    return dist.R_earth
ras = np.arange(-24.0,0.0,0.01)
plt.plot(ras, milky_way_disk(ras),linestyle='-',color='w',linewidth=0.3)
plt.plot(ras, milky_way_halo(ras),linestyle='--',color='w',linewidth=0.3)
plt.annotate('Extent of the Milky Way disk',xy=(-15,10**14),color='w',fontsize=5)
plt.annotate('Estimated extent of the Milky Way dark matter halo',xy=(-17,10**15),color='w',fontsize=5)
ber_sig = Distance(1.3485*10.**17.,u.m)
plt.axhline(ber_sig.R_earth,linestyle='--',color='w',linewidth=0.1)
plt.annotate('Farthest radio signal from Earth',xy=(-14,2.2*10**10),color='w',fontsize=5) #1936 Berlin Olympics broadcast as used by Gott et al
fig = plt.gcf()
#fig.set_size_inches(2,8)
plt.savefig('universe_map_test3.png',bbox_inches='tight', dpi=3000) 
plt.show()