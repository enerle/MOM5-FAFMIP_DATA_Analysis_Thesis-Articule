#
import sys
import os
import numpy as np
import numpy.ma as ma
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["faf-stress","faf-water","faf-heat","faf-all","Control"]
filename = ["OHU_FAFSTRESS.nc","OHU_FAFWATER.nc","OHU_FAFHEAT.nc","OHU_FAFALL.nc","OHU_flux-only.nc"]

OHU     = [None]*len(exp)
OHUmean = [None]*len(exp)
OHU2    = [None]*len(exp)
LON     = [None]*len(exp)
LON2    = [None]*len(exp)
LAT     = [None]*len(exp)
LAT2    = [None]*len(exp)

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON[i]   = file.variables['XT_OCEAN'][:]
    LAT[i]   = file.variables['YT_OCEAN'][:]
    OHU[i]   = file.variables['OHU'][:,:]*1e-9 # GJ/m^2 
    OHUmean[i] = np.ma.average(OHU[i],axis=(0,1))
    file.close()

for i in range(len(filename)):
    OHU2[i]  = OHU[i] - OHUmean[i]

#---> Get OH content for the control
fn   = os.path.join(datadir,"heat_content_flux-only.nc")
file = nc.Dataset(fn)
OHC  = np.squeeze(file.variables['HEAT_CONTENT'][:]*1e-21)
file.close()

#------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27)) #rc('figure', figsize=(8.27,11.69))

#cmap2 = cmocean.cm.balance
#cmap2 = plt.get_cmap('bwr_r') 
#cmap2 = plt.get_cmap('RdBu_r')
#cmap2 = plt.get_cmap('coolwarm')
cmap2 = plt.get_cmap('bwr')
cmap2.set_bad(color = '0.5', alpha = None)

#kmin = -2.2
#kmax = 2.2
#clevs = [-15,-10,-5,-2,-1,-0.5,0.5,1,2,5,10,15]

kmin = -15; kmax = 15
clevs = np.linspace(kmin,kmax,16)

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [LON2[i],LAT2[i]] = np.meshgrid(LON[i],LAT[i])
    ax = fig.add_subplot(3,2,i+1)
    
    OHU_anom = OHU2[i]-OHU2[-1]

    cs  = plt.pcolormesh(LON2[i],LAT2[i],OHU_anom,shading='flat',cmap=cmap2)
    cs1 = plt.contourf(LON2[i],LAT2[i],OHU_anom,levels=clevs,cmap=cmap2,extend='both')

    plt.clim(kmin,kmax)
    plt.title("%s" %exp[i] + " (%.2f $GJm^{-2}$)" %(OHUmean[i]-OHUmean[-1]),fontsize=16)
    plt.xticks([]); plt.yticks([])

    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

cbaxes = fig.add_axes([0.3, 0.32, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs1,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=12)
#cbar.ax.set_yticklabels(['-15','-10','-5','-2','-1','-0.5','0','0.5','1','2','5','10','15'])
cbar.ax.set_title('[$GJm^{-2}$]',fontsize=12,color='k')

plt.show()
#plt.savefig('OHU.png',transparent = True, bbox_inches='tight',dpi=800)

