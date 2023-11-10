import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = ' /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'
exp      = ["faf-stress","faf-water","faf-heat","faf-all","Control"]

filename = ["MOC_FAFSTRESS.nc","MOC_FAFWATER.nc","MOC_FAFHEAT.nc","MOC_FAFALL.nc","MOC_flux-only.nc"]

AMOC     = [None]*len(exp)
MOC      = [None]*len(exp)
MOC_GM   = [None]*len(exp)
AMOC_GM  = [None]*len(exp)

DEPTH  = [None]*len(exp)
LAT    = [None]*len(exp)
DEPTH2 = [None]*len(exp)
LAT2   = [None]*len(exp)

#---> Get the AMOC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    LAT[i]     = file.variables['YU_OCEAN'][:]
    DEPTH[i]   = file.variables['ST_OCEAN'][:]
    AMOC[i]    = file.variables['AMOC'][:,:]
    AMOC_GM[i] = file.variables['AMOC_GM'][:,:]
    MOC[i]     = file.variables['MOC'][:,:]
    MOC_GM[i]  = file.variables['MOC_GM'][:,:]
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

#-----------------------------------------------------------------------
##-----Zonal sections AMOC MOC
#-----------------------------------------------------------------------

#cmap = plt.cm.RdBu_r
cmap = plt.get_cmap('bwr')
kmin = -6; kmax = 6
clevs   = np.arange(kmin,kmax+.5,.5)
clevs2  = [-20,-15,-10,-5,0,5,10,15,20]
v= [-90,90,0,5000]

##------AMOC
fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(3,2,i+1)

    cs = plt.contourf(LAT2[i],DEPTH2[i],AMOC[i]-AMOC[-1],levels=clevs,cmap=cmap,extend='both')
    cc = plt.contour (LAT2[i],DEPTH2[i],AMOC[-1],levels=clevs2,colors='k',linewidths=0.25)
    plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    plt.clim(kmin,kmax)
    plt.axis(v)
    plt.title('%s' % (exp[i]), fontsize=16, color='k')

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-30,0,30,60,90],['30S','0','30N','60N','90N'],fontsize=12)
    else:
        plt.xticks([-30,0,30,60,90],[])
    if (i==0 or i==2 or i==4):
       plt.yticks([0,1000,2000,3000,4000,5000],[0,1000,2000,3000,4000,5000],fontsize=12)
       ax.set_ylabel('Depth [m]',fontsize=16) 
    else:
       plt.yticks([0,1000,2000,3000,4000,5000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
    
##changes in colorbar
cbaxes = fig.add_axes([0.1, 0.3, 0.8, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_title('Sv',fontsize=14,color='k')

#plt.show()
plt.savefig('AMOC_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

##------MOC
cmap = plt.get_cmap('bwr')
kmin = -6; kmax = 6
clevs   = np.arange(kmin,kmax+.5,.5)
clevs2  = [-20,-15,-10,-5,0,5,10,15,20]

v= [-90,90,0,5000]

fig = plt.figure(2)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(3,2,i+1)

    cs = plt.contourf(LAT2[i],DEPTH2[i],MOC[i]-MOC[-1],levels=clevs,cmap=cmap,extend='both')
    cc = plt.contour (LAT2[i],DEPTH2[i],MOC[-1],levels=clevs2,colors='k',linewidths=0.25)
    plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    plt.clim(kmin,kmax)
    plt.axis(v)
    plt.title('%s' % (exp[i]), fontsize=16, color='k')

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=12)
    else:
        plt.xticks([-90,-60,-30,0,30,60,90],[])
    if (i==0 or i==2 or i==4):
       plt.yticks([0,1000,2000,3000,4000,5000],[0,1000,2000,3000,4000,5000],fontsize=12)
       ax.set_ylabel('Depth [m]',fontsize=16)
    else:
       plt.yticks([0,1000,2000,3000,4000,5000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis


cbaxes = fig.add_axes([0.1, 0.3, 0.8, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=10)

cbar.ax.set_title('[Sv]',fontsize=16,color='k')

#plt.show()
plt.savefig('MOC_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

