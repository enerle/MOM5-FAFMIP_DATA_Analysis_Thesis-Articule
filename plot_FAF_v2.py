#
import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc
#import tol_colors 
#from mpl_toolkits.basemap import Basemap

#----------plot_FAF.py------------ LOAD ALL DATA
datadir  = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/ART/DATA_SFC-fluxes'
filename  = ["tau_x_correction_v2.nc","tau_y_correction_v2.nc","salt_sfc_correction_v2.nc","temp_sfc_correction_v2.nc"]

fn = os.path.join(datadir,filename[0])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['XT_OCEAN30_390'][:]
Y1   = file.variables['YT_OCEAN'][:]
tau_x = file.variables['TAU_X_V2'][:,:]
tau_x_zonal = np.mean(tau_x,axis=1)
file.close()

fn = os.path.join(datadir,filename[1])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['XT_OCEAN30_390'][:]
Y1   = file.variables['YT_OCEAN'][:]
tau_y = file.variables['TAU_Y_V2'][:,:]
tau_y_zonal = np.mean(tau_y,axis=1)
file.close()

fn = os.path.join(datadir,filename[2])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X2   = file.variables['XT_OCEAN31_390'][:]
Y2   = file.variables['YT_OCEAN'][:]
PME = file.variables['PME_V2'][:,:]
PME_zonal = np.mean(PME,axis=1)
file.close()

fn = os.path.join(datadir,filename[3])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X3   = file.variables['XT_OCEAN31_390'][:]
Y3   = file.variables['YT_OCEAN'][:]
SFC_HFLUX = file.variables['SFC_HFLUX_V2'][:,:]
SFC_HFLUX_zonal = np.mean(SFC_HFLUX,axis=1)
file.close()

#------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(8.27,11.69))

cmap1=plt.get_cmap('Reds')
#cmap2=plt.get_cmap('RdBu'); cmap2r=cmap2.reversed()
cmap2r=plt.get_cmap('RdBu')#; cmap2r=cmap2.reversed()
cmap3=plt.get_cmap('bwr') 

cmap1.set_bad(color='0.7',alpha=1.)
cmap2r.set_bad(color='0.7',alpha=1.)
cmap3.set_bad(color='0.7',alpha=1.)

fontaxis = 14
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.2)

####
##---momentum Flux
kmin = 0; kmax = 31
clevs = np.arange(kmin,kmax,5)
#cc = np.arange(kmin,kmax,10)

[LON,LAT] = np.meshgrid(X1,Y1)

ax1 = plt.subplot2grid((3,5),(0,0),colspan=4) 

cs = plt.pcolormesh(LON,LAT,tau_x*1e3,shading='flat',cmap=cmap1)
cs1 = plt.contourf(LON,LAT,tau_x*1e3,levels=clevs,cmap=cmap1,extend='max')

plt.clim(kmin,kmax)

Ntau_x = tau_x/np.sqrt(tau_x**2 + tau_y**2); Ntau_y = tau_y/np.sqrt(tau_x**2 + tau_y**2)
css = plt.quiver(LON[::10,::10],LAT[::10,::10],Ntau_x[::10,::10],Ntau_y[::10,::10],color='.2')#,norm='True')

plt.axhline(y=-32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)
plt.axhline(y= 32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)

plt.title('(a) Stress',fontsize=16)
plt.yticks([])#-80,-60,-40,-20,0,20,40,60,80],['80S','60S','40S','20S','0','20N','40N','60N','80N'],fontsize=11)
plt.xticks([])#,[],fontsize=12)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

cbar = plt.colorbar(cs1,ticks=clevs,extend='max',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(clevs)
cbar.ax.set_title('[$10^{-3}$ Pa]',fontsize=12,color='k')

##---Water Flux
kmin = -0.6; kmax = 0.62
clevs = np.arange(kmin,kmax,0.1)

[LON,LAT] = np.meshgrid(X2,Y2)

ax3 = plt.subplot2grid((3, 5),(1,0),colspan=4)
cs = plt.pcolormesh(LON,LAT,((PME/1025)*(86400*1000))*(365/1000),shading='flat',cmap=cmap2r)
cs1 = plt.contourf(LON,LAT,((PME/1025)*(86400*1000))*(365/1000),levels=clevs,cmap=cmap2r,extend='both')

plt.clim(kmin,kmax)

plt.axhline(y=-32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)
plt.axhline(y= 32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)

plt.title('Water',fontsize=16)
plt.yticks([])#-80,-60,-40,-20,0,20,40,60,80],['80S','60S','40S','20S','0','20N','40N','60N','80N'],fontsize=11)
plt.xticks([])#,[],fontsize=12)

ax3.spines['top'].set_linewidth(2);  ax3.spines['bottom'].set_linewidth(2)
ax3.spines['left'].set_linewidth(2); ax3.spines['right'].set_linewidth(2)
ax3.xaxis.set_tick_params(width=2);  ax3.yaxis.set_tick_params(width=2)
#
cbar = plt.colorbar(cs1,ticks=clevs,extend='both',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(['-0.6','','-0.4','','-0.2','','0','','0.2','','0.4','','0.6'])
##cbar.ax.set_yticklabels(clevs)
cbar.ax.set_title('[m yr$^{-1}$]',fontsize=12,color='k')


##---heat Flux
kmin = -30; kmax = 31
clevs = np.arange(kmin,kmax,5)
#cc = np.arange(kmin,kmax,10)

[LON,LAT] = np.meshgrid(X3,Y3)

ax5 = plt.subplot2grid((3,5),(2,0),colspan=4)
cs = plt.pcolormesh(LON,LAT,SFC_HFLUX,shading='flat',cmap=cmap3)
cs1 = plt.contourf(LON,LAT,SFC_HFLUX,levels=clevs,cmap=cmap3,extend='both')
#ax5.axis([0,600,-90,90])

plt.clim(kmin,kmax)

plt.axhline(y=-32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)
plt.axhline(y= 32.0,color=[.4,.4,.4],linestyle=':',linewidth=1)

plt.title('(c) Heat',fontsize=16)
plt.yticks([])#-80,-60,-40,-20,0,20,40,60,80],['80S','60S','40S','20S','0','20N','40N','60N','80N'],fontsize=11)
plt.xticks([])#,[],fontsize=12)

ax5.spines['top'].set_linewidth(2);  ax5.spines['bottom'].set_linewidth(2)
ax5.spines['left'].set_linewidth(2); ax5.spines['right'].set_linewidth(2)
ax5.xaxis.set_tick_params(width=2);  ax5.yaxis.set_tick_params(width=2)

cbar = plt.colorbar(cs1,ticks=clevs,extend='both',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=10)
#cbar.ax.set_yticklabels(clevs)
cbar.ax.set_yticklabels(['30','','20','','10','','0','','10','','20','','30'])
cbar.ax.set_title('[Wm$^{-2}$]',fontsize=12,color='k')

plt.show()
#plt.savefig('FAF_anomalies.png',transparent = True, bbox_inches='tight',dpi=600)
