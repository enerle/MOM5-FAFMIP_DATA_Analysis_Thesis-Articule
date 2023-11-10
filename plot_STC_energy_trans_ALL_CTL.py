import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'

exp       = ["Pacific","Atlantic","Indian"]
filename1 = ["STC_trans_energy_flux-only_PAC.nc","STC_trans_energy_flux-only_ATL.nc","STC_trans_energy_flux-only_IND.nc"]

lat                = [None]*len(exp)
lat30n             = [None]*len(exp)
lat30s             = [None]*len(exp)
mek                = [None]*len(exp)
stc_north          = [None]*len(exp)
stc_south          = [None]*len(exp)
tau                = [None]*len(exp)
mek_zonal_tm       = [None]*len(exp)
stc_north_zonal_tm = [None]*len(exp)
stc_south_zonal_tm = [None]*len(exp)
tau_zonal_tm       = [None]*len(exp)

#---## Latitude factor
file = nc.Dataset('/home/clima-archive2/rfarneti/DATA/FAFMIP_ESM2M/CTL/ocean.static.nc')
geolat = file.variables['geolat_t'][:,:]
grad_geolat = np.gradient(geolat, axis=0)
dl = 1./grad_geolat[:,90]
##---##

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    lat[i]       = file.variables['YT_OCEAN'][:]
    lat30n[i]    = file.variables['YU_OCEAN116_142'][:]
    lat30s[i]    = file.variables['YU_OCEAN50_76'][:]
    mek[i]       = (np.squeeze(file.variables['EKMAN_TRANS'][:])) 
    stc_north[i] = (np.squeeze(file.variables['ESTC_NORTH'][:]))
    stc_south[i] = (np.squeeze(file.variables['ESTC_SOUTH'][:]))
    tau[i]       = np.squeeze(file.variables['TAUX'][:])*1e3
    file.close()

for i in range(len(exp)):
    mek_zonal_tm[i]       = np.ma.average(mek[i][61:69],0)
    stc_north_zonal_tm[i] = np.ma.average(stc_north[i][61:69],0)
    stc_south_zonal_tm[i] = np.ma.average(stc_south[i][61:69],0)
    tau_zonal_tm[i]       = np.ma.average(tau[i][61:69],0)

##------------------------PLOTTING
rc('figure', figsize=(9,11))

colors  = ['black','blue','red']
markers = ['s','o','D']
basin_n = ["Northern Pacific","Northern Atlantic"]
basin_s = ["Southern Pacific","Southern Atlantic","Indian"]

fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)-1):
    ax.plot(lat30n[i],stc_north_zonal_tm[i],color='black',linestyle='solid',linewidth=1.5,marker=markers[i],markerfacecolor='white',label=basin_n[i])
    ax.plot(-lat30s[i],stc_south_zonal_tm[i],color='black',linestyle='solid',linewidth=1.5,marker=markers[i],markerfacecolor='black',label=basin_s[i])
ax.plot(-lat30s[-1],stc_south_zonal_tm[-1],color='black',linestyle='solid',linewidth=1.5,marker=markers[-1],markerfacecolor='black',label=basin_s[-1])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],['10N','15N','20N','25N','30N','35N'])
plt.yticks([0,0.05,.1,.15,.2,.25,.3,.35,.4,.45,.5],[0,0.05,.1,.15,.2,.25,.3,.35,.4,.45,.5])

plt.title("STC meridional energy transport (control)",fontsize=16)
ax.set_ylabel("[PW]",fontsize=16)
ax.legend(loc=1,fontsize=16)
ax.axis([10,35,0,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ESTC_ALL_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)):
    ax.plot(lat[i],mek_zonal_tm[i],color=colors[i],linestyle='solid',linewidth=2.0,label=exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-30,-20,-10,0,10,20,30],['30S','20S','10S','0','10N','20N','30N'])
plt.yticks([-50,-40,-30,-20,-10,0,10,20,30,40,50],[-50,-40,-30,-20,-10,0,10,20,30,40,50])

plt.title("Ekman transport (control)",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.legend(loc=1,fontsize=16)
ax.axis([-35,35,-50,50])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ESTC_change-ekmantransport_ALL_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

##CONTROL
fig = plt.figure(3)
ax = fig.add_subplot(1,1,1)
for i in range(len(exp)):
    ax.plot(lat[i],tau_zonal_tm[i],color=colors[i],linestyle='solid',linewidth=2.0,label=exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-30,-20,-10,0,10,20,30],['30S','20S','10S','0','10N','20N','30N'])

plt.title("Zonal wind stress",fontsize=16)
ax.set_ylabel("[$10^{-3}$ $N/m^2$] ",fontsize=16)
ax.legend(loc=1,fontsize=16)
ax.axis([-35,35,-90,60])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ESTC_taux-zonal_ALL_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

