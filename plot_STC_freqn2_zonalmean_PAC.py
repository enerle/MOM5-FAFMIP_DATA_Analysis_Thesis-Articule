import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["(a) faf-stress","(b) faf-water","(c) faf-heat","faf-all","control"]

filename = ["zonalmean_freqn2_FAFSTRESS_PAC.nc","zonalmean_freqn2_FAFWATER_PAC.nc","zonalmean_freqn2_FAFHEAT_PAC.nc","zonalmean_freqn2_FAFALL_PAC.nc","zonalmean_freqn2_flux-only_PAC.nc"]
filename2  = ["BSO_PAC_FAFSTRESS.nc","BSO_PAC_FAFWATER.nc","BSO_PAC_FAFHEAT.nc","BSO_PAC_FAFALL.nc","BSO_PAC_flux-only.nc"]
filename3  = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_FAFALL.nc","pot_rho_0_zonalmean_flux-only.nc"]
filename4  = ["MOC_PAC_FAFSTRESS.nc","MOC_PAC_FAFWATER.nc","MOC_PAC_FAFHEAT.nc","MOC_PAC_FAFALL.nc","MOC_PAC_flux-only.nc"]
filename5   = ["MLD_BSO_FAFSTRESS.nc","MLD_BSO_FAFWATER.nc","MLD_BSO_FAFHEAT.nc","MLD_BSO_FAFALL.nc","MLD_BSO_flux-only.nc"]


lat               = [None]*len(filename)
depth             = [None]*len(filename)
lat2              = [None]*len(filename)
depth2            = [None]*len(filename)

freqn2            = [None]*len(filename)

latrho            = [None]*len(filename)
depthrho          = [None]*len(filename)
latrho2           = [None]*len(filename)
depthrho2         = [None]*len(filename)
bso               = [None]*len(filename)
potrho            = [None]*len(filename)

bso_interp        = [None]*len(exp)
bso_interp_rmean  = [None]*len(exp)
bso_rmean         = [None]*len(exp)

LAT      = [None]*len(exp)
DEPTH    = [None]*len(exp)
LAT2     = [None]*len(exp)
DEPTH2   = [None]*len(exp)
PMOC     = [None]*len(exp)
GMOC     = [None]*len(exp)
PMLD     = [None]*len(exp)

yt = 1e4

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    lat[i]    = file.variables['GRIDLAT_T'][:]
    depth[i]  = file.variables['ST_OCEAN1_49'][:]
    freqn2[i] = file.variables['FREQN2'][:,:]*yt
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    bso[i]       = np.squeeze(file.variables['field'][:])
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    latrho[i]   = file.variables['YT_OCEAN'][:]
    depthrho[i] = file.variables['ST_OCEAN'][:]
    potrho[i]  = file.variables['POT_RHO_0_ZONALMEAN_PAC'][:]-1000.
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename4[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['GRIDLAT_T'][:]
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    PMOC[i]  = file.variables['PMOC'][:]
    #GMOC[i]  = file.variables['MOC'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename5[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    #LAT[i]    = file.variables['YT_OCEAN'][:]
    PMLD[i]   = file.variables['PMLD'][:]
    file.close()

####
N=3  #3
for i in range(len(exp)):
    bso_rmean[i] = np.convolve(bso[i][:],np.ones(N)/N, mode='same') #2,

lat_interp = np.linspace(-90,90,300)
for i in range(len(exp)):
    bso_interp_rmean[i] = np.interp(lat_interp,LAT[i],bso_rmean[i])
####

#------------------------PLOTTING
#rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(11,8.27))

cmap2 = plt.get_cmap('bwr')

v = [-45,45,0,1000]

kmin = -.4; kmax = .4
clevs  = [-.4,-.3,-.2,-.1,-.05,-.01,.01,.05,.1,.2,.3,.4]

clevs_moc = [-30,-20,-18,-16,-14,-12,-10,-5,-2.5,-2,-1,0,1,2,2.5,5,10,15,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5]

fig = plt.figure(100)
fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()

subplots_adjust(wspace=None, hspace=.15)

[lat2[-1],depth2[-1]]       = np.meshgrid(lat[-1],depth[-1])
[latrho2[-1],depthrho2[-1]] = np.meshgrid(latrho[-1],depthrho[-1])
[LAT2[-1],DEPTH2[-1]]       = np.meshgrid(LAT[-1],DEPTH[-1])

ax = fig.add_subplot(2,3,1)###
cs  = plt.contourf(lat2[-1],depth2[-1],freqn2[0][:,:]-freqn2[-1][:,:],levels=clevs,cmap=cmap2,extend='both')
plt.clim(kmin,kmax)

cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[0],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
#cc2 = plt.contour(LAT2[-1],DEPTH2[-1],potrho[0],levels=clevs_rho,colors='green',linestyles='solid',linewidths=1)

plt.plot(lat_interp,bso_interp_rmean[0][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(exp[0],fontsize=12)

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5); 

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,200,400,600,800,1000],[0,200,400,600,800,1000],fontsize=12)
ax.set_ylabel('Depth [m]',fontsize=14)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(2,3,2)###
cs  = plt.contourf(lat2[-1],depth2[-1],freqn2[1][:,:]-freqn2[-1][:,:],levels=clevs,cmap=cmap2,extend='both')
plt.clim(kmin,kmax)

cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[1],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
#cc3 = plt.contour(LAT2[-1],DEPTH2[-1],potrho[1],levels=clevs_rho,colors='green',linestyles='solid',linewidths=1)

plt.plot(lat_interp,bso_interp_rmean[1][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(exp[1],fontsize=12)

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5);

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,200,400,600,800,1000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(2,3,3)###
cs  = plt.contourf(lat2[-1],depth2[-1],freqn2[2][:,:]-freqn2[-1][:,:],levels=clevs,cmap=cmap2,extend='both')
plt.clim(kmin,kmax)

cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[2],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
#cc3 = plt.contour(LAT2[-1],DEPTH2[-1],potrho[1],levels=clevs_rho,colors='green',linestyles='solid',linewidths=1)

plt.plot(lat_interp,bso_interp_rmean[2][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(exp[2],fontsize=12)

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,200,400,600,800,1000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

cbaxes = fig.add_axes([0.2, 0.42, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=10)
cbar.ax.set_title("N$^2$ 10$^{-4}$ s$^{-2}$",fontsize=14,color='k')

plt.show()
#plt.savefig('STC_freqn2_zonalmean_PAC.png',transparent = False, bbox_inches='tight',dpi=300)


