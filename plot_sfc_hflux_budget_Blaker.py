#
import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_SFC-fluxes/'

##---Control fields from the flux-only output
fn = os.path.join(datadir,'Blaker_flux-only_ocean_fluxes_timmean.nc')
print("Working on %s" % fn)
file = nc.Dataset(fn)
Xt = file.variables['xt_ocean'][:]
Yt = file.variables['yt_ocean'][:]
swflx              = np.mean(np.squeeze(file.variables['swflx'][:,:,:]),axis=1)
lw_heat            = np.mean(np.squeeze(file.variables['lw_heat'][:,:,:]),axis=1)
sens_heat          = np.mean(np.squeeze(file.variables['sens_heat'][:,:,:]),axis=1)
##calving_melt_heat = np.mean(np.squeeze(file.variables['calving_melt_heat'][:,:,:]),axis=1)
##evap_heat         = np.mean(np.squeeze(file.variables['evap_heat'][:,:,:]),axis=1)
##fprec_melt_heat   = np.mean(np.squeeze(file.variables['fprec_melt_heat'][:,:,:]),axis=1)
#sfc_hflux_total    = np.mean(np.squeeze(file.variables['sfc_hflux_total'][:,:,:]),axis=1)
sfc_hflux_coupler  = np.mean(np.squeeze(file.variables['sfc_hflux_coupler'][:,:,:]),axis=1)
##sfc_hflux_from_calving = np.mean(np.squeeze(file.variables['sfc_hflux_from_calving'][:,:,:]),axis=1)
sfc_hflux_from_runoff  = np.mean(np.squeeze(file.variables['sfc_hflux_from_runoff'][:,:,:]),axis=1)
sfc_hflux_pme          = np.mean(np.squeeze(file.variables['sfc_hflux_pme'][:,:,:]),axis=1)
file.close()
##----

mass_heat      = sfc_hflux_from_runoff + sfc_hflux_pme
net_sfc_hflux  = sfc_hflux_coupler + mass_heat
evap_heat      = sfc_hflux_coupler - (swflx + lw_heat + sens_heat)

##------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(11.69,8.27))
fluxname = ["$Q_{net}$","$Q_{SW}$","$Q_{LW}$","$Q_{sens}$","$Q_{lat}$","$Q_{mass}$"]


###----
###Surface heat flux budget
###----

fig = plt.figure(1)
#fig.subplots_adjust(hspace=0.25,wspace=0.2)
ax = fig.add_subplot(1,1,1)

ax.plot(Yt,net_sfc_hflux,'-',color='k',linewidth=3.5,label=fluxname[0])
ax.plot(Yt,swflx,'-',color='red',linewidth=3,label=fluxname[1])
ax.plot(Yt,lw_heat,'-',color='blue',linewidth=3,label=fluxname[2])
ax.plot(Yt,sens_heat,'-',color='green',linewidth=3,label=fluxname[3])
ax.plot(Yt,evap_heat,'-',color=[0,.5,1],linewidth=3,label=fluxname[4])
ax.plot(Yt,mass_heat,'-',color='gray',linewidth=3,label=fluxname[5])
#ax.plot(Yt,swflx+lw_heat+sens_heat+evap_heat+mass_heat,'-',color='yellow',linewidth=2,label='Qnet 2')

ax.axis([-90,90,-150,250])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
plt.yticks(fontsize=16);

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)  
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[$Wm^{-2}$]',fontsize=16)
ax.legend(loc=1,fontsize=16)

#plt.show()
plt.savefig('sfc_hflux_budget_Blaker.png',transparent = True, bbox_inches='tight',dpi=600)

###----
###Second part of the heat budget: Heat content and meridional heat transport
###---

filename2 = "/home/clima-archive2/rfarneti/RENE/DATA/OHT_flux-only.nc"
fn = os.path.join(datadir,filename2)
print("Working on ", fn)
file = nc.Dataset(fn)
YY = file.variables['YU_OCEAN'][:]
GLHT = file.variables['GLOHT'][:]*1e-15 #PW
file.close()

filename3 = "/home/clima-archive2/rfarneti/RENE/DATA/heat_content_flux-only.nc"
fn = os.path.join(datadir,filename3)
print("Working on %s" % fn)
file = nc.Dataset(fn)
LAT   = file.variables['YT_OCEAN'][:]
OHC   = np.squeeze(file.variables['HEAT_CONTENT'][:])*1e-21 #ZJ
file.close()

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)

ax.plot(YY,GLHT,'-',color='k',linewidth=2.5,label="OHT $[PW]$")
ax.plot(LAT,OHC*1e-2,'-',color='gray',linewidth=3,label="OHC $[ZJ]$")

ax.axis([-90,90,-1,3])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
plt.yticks(fontsize=16);

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel(' ',fontsize=16)
ax.legend(loc=1,fontsize=16)

#plt.show()
plt.savefig('sfc_hflux_budget_Blaker_p2.png',transparent = True, bbox_inches='tight',dpi=600)

