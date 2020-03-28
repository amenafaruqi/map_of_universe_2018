"""Crossmatches GDR2 entries with those in other catalogues that predate Gaia:
    
    - Tycho-2 (Hog. et al. 2000)
    - 2MASS PSC (Skrutskie et al. 2006)
    - GSC 2.3 (Lasker et al. 2008)
    - Hipparcos-2 (van Leeuwen, 2007)
    - PPMXL (Roeser et al. 2010)
    - SDSS DR9 (Ahn et al. 2012)
    - URAT-1 (Zacharias et al. 2015)
    - AllWISE (Secrest et al. 2015)
    - Gaia DR1 (Prusti et al. 2016)
    - Pan-STARRS1 (Chambers et al. 2016)
    - APASS DR9 (Henden et al. 2016)
    - RAVE DR5 (Kunder et al. 2017)
Cross-match catalogues from: https://gea.esac.esa.int/archive/

If a match is found in any database other than IERS, the date of the survey 
it was found in is applied to the entry.

If a match is found in the IERS database, the IERS designation number is used 
to search the ICRF2 catalogue to obtain the MJD of the first observation of 
the star, which is then converted to a date in the Gregorian calendar

If no match is found, the date is left as the default (GDR2 release date)"""

import time
import pandas as pd
from astropy.time import Time
import os

start_time = time.clock()

tycho = pd.read_csv('tycho2_crossid.csv')
tmass = pd.read_csv('2masspsc_crossid.csv')
gsc = pd.read_csv('gsc23_crossid.csv')
hipparcos = pd.read_csv('hipparcos2_crossid.csv')
ppmxl = pd.read_csv('ppmxl_crossid.csv')
sdss = pd.read_csv('sdssdr9_crossid.csv')
urat = pd.read_csv('urat1_crossid.csv')
dr1 = pd.read_csv('dr1_crossid.csv')
allwise = pd.read_csv('allwise_crossid.csv')
panstarrs = pd.read_csv('panstarrs1_crossid.csv')
apass = pd.read_csv('apassdr9_crossid.csv')
rave = pd.read_csv('ravedr5_crossid.csv')
iers = pd.read_csv('iers_crossid.csv')
icrf = pd.read_csv('iers_dates.csv')

"""Produces lists of the Gaia source IDs stored in each XM catalogue"""

iers_ids = set(iers['source_id'])
iers_names = list(iers['iers_name'])
icrf_ids = list(icrf['IERS_Des.'])
icrf_mjds = list(icrf['First_MJD'])
tycho_ids = set(tycho['gaiaSource_sourceId'])
tmass_ids = set(tmass['gaiaSource_sourceId'])
gsc_ids = set(gsc['gaiaSource_sourceId'])
hipparcos_ids = set(hipparcos['source_id'])
ppmxl_ids = set(ppmxl['gaiaSource_sourceId'])
sdss_ids = set(sdss['gaiaSource_sourceId'])
urat_ids = set(urat['gaiaSource_sourceId'])
dr1_ids = set(dr1['dr2_source_id'])
allwise_ids = set(allwise['source_id'])
panstarrs_ids = set(panstarrs['gaiaSource_sourceId'])
apass_ids = set(apass['gaiaSource_sourceId'])
rave_ids = set(rave['source_id'])

