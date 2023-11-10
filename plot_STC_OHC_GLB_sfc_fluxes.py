#
import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_SFC-fluxes/'
filename = ["tau_x_correction_timmean.nc","tau_y_correction_timmean.nc","tau_correction_timmean.nc","salt_sfc_correction_timmean.nc","temp_sfc_correction_timmean.nc"] 

##FAFMIP fluxes
fn = os.path.join(datadir,filename[0])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
faftaux = np.mean(np.squeeze(file.variables['tau_x'][:,:,:]),axis=1)
file.close()

fn = os.path.join(datadir,filename[1])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
faftauy = np.mean(np.squeeze(file.variables['tau_y'][:,:,:]),axis=1)
file.close()

fn = os.path.join(datadir,filename[2])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X1   = file.variables['xt_ocean'][:]
Y1   = file.variables['yt_ocean'][:]
faftau = np.mean(np.squeeze(file.variables['tau_xy'][:,:,:]),axis=1)
file.close()

fn = os.path.join(datadir,filename[3])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X2   = file.variables['xt_ocean'][:]
Y2   = file.variables['yt_ocean'][:]
fafpme = np.mean(np.squeeze(file.variables['pme'][:,:,:]),axis=1)
file.close()

fn = os.path.join(datadir,filename[4])
print("Working on %s" % fn)
file = nc.Dataset(fn)
X3   = file.variables['xt_ocean'][:]
Y3   = file.variables['yt_ocean'][:]
fafheat = np.mean(np.squeeze(file.variables['sfc_hflux'][:,:,:]),axis=1)
file.close()

##---Control fields from the flux-only output
fn = os.path.join(datadir,'Blaker_flux-only_ocean_fluxes_timmean.nc')
print("Working on %s" % fn)
file = nc.Dataset(fn)
Xt = file.variables['xt_ocean'][:]
Yt = file.variables['yt_ocean'][:]
taux   = np.mean(np.squeeze(file.variables['tau_x'][:,:,:]),axis=1)
tauy   = np.mean(np.squeeze(file.variables['tau_y'][:,:,:]),axis=1)
hflux_coupler     = np.mean(np.squeeze(file.variables['sfc_hflux_coupler'][:,:,:]),axis=1)
hflux_from_runoff = np.mean(np.squeeze(file.variables['sfc_hflux_from_runoff'][:,:,:]),axis=1)
hflux_pme         = np.mean(np.squeeze(file.variables['sfc_hflux_pme'][:,:,:]),axis=1)
evap    = np.mean(np.squeeze(file.variables['evap'][:,:,:]),axis=1)
lprec   = np.mean(np.squeeze(file.variables['lprec'][:,:,:]),axis=1)
runoff  = np.mean(np.squeeze(file.variables['runoff'][:,:,:]),axis=1)
pme_sbc = np.mean(np.squeeze(file.variables['pme_sbc'][:,:,:]),axis=1)
file.close()

tau = np.sqrt(taux**2 + tauy**2)
net_sfc_hflux = hflux_coupler + hflux_from_runoff + hflux_pme
net_sfc_wflux = pme_sbc

##------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.2)

##---STRESS
ax = fig.add_subplot(3,1,1)

ax.plot(Y1,taux,'-',color='k',linewidth=1.5)
ax.plot(Y1,faftaux,'-',color='k',linewidth=1.5)
ax.plot(Y1,taux+faftaux,'-',color='r',linewidth=1.5)

ax.axis([-45,45,-.10,.10])

plt.title('Stress',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-40,-30,-20,-10,0,10,20,30,40],[],fontsize=16)
plt.yticks(fontsize=16); 

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[$10^{3}Pa$]',fontsize=16)

##---WATER
ax = fig.add_subplot(3,1,2)

ax.plot(Yt,((net_sfc_wflux/1025)*(86400*1000))*(365/1000),'-',color='k',linewidth=1.5)
ax.plot(Yt,((fafpme/1025)*(86400*1000))*(365/1000),'-',color='k',linewidth=1.5)
ax.plot(Yt,(((net_sfc_wflux+fafpme)/1025)*(86400*1000))*(365/1000),'-',color='r',linewidth=1.5)

ax.axis([-45,45,-1,1])

plt.title('Water',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-40,-30,-20,-10,0,10,20,30,40],[],fontsize=16)
plt.yticks(fontsize=16);

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[$m year^{-1}$]',fontsize=16)

##---HEAT
ax = fig.add_subplot(3,1,3)

ax.plot(Yt,net_sfc_hflux,'-',color='k',linewidth=1.5)
ax.plot(Yt,fafheat,'-',color='k',linewidth=1.5)
ax.plot(Yt,net_sfc_hflux+fafheat,'-',color='r',linewidth=1.5)

ax.axis([-45,45,-50,50])

plt.title('Heat',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'],fontsize=16)
plt.yticks(fontsize=16);

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[$Wm^{-2}$]',fontsize=16)

#plt.show()
plt.savefig('STC_OHC_GLB_sfc_fluxes.png',transparent = True, bbox_inches='tight',dpi=600)

