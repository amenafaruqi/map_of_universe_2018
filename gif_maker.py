# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:36:24 2018

@author: amena
"""

import imageio
import os

directory = os.path.dirname(os.path.realpath(__file__)) 
images = []
years = list(range(1800,2019))
for year in years:
    image_file = directory + '\image%s.png' %year
    images.append(imageio.imread(image_file))
    os.remove(image_file)


imageio.mimwrite(directory + '\MoU_years(deltat=1).gif', images, duration = 0.15)
