# Python3 and pip3
# Reqd packages: numpy, scipy, lightkurve (and others) 
# LightKurve based code to read pixel data of targets and generate light curve 
# using aperture defined in target file.
# Ref:
# Pixel data for C13 targets can be downloaded from 
#    https://archive.stsci.edu/pub/k2/target_pixel_files/c13/ (Or this program 
#    can automatically download based on EPIC ID
# LightKurve SW tutorials: https://docs.lightkurve.org/tutorials/index.html
#    This snippet uses code from the "LightKurve API" tutorial
# However, Light curves can be got for C13 from 
#    https://archive.stsci.edu/pub/k2/lightcurves/c13/

import sys  
import os
import matplotlib.pyplot as plt
import astropy.units as u
from lightkurve import KeplerTargetPixelFile
from lightkurve import search_lightcurvefile
from lightkurve import search_targetpixelfile

#Methods

#print metadata
def print_metadata():
    # print some metadata
    print("Info on pixel data")
    print("Mission: ", tpf.mission)
    print("Quarter: ", tpf.quarter)
    print("Time: ", tpf.astropy_time.utc.iso)
    return

#print normalized LC w/o outliers
def plot_show_normalNoOutliersLC():
    pltTitle = 'Light Curve of ' + sys.argv[1]
    lc.remove_outliers().normalize().plot(title=pltTitle)
    #set title and display plot
    plt.title (pltTitle)
    plt.show()
    return

def plot_show_ampVsFreq():
    pg.plot()
    plt.title ('Amplitude vs Freq: Periodogram of ' + sys.argv[1])
    plt.show()
    return

def plot_show_ampVsPeriodLog():
    pg.plot(view='period', scale='log')
    #set title and display plot
    plt.title ('Amplitude vs Period: Periodogram of ' + sys.argv[1])
    plt.show()
    return

def plot_show_flux():
    #get period of max power
    period = pg.period_at_max_power
    print('Best period: {}'.format(period))
    lc.fold(period.value).scatter();
    #set title and display plot
    plt.title ('Max Power (Flux) of ' + sys.argv[1])
    plt.show()
    return

#Main code
if len(sys.argv) < 2:
    print ("Usage: SAPlightcurve <epicID_of_target>")
    sys.exit()

epicID = int(sys.argv[1])

if epicID is None:
    print ("No epicID give - exiting..")
    sys.exit()
else:
    print ("Going to download pixel data for ", epicID)

tpf = search_targetpixelfile(epicID).download()
if tpf is None:
    print ("Unable to download TPF for ", epicID)
    print ("Exiting..")
else:
    # save pixel data in FITS file
    cwd = os.getcwd()
    fits_fname = str(epicID)+(".fits")
    output_fn=cwd+"/"+fits_fname
    tpf.to_fits(output_fn, overwrite=True)
    print ('Saved FITS file at: ', output_fn)

    print_metadata()

    #generate the LC 
    lc = tpf.to_lightcurve(aperture_mask=tpf.pipeline_mask)

    #plot and show LC
    plot_show_normalNoOutliersLC()

    #plot and show someperiodograms
    pg = lc.to_periodogram(oversample_factor=1)
    plot_show_ampVsFreq()
    plot_show_ampVsPeriodLog()
    plot_show_flux()
