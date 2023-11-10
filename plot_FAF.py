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
datadir  = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_SFC-fluxes'
filename  = ["tau_x_correction_timmean.nc","tau_y_correction_timmean.nc","tau_correction_timmean.nc","salt_sfc_correction_timmean.nc","temp_sfc_correction_timmean.nc"] 

fn = os.path.join(datadir,filename[0])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
tau_x = np.squeeze(file.variables['tau_x'][:,:,:])
tau_x_zonal = np.mean(tau_x,axis=1)
file.close()

fn = os.path.join(datadir,filename[1])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
tau_y = np.squeeze(file.variables['tau_y'][:,:,:])
file.close()

fn = os.path.join(datadir,filename[2])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
TAU  = file.variables['tau_xy'][:,:,:]
TAUt = np.squeeze(TAU) #TAUt = np.mean(TAU,axis=0)
TAUz = np.mean(TAUt,axis=1)
file.close()

fn = os.path.join(datadir,filename[3])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X2   = file.variables['xt_ocean'][:]
Y2   = file.variables['yt_ocean'][:]
PME  = file.variables['pme'][:,:,:]
PMEt = np.squeeze(PME) #PMEt = np.mean(PME,axis=0)
PMEz = np.mean(PMEt,axis=1)
file.close()

fn = os.path.join(datadir,filename[4])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X3   = file.variables['xt_ocean'][:]
Y3   = file.variables['yt_ocean'][:]
SHF  = file.variables['sfc_hflux'][:,:,:]
SHFt = np.squeeze(SHF) #SHFt = np.mean(SHF,axis=0)
SHFz = np.mean(SHFt,axis=1)
file.close()


#------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(8.27,11.69))

cmap1=plt.get_cmap('Reds')
cmap2=plt.get_cmap('RdBu')
cmap2r=cmap2.reversed()
cmap3=plt.get_cmap('bwr') #cmap3=plt.get_cmap('seismic')
cmap1.set_bad(color='0.7',alpha=1.)
cmap2.set_bad(color='0.7',alpha=1.)
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

plt.title('Stress',fontsize=16)
plt.yticks([])#-80,-60,-40,-20,0,20,40,60,80],['80S','60S','40S','20S','0','20N','40N','60N','80N'],fontsize=11)
plt.xticks([])#,[],fontsize=12)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

cbar = plt.colorbar(cs1,ticks=clevs,extend='max',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(clevs)
cbar.ax.set_title('[$10^{-3}$ Pa]',fontsize=12,color='k')

ax2 = plt.subplot2grid((3,5),(0,4),colspan=1) #zonal mean
ax2.plot(tau_x_zonal*1e3,Y1,'-',color='k',linewidth=1.5)
ax2.axis([-25,25,-90,90])

#plt.title('Zonal mean Wind Stress perturbation [$10^3$ Pa]', loc = 'left')
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-30,-20,-10,0,10,20,30],[-30,-20,-10,0,10,20,30])
plt.yticks([-80,-60,-40,-20,0,20,40,60,80],[-80,-60,-40,-20,0,20,40,60,80],fontsize=10)

ax2.spines['top'].set_linewidth(2);  ax2.spines['bottom'].set_linewidth(2)
ax2.spines['left'].set_linewidth(2); ax2.spines['right'].set_linewidth(2)
ax2.xaxis.set_tick_params(width=2);  ax2.yaxis.set_tick_params(width=2)


##---Water Flux
kmin = -0.6; kmax = 0.62
clevs = np.arange(kmin,kmax,0.1)

[LON,LAT] = np.meshgrid(X2,Y2)

ax3 = plt.subplot2grid((3, 5),(1,0),colspan=4)
#cs = plt.pcolormesh(LON,LAT,((PMEt/1025)*(86400*1000))*(365/1000),shading='flat',cmap=cmap2)
#cs1 = plt.contourf(LON,LAT,((PMEt/1025)*(86400*1000))*(365/1000),levels=clevs,cmap=cmap2,extend='both')

