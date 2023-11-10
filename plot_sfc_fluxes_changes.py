#
import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir = '/home/clima-archive2/rfarneti/RENE/DATA'
datadir   = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_SFC-fluxes'

#exp       = ["Stress","Water","Heat","Heat+","All","flux-only"]
#filename  = ['Blaker_FAFSTRESS_ocean_fluxes_timmean.nc','Blaker_FAFWATER_ocean_fluxes_timmean.nc','Blaker_FAFHEAT_ocean_fluxes_timmean.nc','Blaker_FAFHEAT-plus_ocean_fluxes_timmean.nc','Blaker_FAFALL_ocean_fluxes_timmean.nc','Blaker_flux-only_ocean_fluxes_timmean.nc']

exp       = ["Stress","Heat","flux-only"]
filename  = ['Blaker_FAFSTRESS_ocean_fluxes_timmean.nc','Blaker_FAFHEAT_ocean_fluxes_timmean.nc','Blaker_flux-only_ocean_fluxes_timmean.nc']

x    = [None]*len(exp)
y    = [None]*len(exp)
taux = [None]*len(exp)
tauy = [None]*len(exp)
tau  = [None]*len(exp)
net_sfc_wflux     = [None]*len(exp)
net_sfc_hflux     = [None]*len(exp)
hflux_coupler     = [None]*len(exp)
hflux_from_runoff = [None]*len(exp)
hflux_pme         = [None]*len(exp)
delta_mean_net_sfc_hflux = [None]*len(exp)

##---Control fields from the flux-only output
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    x[i]  = file.variables['xt_ocean'][:]
    y[i]  = file.variables['yt_ocean'][:]
    taux[i] = np.squeeze(file.variables['tau_x'][:,:,:])
    tauy[i] = np.squeeze(file.variables['tau_y'][:,:,:])
    net_sfc_wflux[i] = np.squeeze(file.variables['pme_sbc'][:,:,:])
    #net_sfc_hflux[i] = np.squeeze(file.variables['sfc_hflux_total'][:,:,:])
    hflux_coupler[i] = np.squeeze(file.variables['sfc_hflux_coupler'][:,:,:])
    hflux_from_runoff[i] = np.squeeze(file.variables['sfc_hflux_from_runoff'][:,:,:])
    hflux_pme[i]         = np.squeeze(file.variables['sfc_hflux_pme'][:,:,:])
    file.close()

    net_sfc_hflux[i] = hflux_coupler[i] + hflux_from_runoff[i] + hflux_pme[i]

for i in range(len(exp)-1):
    delta_mean_net_sfc_hflux[i] = np.mean(net_sfc_hflux[i]-net_sfc_hflux[-1])


##change in heat flux!!
#------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(11.69,8.27))

cmap2 = cmocean.cm.balance
cmap2.set_bad(color = '0.5', alpha = None)

kmin = -50; kmax = 50
clevs = [-50,-40,-30,-20,-10,-5,0,5,10,20,30,40,50]

## Stress
fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [lon,lat] = np.meshgrid(x[i],y[i])

    ax = fig.add_subplot(3,2,i+1)
    cs  = plt.pcolormesh(lon,lat,taux[i]-taux[-1],shading='flat',cmap=cmap2)

    plt.clim(kmin,kmax)

    plt.xticks([]); plt.yticks([])

    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

cbaxes = fig.add_axes([0.3, 0.62, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)

#plt.show()

## Water
fig = plt.figure(2)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [lon,lat] = np.meshgrid(x[i],y[i])

    ax = fig.add_subplot(3,2,i+1)
    cs  = plt.pcolormesh(lon,lat,net_sfc_wflux[i]-net_sfc_wflux[-1],shading='flat',cmap=cmap2)

    plt.clim(kmin,kmax)

    plt.xticks([]); plt.yticks([])

    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

cbaxes = fig.add_axes([0.3, 0.62, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)

#plt.show()

## Heat
fig = plt.figure(3)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [lon,lat] = np.meshgrid(x[i],y[i])

    ax = fig.add_subplot(3,2,i+1)
    cs  = plt.pcolormesh(lon,lat,net_sfc_hflux[i]-net_sfc_hflux[-1],shading='flat',cmap=cmap2)

    plt.clim(kmin,kmax)
    plt.title("%s" %exp[i] + " ($\delta Q=$ %.2f $Wm^{-2}$)" %delta_mean_net_sfc_hflux[i],fontsize=16)
    plt.xticks([]); plt.yticks([])

    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

cbaxes = fig.add_axes([0.3, 0.62, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)

#plt.show()
plt.savefig('sfc_hflux_changes_BLAKER.png',transparent = True, bbox_inches='tight',dpi=600)


