from astrodbkit import astrodb

ma_db = astrodb.Database('/Users/teacher/Desktop/Research/model_atmospheres.db')


from matplotlib import pyplot as plt
import numpy as np
#from BDNYCdb import utilities as u
from pylab import rcParams
import pandas as pd
rcParams['figure.figsize'] = 6, 5
import glob

def slope(plot,path=None):
    plt.close()
    if path != None:
        input = pd.read_csv(path,index_col=0)
    else:
        input = pd.read_csv('/Users/teacher/Desktop/Research/Models/Combo/Fits.txt',index_col=0)
        list = glob.glob("/Users/teacher/Desktop/Research/Models/Fits/*")
    sub = len(list)
    plt.xlabel(r'Temperature (K)',fontsize=30)
    plt.tick_params(axis='both',labelsize=20)
    plt.xlim(700,3050)
    plt.gca().invert_xaxis()
    fits = []
    coefs = []
    y = .14
    n = 1
    y2 = .86
    if plot == 'Red':
        '''temps = sorted(set(input['1']), key=int)
        rslopes = []
        rslopemax = []
        rslopemin = []
        for t in temps:
            bytemp = np.where(input['1']==t)
            for value in bytemp:
                points = len(value)
                if points ==5:
                    print(t)
                for p in range(points):
                    rslopes.append(input['4'][value[p]])
            rslopemax.append(np.amax(rslopes))
            rslopemin.append(np.amin(rslopes))
            rslopes = []
        coefrmax = np.polyfit(temps,rslopemax,9)
        coefrmin = np.polyfit(temps,rslopemin,9)
        fitrmax = np.poly1d(coefrmax)
        fitrmin = np.poly1d(coefrmin)
        plt.fill_between(temps,rslopemax,rslopemin,alpha=0.1)'''
        for logg in list:
            inputg = pd.read_csv('{}'.format(logg),index_col=0)
            name = logg.rsplit("/")[-1]
            name = name.rsplit(".",1)[0]
            name = name.rsplit("g")[1]
            print(name)
            if name == '3.5':
                deg = 5
                shade = '#a1d99b'
            elif name == '4.0':
                deg = 4
                shade = '#74c476'
            elif name == '4.5':
                deg = 7
                shade = '#41ab5d'
            elif name == '5.0':
                deg = 6
                shade = '#238b45'
            else:
                deg = 6
                shade = '#005a32'
            coef = np.polyfit(inputg['1'],inputg['4'],deg,full=True)
            fit = np.poly1d(coef[0])
            print(coef[0])
            x = np.linspace(900,3000,1000)
            fits.append(fit(x))
            coefs.append([name,deg,coef[0],coef[1],coef[2]])
            #list[x] = list[x].rsplit("t")[1]
            #list[x] = int(list[x])
            #plt.subplot(sub,1,n)
            plt.plot(x, fit(x),color = shade,linewidth = 2)
            plt.errorbar(inputg['1'],inputg['4'],yerr = inputg['5'],marker='o',mfc='{}'.format(y2),mec='.1',ecolor = '{}'.format(y2),label = 'log(g) = {}'.format(name),linestyle='None')
            y2=y2-.14
            y = y+.14
            n = n+1
            plt.gca().invert_yaxis()
            plt.ylabel(r'Red K Band Slope ($\mu m^{-1}$)',fontsize=30)
            plt.ylim(1,-6)
        plt.legend(loc=2)
        plt.gca().invert_xaxis
        #for i in range(0,(sub-1)):
#plt.fill_between(x,fits[i],fits[i+1],alpha = 0.1)
    if plot == 'Blue':
        '''temps = sorted(set(input['1']), key=int)
        bslopes = []
        bslopemax = []
        bslopemin = []
        for t in temps:
            bytemp = np.where(input['1']==t)
            for value in bytemp:
                points = len(value)
                for p in range(points):
                    bslopes.append(input['2'][value[p]])
            bslopemax.append(np.amax(bslopes))
            bslopemin.append(np.amin(bslopes))
            bslopes = []
        coefbmax = np.polyfit(temps,bslopemax,9)
        coefbmin = np.polyfit(temps,bslopemin,9)
        fitbmax = np.poly1d(coefbmax)
        fitbmin = np.poly1d(coefbmin)
        plt.fill_between(temps,bslopemax,bslopemin,alpha=0.1)'''
        for logg in list:
            inputg = pd.read_csv('{}'.format(logg),index_col=0)
            name = logg.rsplit("/")[-1]
            name = name.rsplit(".",1)[0]
            name = name.rsplit("g")[1]
            print(name)
            if name == '3.5':
                deg = 7
                shade = '#a1d99b'
            elif name == '4.0':
                deg = 6
                shade = '#74c476'
            elif name == '4.5':
                deg = 6
                shade = '#41ab5d'
            elif name == '5.0':
                deg = 7
                shade = '#238b45'
            else:
                deg = 7
                shade = '#005a32'
            coef = np.polyfit(inputg['1'],inputg['2'],deg,full=True)
            fit = np.poly1d(coef[0])
            x = np.linspace(900,3000,1000)
            fits.append(fit(x))
            coefs.append([name,deg,coef[0],coef[1],coef[2]])
            plt.plot(x, fit(x),color = shade, linewidth=2)
            plt.errorbar(inputg['1'],inputg['2'],yerr = inputg['3'],marker='o',mfc='{}'.format(y2),mec='.1',ecolor = '{}'.format(y2),label = 'log(g) = {}'.format(name),linestyle='None')
            plt.ylim(-2,10)
            plt.ylabel(r'Blue K Band Slope ($\mu m^{-1}$)',fontsize=30)
            plt.legend(loc=2)
            y2=y2-.14
            y = y+.14
            n = n+1
    #for i in range(0,(sub-1)):
            #plt.fill_between(x,fits[i],fits[i+1],alpha = 0.1)
    out =pd.DataFrame(coefs)
    out.columns = ['logg','degree','coefficients','RMS','rank']
    out.to_csv('/Users/teacher/Desktop/Research/{}_polys.txt'.format(plot))

    plt.show()


#fnew = sum(f[np.where(np.logical_and(w>start,w<end))])
