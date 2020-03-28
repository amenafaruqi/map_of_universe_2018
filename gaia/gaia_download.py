# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:57:57 2018

@author: amena
"""
import urllib
import gzip
from bs4 import BeautifulSoup
import os
import pandas as pd


"""Loops through all download links on a given webpage and downloads all files
(compressed), decompresses them and deletes the compressed file"""

def obtainfunc(http,savefile):
    urllib.request.urlretrieve(http,savefile)
    return savefile

def decompress(data, name):
    with gzip.open(data, 'rb') as f:
        file_content = str(f.read())
        file_content = file_content.replace(str("\\") + "n", '\n')
        file = open(name + '.csv','w') 
        file.write(file_content)
        file.close

def download(): 
    resp = urllib.request.urlopen("http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/")
    soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().get_param('charset'))
    hrefs = []
    for link in soup.find_all('a', href=True):
        if str(link['href'])[:4] == 'Gaia':
            hrefs.append(link['href'])
    
    for num in range(0,61234):  
            file_name = "gaia%g.csv.gz" %num
            file = obtainfunc("http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/" + hrefs[num],file_name)
            decompress(file_name, 'gaia_%s' %num)
            os.remove(file)
            filename = r'gaia_%s.csv' %num
            data = pd.read_csv(filename)
            data.rename(columns={"b'solution_id" : 'solution_id'}, inplace=True)
            new_data = data.filter(['solution_id', 'source_id', 'ref_epoch', 'ra', 'dec','parallax', 'parallax_over_error','radius_val', 'lum_val', 'teff_val', 'radial_velocity'], axis=1)
            new_data.to_csv('gaia%s.csv' %num)
            os.remove(filename)
        
download()