for num in range(52000,61234):
    
    print('Reading: ' + str(num))
    gaia = pd.read_csv('gaia_%g.csv' %num)
    print('Read: ' + str(num))
    gaia_ids = set(gaia['source_id'])
    dates = ['01/04/2018' for x in range(len(gaia))]
    
    """Produces list of all cross-matches for each catalogue"""
    
    iers_XM = list(gaia_ids.intersection(iers_ids))
    tycho_XM = list(gaia_ids.intersection(tycho_ids))
    tmass_XM = list(gaia_ids.intersection(tmass_ids))
    gsc_XM = list(gaia_ids.intersection(gsc_ids))
    hipparcos_XM = list(gaia_ids.intersection(hipparcos_ids))
    ppmxl_XM = list(gaia_ids.intersection(ppmxl_ids))
    sdss_XM = list(gaia_ids.intersection(sdss_ids))
    urat_XM = list(gaia_ids.intersection(urat_ids))
    dr1_XM = list(gaia_ids.intersection(dr1_ids))
    allwise_XM = list(gaia_ids.intersection(allwise_ids))
    panstarrs_XM = list(gaia_ids.intersection(panstarrs_ids))
    apass_XM = list(gaia_ids.intersection(apass_ids))
    rave_XM = list(gaia_ids.intersection(rave_ids))
    
    
    """Converts MJDs to Gregorian dates (needed for ICRF catalogue)"""
    
    def MJD_to_ISO(mjd):
        date = Time(mjd, format = 'mjd', scale = 'utc')
        return Time(date.iso, format = 'iso', scale = 'utc',  out_subfmt = 'date')
    
    for row in gaia.itertuples():
        
        if row.source_id in iers_XM:
            iers_ind = list(iers_ids).index(row.source_id)
            iers_des = iers_names[iers_ind]    
            print('icrf added')
            
            if iers_des in icrf_ids:
                icrf_ind = icrf_ids.index(iers_des)
                MJD = icrf_mjds[icrf_ind]
                dates[row.Index] = MJD_to_ISO(MJD)
        
            else:
                dates[row.Index] = '01/08/2015'
                
        elif row.source_id in tycho_XM:
            dates[row.Index] = '01/01/2000'
            print('tycho added')
            
        elif row.source_id in tmass_XM:
            dates[row.Index] = '01/01/2006'
            print('tmass added')
        
        elif row.source_id in gsc_XM:
            dates[row.Index] = '01/01/2007'
            print('gsc added')
        
        elif row.source_id in hipparcos_XM:
            dates[row.Index] = '01/01/2007'
            print('hipparcos added')
        
        elif row.source_id in ppmxl_XM:
            dates[row.Index] = '01/01/2010'
            print('ppmxl added')
            
        elif row.source_id in sdss_XM:
            dates[row.Index] = '01/01/2012'
            print('sdss added')
        
        elif row.source_id in allwise_XM:
            dates[row.Index] = '01/01/2013'
            print('allwise added')
            
        elif row.source_id in urat_XM:
            dates[row.Index] = '01/01/2015'
            print('urat added')
        
        elif row.source_id in dr1_XM:
            dates[row.Index] = '01/01/2015'
            print('dr1 added')
            
        elif row.source_id in panstarrs_XM:
            dates[row.Index] = '01/01/2016'
            print('panstarrs added')
        
        elif row.source_id in apass_XM:
            dates[row.Index] = '01/01/2016'
            print('apass added')
        
        elif row.source_id in rave_XM:
            dates[row.Index] = '01/01/2017'
            print('rave added')
        
        """
        A possible alternative method for obtaining dates,using apparent 
        magnitudes and historical knowledge of telescope capabilities to 
        estimate when a star could have been first observed. Not used since it 
        assigned an unrealistic number of stars the discovery year '0000'.
        
        elif row.mapp < 6.0:
            dates[row.Index] = '01/01/0000'
        
        elif row.mapp < 10.3:                  #Galileo' Refractor
        
        elif row.mapp < 15.1:
            dates[row.Index] = '01/01/1789'    #Herschel's 40-foot Telescope
        
        elif row.mapp < 17.0:
            dates[row.Index] = '01/01/1895'    #Yerkes' Refractor 
        
            """
            
    new_data = pd.DataFrame({
            
                'solution_id': gaia['solution_id'],
                'source_id': gaia['source_id'],        
                'ra':gaia['ra'],
                'dec':gaia['dec'],
                'date': dates,
                'dist': gaia['dist'],
                'mabs': gaia['mabs'],
                'mapp': gaia['mapp'],
                'type': gaia['type'],
                'subtype': gaia['subtype'],
                'importance': gaia['importance'],
                'commentary': gaia['commentary'],
                'teff_val': gaia['teff_val'],
                'radius_val': gaia['radius_val'],
                'radial_velocity': gaia['radial_velocity']
                       
                })
            
    new_data.to_csv('gaiawithdates%g.csv' %num )
    os.remove('gaia_%g.csv' %num)

print("Runtime: " + str(time.clock()-start_time))