cs = plt.pcolormesh(LON,LAT,((PMEt/1025)*(86400*1000))*(365/1000),shading='flat',cmap=cmap2r)
cs1 = plt.contourf(LON,LAT,((PMEt/1025)*(86400*1000))*(365/1000),levels=clevs,cmap=cmap2r,extend='both')

plt.clim(kmin,kmax)

plt.title('Water',fontsize=16)
plt.yticks([])#-80,-60,-40,-20,0,20,40,60,80],['80S','60S','40S','20S','0','20N','40N','60N','80N'],fontsize=11)
plt.xticks([])#,[],fontsize=12)

ax3.spines['top'].set_linewidth(2);  ax3.spines['bottom'].set_linewidth(2)
ax3.spines['left'].set_linewidth(2); ax3.spines['right'].set_linewidth(2)
ax3.xaxis.set_tick_params(width=2);  ax3.yaxis.set_tick_params(width=2)

cbar = plt.colorbar(cs1,ticks=clevs,extend='both',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_yticklabels(['-0.6','','-0.4','','-0.2','','0','','0.2','','0.4','','0.6'])
#cbar.ax.set_yticklabels(clevs)
cbar.ax.set_title('[m yr$^{-1}$]',fontsize=12,color='k')

ax4 = plt.subplot2grid((3, 5), (1, 4), colspan=1) #zonal mean
ax4.plot(((PMEz/1025)*(86400*1000))*(365/1000),Y2,'-',color='k',linewidth=1.5)
ax4.axis([-.4,.4,-90,90])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-.4,-.2,0,.2,.4],[-.4,-.2,0,.2,.4])
plt.yticks([-80,-60,-40,-20,0,20,40,60,80],[-80,-60,-40,-20,0,20,40,60,80],fontsize=11)

ax4.spines['top'].set_linewidth(2);  ax4.spines['bottom'].set_linewidth(2)
ax4.spines['left'].set_linewidth(2); ax4.spines['right'].set_linewidth(2)
ax4.xaxis.set_tick_params(width=2);  ax4.yaxis.set_tick_params(width=2)


##---heat Flux
kmin = -30; kmax = 31
clevs = np.arange(kmin,kmax,5)
#cc = np.arange(kmin,kmax,10)

[LON,LAT] = np.meshgrid(X3,Y3)

ax5 = plt.subplot2grid((3,5),(2,0),colspan=4)
cs = plt.pcolormesh(LON,LAT,SHFt,shading='flat',cmap=cmap3)
cs1 = plt.contourf(LON,LAT,SHFt,levels=clevs,cmap=cmap3,extend='both')
#ax5.axis([0,600,-90,90])

plt.clim(kmin,kmax)

plt.title('Heat',fontsize=16)
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

ax6 = plt.subplot2grid((3,5),(2,4),colspan=1) #zonal mean
ax6.plot(SHFz,Y3,'-',color='k',linewidth=1.5)
ax6.axis([-21,21,-90,90])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
ax6.tick_params(labelbottom='on', labelleft='off')
ax6.tick_params(tickdir='out',labelright='on',direction='out')
plt.xticks([-20,-10,0,10,20],[-20,-10,0,10,20])
plt.yticks([-80,-60,-40,-20,0,20,40,60,80],[-80,-60,-40,-20,0,20,40,60,80],fontsize=11)

ax6.spines['top'].set_linewidth(2);  ax6.spines['bottom'].set_linewidth(2)
ax6.spines['left'].set_linewidth(2); ax6.spines['right'].set_linewidth(2)
ax6.xaxis.set_tick_params(width=2);  ax6.yaxis.set_tick_params(width=2)

#plt.show()
plt.savefig('FAF_anomalies.png',transparent = True, bbox_inches='tight',dpi=600)
