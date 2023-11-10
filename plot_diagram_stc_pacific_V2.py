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
datadir2 = '/home/clima-archive2/rfarneti/RENE/DATA'

fn = os.path.join(datadir,"temp_sfc_correction_v2.nc")
print("Working on %s" % fn)
file = nc.Dataset(fn)
X3   = file.variables['XT_OCEAN31_390'][:]
Y3   = file.variables['YT_OCEAN'][:]
SFC_HFLUX = file.variables['SFC_HFLUX_V2'][:,:]
SFC_HFLUX_zonal = np.mean(SFC_HFLUX,axis=1)
file.close()

##---Control fields from the flux-only output
fn = os.path.join(datadir,'Blaker_flux-only_ocean_fluxes_timmean.nc')
print("Working on %s" % fn)
file = nc.Dataset(fn)
Xt = file.variables['xt_ocean'][:]
Yt = file.variables['yt_ocean'][:]
tau_x   = np.squeeze(file.variables['tau_x'][:,:,:])
tau_y   = np.squeeze(file.variables['tau_y'][:,:,:])
hflux_coupler     = np.squeeze(file.variables['sfc_hflux_coupler'][:,:,:])
hflux_from_runoff = np.squeeze(file.variables['sfc_hflux_from_runoff'][:,:,:])
hflux_pme         = np.squeeze(file.variables['sfc_hflux_pme'][:,:,:])
evap    = np.squeeze(file.variables['evap'][:,:,:])
lprec   = np.squeeze(file.variables['lprec'][:,:,:])
runoff  = np.squeeze(file.variables['runoff'][:,:,:])
pme_sbc = np.squeeze(file.variables['pme_sbc'][:,:,:])
file.close()

#tau       = np.sqrt(tau_x**2 + tau_y**2)
SFC_HFLUX = hflux_coupler + hflux_from_runoff + hflux_pme
PME       = pme_sbc

#MLD
fn = os.path.join(datadir2,"MLD_BSO_flux-only.nc")
file = nc.Dataset(fn)
PMLD   = file.variables['PMLD'][:]
file.close()

#rho
fn = os.path.join(datadir2,"PAC_potrho_zonalmean_and_levels_STC_flux-only.nc")
file = nc.Dataset(fn)
LAT   = file.variables['GRIDLAT_T'][:]
DEPTH = file.variables['ST_OCEAN'][:]
POTRHO  = file.variables['PPOTRHO2'][:]-1000.
file.close()


##------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(8.27,11.69))

cmap1=plt.get_cmap('seismic')
#cmap1=plt.get_cmap('Reds')
cmap2=plt.get_cmap('RdBu')
cmap3=plt.get_cmap('bwr')

cmap1.set_bad(color='0.7',alpha=1.)
cmap2.set_bad(color='0.7',alpha=1.)
cmap3.set_bad(color='0.7',alpha=1.)

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.2)

[LON,LAT] = np.meshgrid(X3,Y3)

#wind stress
kmin= -.2; kmax =.2
clevs1 = np.arange(kmin,kmax,.02)

ax = fig.add_subplot(3,1,1)
cs = plt.pcolormesh(LON,LAT,tau_x,shading='flat',cmap=cmap3)
cs1 = plt.contour(LON,LAT,tau_x,levels=clevs1,colors='k')
ax.axis([-250,-69,-55,55])
#plt.clim(kmin,kmax)

plt.axhline(y=0.0,color='k',linestyle='solid',linewidth=1.)

plt.yticks([-60,-45,-30,-15,0,15,30,45,60],['60S','45S','30S','15S','0','15N','30N','45N','60N'],fontsize=11)
plt.xticks([-250,-225,-200,-175,-150,-125,-100,-75],['110E','135E','160E','175W','150W','125W','100W','75W'],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#plt.show()
plt.savefig('pacific_diagram_vsept.png',transparent = True, bbox_inches='tight',dpi=600)

