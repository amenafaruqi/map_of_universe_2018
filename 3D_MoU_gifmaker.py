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
import imageio
import os
import glob
import time


def find_csv(dir):
    '''
    input: the directory you want to explore
    return: The names of all csv files in the directory in terms a list of strings 
    '''
    filenames= []
    os.chdir(dir)
    for file in glob.glob("*.csv"):
        filenames.append(file)
    return filenames

    
"""Create function that will plot a given dataset on a 3D plot.
   Distances are plotted in units of AU, RA and DEC are plotted in hours."""
def plot_data(dataset):   
#Set colours and sizes for all objects according to their 'type'
    if dataset.type.tolist()[0].lower() == 'galaxy':
        colour = 'lawngreen'
        size = 1
    elif dataset.type.tolist()[0].lower() == 'star':
        colour = 'yellow'
        size = 1.5
    elif dataset.type.tolist()[0].lower() == 'blackhole':
        colour = 'orange'
        size = 15
    elif dataset.type.tolist()[0].lower() == 'satellite':
        colour = 'pink'
        size = 2
    elif dataset.type.tolist()[0].lower() == 'mainbody':
        colour = 'red'
        size = 27
    elif dataset.type.tolist()[0].lower() == 'moon':
        colour = 'blue'
        size = 20
    elif dataset.type.tolist()[0].lower() == 'asteroid':
        colour = 'lightgray'
        size = 1
    elif dataset.type.tolist()[0].lower() == 'exoplanet':
        colour = 'darkviolet'
        size = 9
    elif dataset.type.tolist()[0].lower() == 'spacecraft':
        colour = 'pink'
        size = 2
    elif dataset.type.tolist()[0].lower() == 'quasar':
        colour = 'aqua'
        size = 1
    elif dataset.type.tolist()[0].lower() == 'supernova':
        colour = 'white'
        size = 3
    else:
        colour = 'grey'
        size = 3
        print('Unknown object found')

    DIST = dataset.dist.tolist()
    RA = dataset.ra.tolist() 
    DEC = dataset.dec.tolist()
    X = []
    Y = []
    Z = []
    '''
    if len(DIST) <800: 
        Z = [abs(float(d)) for d in DIST]
        X = [(Angle(ra, u.degree).hour) for ra in RA]
        Y = [(Angle(dec,u.degree).hour) for dec in DEC]
    elif dataset.type.tolist()[0] =='Star':
        randints = [np.random.randint(len(DIST)) for x in range(8100)]
        Z = [abs(float(DIST[i])) for i in randints]
        X = [(Angle(RA[i], u.degree).hour) for i in randints]
        Y = [(Angle(DEC[i],u.degree).hour) for i in randints]
    else:
        lim = int(200*np.log(len(DIST)))
        randints = [np.random.randint(len(DIST)) for x in range(0,lim)]
        Z = [abs(float(DIST[i])) for i in randints]
        X = [(Angle(RA[i], u.degree).hour) for i in randints]
        Y = [(Angle(DEC[i],u.degree).hour) for i in randints]        
    
    ax.scatter3D(X,Y,np.log10(Z), marker='.',s=size,color=colour, depthshade=False)'''
    
    if len(DIST) > 800:          # Limit number of datapoints from each CSV file
        randints = [np.random.randint(len(DIST)) for x in range(0,800)]
        for i in randints: 
            dist = Distance(abs(DIST[i]), u.au)
            Z.append(dist/u.au)
            ra = Angle(RA[i], u.degree)
            X.append(ra.hour)
            dec = Angle(DEC[i],u.degree)
            Y.append(dec.hour)
    else:
        for d in DIST:
            dist = Distance(abs(d), u.au)
            Z.append(dist/u.au)
        for ra in RA:
            ra = Angle(ra, u.degree)
            X.append(ra.hour)
        for dec in DEC:
            dec = Angle(dec,u.degree)
            Y.append(dec.hour)  
        
    ax.scatter3D(X,Y,np.log10(Z), marker='.',s=size,color=colour, depthshade=False)

    #ax.grid(False)
    ax.set_xlim3d(-1,25)
    ax.set_ylim3d(-6,11)
    ax.set_zlim3d(-22,1)
    ax.set_zlabel('Log[Distance from Earth center (Gpc)]',fontsize=12)
    ax.set_xlabel('Right Ascension (h)',fontsize=12)
    ax.set_ylabel('Declination (h)', fontsize=12)


"""Create a plot of all bodies that had been discovered by a given year"""
def make_year_plot(year):
    for dataset in datasets:
        date_filter = []
        for date in dataset['date']:
            if str(date)[0:4].isdigit() == True:
                if int(date[0:4]) == int(year):
                    date_filter.append(1)
                else:
                    date_filter.append(0)
                    
            elif str(date)[len(str(date))-4:len(str(date))].isdigit() == True:
                if int(date.split('/')[2]) == int(year):
                    date_filter.append(1)
                else:
                    date_filter.append(0)
            else:
                date_filter.append(0)
        
        dataset['date_filter'] = date_filter
        dataset = dataset[dataset.date_filter == 1]
        if len(dataset)>0:
            plot_data(dataset)
   
if __name__ == "__main__":

    st = time.clock()
    directory = os.path.dirname(os.path.realpath(__file__)) + '\data_gpc'
    datasets = []

    for file in find_csv(directory):
        print(file)
        datasets.append(pd.read_csv(file, low_memory=False, encoding='latin-1'))
    print('Datasets read')
        
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_size_inches(10,20,10)
    plt.gca().patch.set_facecolor('white')
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    plt.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
    zticks = [1e-20,1e-15,1e-10,1e-5,1e0]
    ax.set_zticks(np.log10(zticks))
    ax.set_zticklabels(np.log10(zticks), fontsize = 9)
    
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
    leg = plt.legend(handles=[mb_patch, gal_patch, st_patch, bh_patch, as_patch, ex_patch, s_patch,m_patch,q_patch,su_patch,o_patch], ncol=4, loc = 'upper center',  prop={'size': 11}, bbox_to_anchor=(0.55,-0.035))
    
    images = []
    years = list(range(2009,2019)) #timesteps for gif
    make_year_plot(0000)
    for year in years:
        make_year_plot(year)  
        plt.suptitle('Year : ' + str(year), y=0.89, fontsize = 18)
        fig = plt.gcf()
        fig.set_size_inches(9,12,9)
        #plt.show()
        fig.savefig('image%s.png' %year, bbox_inches='tight')
        images.append(imageio.imread(directory + '\image%s.png' %year))
    
    imageio.mimwrite(directory + '\MoU_years.gif', images, duration = 0.15)
    
    plt.show()
    print(time.clock()-st)
