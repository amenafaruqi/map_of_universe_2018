# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 16:31:30 2018

@author: amena
"""

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
import matplotlib.patches as mpatches
from astropy import units as u
from astropy.coordinates import Angle,Distance
import pandas as pd
import os
import glob
import time

st = time.clock()
directory = os.path.dirname(os.path.realpath(__file__)) 

datasets = []
def find_csv(dir):
    """
    input: the directory you want to explore
    return: The names of all csv files in the directory in terms a list of strings 
    """
    filenames= []
    os.chdir(dir)
    for file in glob.glob("*.csv"):
        filenames.append(file)
    return filenames

for file in find_csv(directory):
    print(file)
    datasets.append(pd.read_csv(file, low_memory=False, encoding='latin-1'))
print('Datasets read')
    

"""Create function that will plot a given dataset on a 3D plot.
   Distances are plotted in units of AU, RA and DEC are plotted in hours."""
def plot_data(dataset):   
#Set colours and sizes for all objects according to their 'type'
    if dataset.type.tolist()[0].lower() == 'galaxy':
        colour = 'lawngreen'
        size = 10
    elif dataset.type.tolist()[0].lower() == 'star':
        colour = 'yellow'
        size = 10
    elif dataset.type.tolist()[0].lower() == 'blackhole':
        colour = 'orange'
        size = 50
    elif dataset.type.tolist()[0].lower() == 'satellite':
        colour = 'pink'
        size = 20
    elif dataset.type.tolist()[0].lower() == 'mainbody':
        colour = 'red'
        size = 170
    elif dataset.type.tolist()[0].lower() == 'moon':
        colour = 'blue'
        size = 60
    elif dataset.type.tolist()[0].lower() == 'asteroid':
        colour = 'lightgray'
        size = 10 
    elif dataset.type.tolist()[0].lower() == 'exoplanet':
        colour = 'darkviolet'
        size = 30
    elif dataset.type.tolist()[0].lower() == 'spacecraft':
        colour = 'pink'
        size = 30
    elif dataset.type.tolist()[0].lower() == 'quasar':
        colour = 'aqua'
        size = 20
    elif dataset.type.tolist()[0].lower() == 'supernova':
        colour = 'white'
        size = 30
    else:
        colour = 'grey'
        size = 40

    DIST = dataset.dist.tolist()
    RA = dataset.ra.tolist() 
    DEC = dataset.dec.tolist()
    Z = [(Distance(abs(d), u.au)/u.au) for d in DIST]
    X = RA
    Y = DEC
    
    ax.scatter3D(X,Y,np.log10(Z), marker='.',s=size,color=colour, depthshade=False)
    
    #ax.grid(False)
    #ax.set_xlim3d(-1,25)
    ax.set_ylim3d(-4,4)
    #ax.set_zlim3d(-5,16)
    ax.set_zlabel('Log[Distance from Earth center (AU)]',fontsize=12)
    ax.set_xlabel('Right Ascension (h)',fontsize=12)
    ax.set_ylabel('Declination (h)', fontsize=12)


"""Create a plot of all bodies that had been discovered by a given year"""
def make_year_plot(year):
    for dataset in datasets:
        date_filter = []
        for date in dataset['date']:
            if str(date)[0:4].isdigit() == True:
                if int(date[0:4]) <= int(year):
                    date_filter.append(1)
                else:
                    date_filter.append(0)
                    
            elif str(date)[len(str(date))-4:len(str(date))].isdigit() == True:
                if int(date.split('/')[2]) <= int(year):
                    date_filter.append(1)
                else:
                    date_filter.append(0)
            else:
                date_filter.append(0)
        
        dataset['date_filter'] = date_filter
        dataset = dataset[dataset.date_filter == 1]
        if len(dataset)>0:
            plot_data(dataset)
   

fig = plt.figure()
ax = plt.axes(projection='3d')
fig.set_size_inches(10,20,10)
plt.gca().patch.set_facecolor('white')
ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
#zticks = [1e0,1e3,1e6,1e9,1e12,1e15]
#ax.set_zticks(np.log10(zticks))
#ax.set_zticklabels(np.log10(zticks))


"""Function to update the plot each time the date slider is moved to a 
different year (called whenever the slider is moved)"""
def update(year):
    ax.clear()
    make_year_plot(year)
    plt.show()

    
"""Make slider to view plot at different years"""
year_min = 1700
year_max = 2018
year_init = 2018
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
year_slider = Slider(slider_ax, 'Year', year_min, year_max, valinit=year_init, valfmt='%0.0f')
slider_ax.xaxis.set_visible(True)
slider_ax.set_xticks([1700, 1750, 1800, 1850, 1900, 1950, 2000, 2018]) 
year_slider.on_changed(update)

"""Create plot legend"""
mb_patch = mpatches.Patch(color='red', label='Mainbody')
gal_patch = mpatches.Patch(color='lawngreen', label='Galaxy')
st_patch = mpatches.Patch(color='yellow', label='Star')
bh_patch = mpatches.Patch(color='orange', label='Blackhole')
as_patch = mpatches.Patch(color='lightgray', label='Asteroid')
ex_patch = mpatches.Patch(color='darkviolet', label='Exoplanet')
s_patch = mpatches.Patch(color='pink', label='Satellite/Spacecraft')
m_patch = mpatches.Patch(color='blue', label='Moon')
q_patch = mpatches.Patch(color='aqua', label='Quasar')
su_patch = mpatches.Patch(color='white', label='Supernova')
o_patch = mpatches.Patch(color='grey', label='Other')
plt.legend(handles=[mb_patch, gal_patch, st_patch, bh_patch, as_patch, ex_patch, s_patch,m_patch,q_patch,su_patch,o_patch], loc='upper left', ncol=3, bbox_to_anchor=(0.0, 30.6))

for dataset in datasets:
    plot_data(dataset)


plt.show()
print(time.clock()-st)
