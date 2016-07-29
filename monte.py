### This defines a function that fits portions before and after flux peak in K band.
### Put in a source id and a spectral id (and spectral type if you want) from bdnyc database or the path to a textfile.
### The function will output a list with the source id, spectral type, first slope, its unc, second slope, and its unc.

import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import *

## Test for code!
## np.random.seed(30)
## print np.random.randn(10)

from astrodbkit import astrodb
db = astrodb.Database('/Users/teacher/Desktop/Research/model_atmospheres.db')
import glob

# Defines the list that will later be populated
fitsdata = []
n = 1000
slopesvals = []


def linear_fit(logg):
    list = glob.glob("/Users/teacher/Desktop/Research/Models/Errors/g{}_*".format(logg))
    x=0
    for txt in list:
        list[x] = txt.rsplit("_")[1]
        list[x] = list[x].rsplit("t")[1]
        list[x] = int(list[x])
        x = x+1
    g = 0
    for teff in list:
        fitsdata = []
        textfile = "/Users/teacher/Desktop/Research/Models/Errors/g{}_t{}_n300.txt".format(logg,teff)
        shortfilename = textfile.rsplit("/",1)[-1]
        shortfilename = shortfilename.rsplit(".",1)[0]
        shortfilename = shortfilename.rsplit("_",1)[0]
        file = np.loadtxt(textfile, delimiter=',')
        xdata = [i[0] for i in file]
        ydata = [i[1] for i in file]
        yunc = [i[2] for i in file]
        spec = [xdata,ydata,yunc]
        '''if source_id != None and spectral_id != None:
            if SNR == 0:
                spec = db.query("SELECT spectrum FROM spectra WHERE id={}".format(spectral_id), fetch='one')[0]
                spec = spec.data
            else:
                wave_flux = db.query("SELECT spectrum FROM spectra WHERE id={}".format(spectral_id), fetch='one')[0]
                wave_flux = wave_flux.data
                err = []
                for i in wave_flux[1]:
                    err.append(1.0/SNR*i)
                spec = [wave_flux[0],wave_flux[1],err]

        elif textfile != None:					###### This allows you to run code from a txt file
            shortfilename = textfile.rsplit("/",1)[-1]
            shortfilename = shortfilename.rsplit(".",1)[0]
            file = np.loadtxt(textfile, delimiter=',')
            xdata = [i[0] for i in file]
            ydata = [i[1] for i in file]
            yunc = []
            if SNR == 0:
                for i in file:
                    try:
                        yunc.append(i[2])
                    except IndexError:
                        yunc.append(0)
            else:
                for j in ydata:
                    yunc.append(1.0/SNR*j)
            spec = [xdata,ydata,yunc]


        ## if the spectral type isn't given (in number form), it will look up the optical spec type in the database. If neither of these exist, defaults to
        ## 2.01 - 2.1.. Need to figure out what to do for models
        if not spectral_type:
            try:
                spectral_type = db.list("SELECT spectral_type FROM spectral_types WHERE regime='OPT' AND source_id={}".format(source_id)).fetchone()[0]
            except:
                None'''

        ## Picks just the K band of the spectrum (from 1.97 to 2.40 microns)
        df_toplot = pd.DataFrame(spec[0])					## wavelength
        df_toplot[1] = spec[1]								## flux
        df_toplot[2] = spec[2]								## uncertainty
        
        df_toplot = df_toplot[df_toplot[0] < 2.40]
        df_toplot = df_toplot[df_toplot[0] > 1.97]
        
        ### Normalizing the flux and unc
        df_toplot[2] = df_toplot[2] / np.nanmean(df_toplot[1])
        df_toplot[1] = df_toplot[1] / np.nanmean(df_toplot[1])
        
        
        
        
        #### Monte carlo iterations
        flux0 = np.array(df_toplot[1]).copy()
        for w in range(n):
            flux2 = flux0 + np.random.randn(len(np.array(df_toplot[1])))*np.array(df_toplot[2])
            #pl.plot(df_toplot[0],flux2)
            #pl.fill_between(df_toplot[0],df_toplot[1]-df_toplot[2],df_toplot[1]+df_toplot[2])
            
            
            """ Slope 1 """
            ### All sources use the same range from 2.03 to 2.1

            xmin = 2.03
            xmax = 2.1
            
            ## gets x values of just region being fit
            df_blue_1 = df_toplot.copy()
            df_blue_1[1] = flux2						#### shifted y values
            
            
            df_blue_1 = df_blue_1[df_blue_1[0] < xmax]
            df_blue_1 = df_blue_1[df_blue_1[0] > xmin]
            
            
            ## Fits the selected region to a line and gives a covariance matrix.
            fit_1 = np.polyfit(df_blue_1[0],df_blue_1[1],1,cov=True,full=False)
            
            ## Variance of slope in 1st entry in covariance matrix.. unc is it's sqrt
            ## variance = np.diagonal(fit_1[1])
            ## abs_unc_slope_fit_1 = variance[0]**(0.5)
            
            ## Plots the line fit on the spectrum.
            #x = np.linspace(xmin,xmax,10000)
            #y = fit_1[0][0]*x + fit_1[0][1]
            #pl.plot(x,y,'b',linewidth=2)
            
                
            """ slope 2 """
            ## Slope 2 is fit from 2.214-2.29 (avoids Na line at ~2.2 and goes right up to CO absorption)
            ## Everything is same as above.
            xmin = 2.215
            xmax = 2.29

            df_red = df_toplot.copy()
            df_red[1] = flux2
                
            df_red = df_red[df_red[0] < xmax]
            df_red = df_red[df_red[0] > xmin]
                
            #### Linear fit
            fit_2 = np.polyfit(df_red[0],df_red[1],1,cov=True,full=False)				## fits 2 order poly. to (a,b2)
            ## variance = np.diagonal(fit_2[1])
            ## abs_unc_slope_fit_2 = variance[0]**(0.5)
            
                    
            #x = np.linspace(xmin,xmax,10000)	## creates lots of x points
            #y = fit_2[0][0]*x + fit_2[0][1]		## y as fnc given by polyfit
            #pl.plot(x,y,'r',linewidth=2,)#label=('slope =', fit_2[0][0], 'unc =', abs_unc_slope_fit_2))		#r'Slope = #-0.75 $\pm$ 0.10 $\mu m^{-1}$'))
            
  
            ### VERY IMPORTANT
            ### This appends to the list 'fitsdata' the source id, spectral type, lower micron fit, its unc, higher micron fit,
            ### and its unc.
            fitsdata.append([logg,teff,fit_1[0][0],fit_2[0][0],shortfilename,fit_1[0][1],fit_2[0][1]])
            ## Uncomment pl.show() to plot spectrum with fits on it.
            #pl.show()

            

        with PdfPages('/Users/teacher/Desktop/Research/Plots/Histo/{}_blue.pdf'.format(shortfilename)) as pdf:
            blue = []
            for i in range(0,n):
                if fitsdata[i][4] == shortfilename:
                    blue.append(fitsdata[i][2])						
            pl.hist(blue,15)
            pl.axvline(np.nanmean(blue),0,350,linewidth = 2, color = 'black', ls='-')
            pl.axvline(np.nanmean(blue)+np.std(blue),0,350,linewidth = 2, color = 'black', ls='--')
            pl.axvline(np.nanmean(blue)-np.std(blue),0,350,linewidth = 2, color = 'black', ls='--')
            pl.ylabel('Counts')
            pl.xlabel('Blue K Band Slope')
            pl.title('{}'.format(shortfilename))
            pdf.savefig()
            pl.close()

        with PdfPages('/Users/teacher/Desktop/Research/Plots/Histo/{}_red.pdf'.format(shortfilename)) as pdf:
            red = []
            for i in range(0,n):
                if fitsdata[i][4] == shortfilename:
                    red.append(fitsdata[i][3])
            pl.hist(red,15,facecolor='red')
            pl.axvline(np.nanmean(red),0,350,linewidth = 2, color = 'black', ls='-')
            pl.axvline(np.nanmean(red)+np.std(red),0,350,linewidth = 2, color = 'black', ls='--')
            pl.axvline(np.nanmean(red)-np.std(red),0,350,linewidth = 2, color = 'black', ls='--')
            pl.ylabel('Counts')
            pl.xlabel('Red K Band Slope')
            pl.title('{}'.format(shortfilename))
            pdf.savefig()
            pl.close()


        #### PLOT INFORMATION #####
        title('{}'.format(shortfilename))
        legend(loc=8)
        xscale('linear')
        yscale('linear')
        xlim(1.97,2.4)
        #xlim(2,2.2)
        ylim(0.0,2.5)
        #pl.tick_params(axis='both',labelsize=20)
        xlabel(r'Wavelength ($\mu m$)',fontsize=30)
        ylabel(r'Normalized Flux ($F_{\lambda}$)',fontsize=30)
        tick_params(axis='both',labelsize=20)
        
        ## Plots the normalized K band in blue.
        #pl.figure()
        pl.plot(df_toplot[0],df_toplot[1],'blue')
        pl.fill_between(df_toplot[0],df_toplot[1]-df_toplot[2],df_toplot[1]+df_toplot[2],alpha = .1)

        ## Plots the average of the blue fits on top
        xb = np.linspace(2.03,2.1,10000)
        xr = np.linspace(2.215,2.29,10000)
        ## Plots the average of the red fits on top
        bluestart=[]
        redstart=[]
        for i in range(0,n):
            if fitsdata[i][4] == shortfilename:
                bluestart.append(fitsdata[i][5])
                redstart.append(fitsdata[i][6])
        y = np.nanmean(blue)*xb + np.nanmean(bluestart)
        pl.plot(xb,y,'b',linewidth=2)
        y = np.nanmean(red)*xr + np.nanmean(redstart)
        pl.plot(xr,y,'r',linewidth=2)

        #Saves the Plot
        with PdfPages('/Users/teacher/Desktop/Research/Plots/Fits/{}_fit.pdf'.format(shortfilename)) as pdf:
            pdf.savefig()
            pl.close()

        #name = db.list("SELECT names FROM sources WHERE id={}".format(source_id)).fetchone()[0]
        slopesvals.append([logg,teff,np.nanmean(blue),np.std(blue),np.nanmean(red),np.std(red),shortfilename])
        print(logg,teff)
    out = pd.DataFrame(slopesvals)
    out.to_csv('/Users/teacher/Desktop/Research/Models/Fits/g{}.txt'.format(logg))


