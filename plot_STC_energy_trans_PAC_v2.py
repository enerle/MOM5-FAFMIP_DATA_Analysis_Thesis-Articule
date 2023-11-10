import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'
#datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'

#exp       = ["faf-stress","faf-heat","control"]
#filename1 = ["STC_trans_energy_FAFSTRESS_PAC.nc","STC_trans_energy_FAFHEAT_PAC.nc","STC_trans_energy_flux-only_PAC.nc"]

exp       = ["faf-stress","faf-water","faf-heat","Control"]
filename1 = ["STC_trans_energy_FAFSTRESS_PAC.nc","STC_trans_energy_FAFWATER_PAC.nc","STC_trans_energy_FAFHEAT_PAC.nc","STC_trans_energy_flux-only_PAC.nc"]

lat       = [None]*len(exp)
lat30n    = [None]*len(exp)
lat30s    = [None]*len(exp)
latdx     = [None]*len(exp)
mek       = [None]*len(exp)
stc_north = [None]*len(exp)
stc_south = [None]*len(exp)
tau       = [None]*len(exp)
time      = [None]*len(exp)

tgrad_north_mean = [None]*len(exp)
tgrad_south_mean = [None]*len(exp)
trans_north_max  = [None]*len(exp)
trans_south_max  = [None]*len(exp)
taux_north_max   = [None]*len(exp)
taux_south_max   = [None]*len(exp)
estc_north_max   = [None]*len(exp)
estc_south_max   = [None]*len(exp)

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
    time[i]  = file.variables['TIME'][:]/365 -2188.0
    lat[i]   = file.variables['YT_OCEAN'][:]
    lat30n[i]= file.variables['YU_OCEAN116_142'][:]
    lat30s[i]= file.variables['YU_OCEAN50_76'][:]
    mek[i]       = np.squeeze(np.mean(file.variables['EKMAN_TRANS'][:][61:70],0))
    stc_north[i] = np.squeeze(np.mean(file.variables['ESTC_NORTH'][:][61:70],0))
    stc_south[i] = np.squeeze(np.mean(file.variables['ESTC_SOUTH'][:][61:70],0))
    tau[i]       = np.squeeze(np.mean(file.variables['TAUX'][:][61:70],0))*1e3
    tgrad_north_mean[i] = np.mean(file.variables['TEMPGRAD_NORTH_MEAN'][61:70]) 
    tgrad_south_mean[i] = np.mean(file.variables['TEMPGRAD_SOUTH_MEAN'][61:70])
    trans_north_max[i]  = np.mean(file.variables['MEK_10N'][61:70])
    trans_south_max[i]  = np.mean(file.variables['MEK_10S'][61:70])
    taux_north_max[i]   = np.mean(file.variables['TAUX_10N'][61:70])
    taux_south_max[i]   = np.mean(file.variables['TAUX_10S'][61:70])
    estc_north_max[i]   = np.mean(file.variables['ESTC_10N'][61:70])
    estc_south_max[i]   = np.mean(file.variables['ESTC_10S'][61:70])
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
#rc('figure', figsize=(11.69,8.27))
rc('figure', figsize=(9,11))

colors = ['black','blue','red','gray']
styles = ['solid','solid','solid','solid']

fig = plt.figure(1)

#southern hemisphere
ax = fig.add_subplot(2,2,1)


for i in range(len(exp)-1):
    ax.plot(-lat30s[i],stc_south[i]-stc_south[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])
plt.yticks([-.04,-.02,0,.02,.04,.06,.08,1],[-.04,-.02,0,.02,.04,.06,.08,1])

plt.title("SH anomalies (a)",fontsize=16)
ax.set_ylabel("PW",fontsize=16)
ax.legend(loc=1,fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
##

##nnorthern hemisphere
ax = fig.add_subplot(2,2,2)
for i in range(len(exp)-1):
    ax.plot(lat30n[i],stc_north[i]-stc_north[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])
plt.yticks([-.04,-.02,0,.02,.04,.06,.08,1],[])

plt.title("NH anomalies (b)",fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,2,3)
ax.plot(-lat30s[-1],stc_south[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],['10S','15S','20S','25S','30S','35S'])
plt.yticks([0,.1,.2,.3,.4,.5],[0,.1,.2,.3,.4,.5])

plt.title("SH control (c)",fontsize=16)
ax.set_ylabel("PW",fontsize=16)
ax.axis([10,35,0,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

## north
ax = fig.add_subplot(2,2,4)
ax.plot(lat30n[-1],stc_north[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],['10N','15N','20N','25N','30N','35N'])
plt.yticks([0,.1,.2,.3,.4,.5],[])

plt.title("NH control (d)",fontsize=16)
#ax.set_ylabel("PW",fontsize=16)
ax.axis([10,35,0,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)

#plt.show()
plt.savefig('ESTC_change_PAC.png',transparent = True, bbox_inches='tight',dpi=600)

