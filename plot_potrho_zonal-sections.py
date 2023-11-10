import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'

#exp      = ["Stress","Water","Heat","All","flux-only"]
#filename = ["zonalsection_rholevels_STC_FAFSTRESS.nc","zonalsection_rholevels_STC_FAFWATER.nc","zonalsection_rholevels_STC_FAFHEAT.nc","zonalsection_rholevels_STC_FAFALL.nc","zonalsection_rholevels_STC_flux-only.nc"]

exp      = ["Stress","Water","Heat","Control"]
filename = ["zonalsection_rholevels_STC_FAFSTRESS.nc","zonalsection_rholevels_STC_FAFWATER.nc","zonalsection_rholevels_STC_FAFHEAT.nc","zonalsection_rholevels_STC_flux-only.nc"]

LON    = [None]*len(exp)
DEPTH  = [None]*len(exp)
RHO_NH = [None]*len(exp)
RHO_SH = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON[i]    = file.variables['GRIDLON_T'][:]
    DEPTH[i]  = file.variables['ST_OCEAN'][:]
    RHO_NH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24N'][:,:,:])-1000. 
    RHO_SH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24S'][:,:,:])-1000.
    file.close()

#------------------------PLOTTING
#rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(11,8.27))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.1,.1)

clevs_rho1 = [31.8668,32.7973,33.8931,34.6656,35.0366,35.3538,36.20,36.80,36.90]
clevs_rho2 = [0,31.8668,35.3538] #ekman, upper and bso


v = [-238,-112,0,750]

fig = plt.figure(1)

for i in range(len(exp)): 
    fig.subplots_adjust(hspace=0.25,wspace=0.12)
    fig.tight_layout()
    subplots_adjust(wspace=None, hspace=.15)

    ax = fig.add_subplot(2,2,i+1)
     
    cc1 = plt.contour(LON[i],DEPTH[i],RHO_NH[i],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=1)
    plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    cc2 = plt.contour(LON[i],DEPTH[i],RHO_NH[i],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)

    cc3 = plt.contour(LON[i][0:66],DEPTH[i][:],RHO_NH[i][:,0:66],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

    #plt.plot(np.ones(10)*-215.,linspace(75,680,10),color='k',linestyle='--',linewidth=2.)

    plt.title(exp[i],fontsize=14)
    plt.xticks([]); plt.yticks([])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#plt.show()
plt.savefig('stc_section_rholevels_north.png',transparent = False, bbox_inches='tight',dpi=300)

###

clevs_rho1 = [32.1096,32.7334,33.9313,34.6682,36.2835,36.5690,36.7336,36.85,36.90]
#clevs_rho2 = [33.9313]
clevs_rho2 = [0,32.1096,36.2835]

v = [-208,-71,0,1100]

fig = plt.figure(2)

for i in range(len(exp)):
    fig.subplots_adjust(hspace=0.25,wspace=0.12)
    fig.tight_layout()
    subplots_adjust(wspace=None, hspace=.15)

    ax = fig.add_subplot(2,2,i+1)

    cc1 = plt.contour(LON[i],DEPTH[i],RHO_SH[i],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=1)
    plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    cc2 = plt.contour(LON[i],DEPTH[i],RHO_SH[i],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)

    cc3 = plt.contour(LON[i][0:86],DEPTH[i][:],RHO_SH[i][:,0:86],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

    plt.title(exp[i],fontsize=14)
    plt.xticks([]); plt.yticks([])

    #plt.plot(np.ones(10)*-195.,linspace(75,1000,10),color='k',linestyle='--',linewidth=2.)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#plt.show()
plt.savefig('stc_section_rholevels_south.png',transparent = False, bbox_inches='tight',dpi=300)


