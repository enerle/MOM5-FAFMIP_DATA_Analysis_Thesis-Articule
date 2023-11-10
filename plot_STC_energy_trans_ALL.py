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

exp       = ["Stress","Water","Heat","All","control"]
filename1 = ["STC_trans_energy_FAFSTRESS_PAC.nc","STC_trans_energy_FAFWATER_PAC.nc","STC_trans_energy_FAFHEAT_PAC.nc","STC_trans_energy_FAFALL_PAC.nc","STC_trans_energy_flux-only_PAC.nc"]
filename2 = ["STC_trans_energy_FAFSTRESS_ATL.nc","STC_trans_energy_FAFWATER_ATL.nc","STC_trans_energy_FAFHEAT_ATL.nc","STC_trans_energy_FAFALL_ATL.nc","STC_trans_energy_flux-only_ATL.nc"]
filename3 = ["STC_trans_energy_FAFSTRESS_IND.nc","STC_trans_energy_FAFWATER_IND.nc","STC_trans_energy_FAFHEAT_IND.nc","STC_trans_energy_FAFALL_IND.nc","STC_trans_energy_flux-only_IND.nc"]

lat30_north_pac = [None]*len(exp)
lat30_south_pac = [None]*len(exp)
lat30_north_atl = [None]*len(exp)
lat30_south_atl = [None]*len(exp)
lat30_south_ind = [None]*len(exp)
stc_north_pac   = [None]*len(exp)
stc_south_pac   = [None]*len(exp)
stc_north_atl   = [None]*len(exp)
stc_south_atl   = [None]*len(exp)
stc_south_ind   = [None]*len(exp)
stc_north_pac_zonal_tm = [None]*len(exp)
stc_south_pac_zonal_tm = [None]*len(exp)
stc_north_atl_zonal_tm = [None]*len(exp)
stc_south_atl_zonal_tm = [None]*len(exp)
stc_south_ind_zonal_tm = [None]*len(exp)

#---## Latitude factor
file = nc.Dataset('/home/clima-archive2/rfarneti/DATA/FAFMIP_ESM2M/CTL/ocean.static.nc')
geolat = file.variables['geolat_t'][:,:]
grad_geolat = np.gradient(geolat, axis=0)
dl = 1./grad_geolat[:,90]
##---##

#---> Pacific
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    lat30_north_pac[i] = file.variables['YU_OCEAN116_142'][:]
    lat30_south_pac[i] = file.variables['YU_OCEAN50_76'][:]
    stc_north_pac[i]   = (np.squeeze(file.variables['ESTC_NORTH'][:]))
    stc_south_pac[i]   = (np.squeeze(file.variables['ESTC_SOUTH'][:]))
    file.close()
for i in range(len(exp)):
    stc_north_pac_zonal_tm[i] = np.ma.average(stc_north_pac[i][61:69],0)
    stc_south_pac_zonal_tm[i] = np.ma.average(stc_south_pac[i][61:69],0)

#---> Atlantic
for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Working on ", fn)
    file = nc.Dataset(fn)
    lat30_north_atl[i] = file.variables['YU_OCEAN116_142'][:]
    lat30_south_atl[i] = file.variables['YU_OCEAN50_76'][:]
    stc_north_atl[i]   = (np.squeeze(file.variables['ESTC_NORTH'][:]))
    stc_south_atl[i]   = (np.squeeze(file.variables['ESTC_SOUTH'][:]))
    file.close()
for i in range(len(exp)):
    stc_north_atl_zonal_tm[i] = np.ma.average(stc_north_atl[i][61:69],0)
    stc_south_atl_zonal_tm[i] = np.ma.average(stc_south_atl[i][61:69],0)

#---> Indian
for i in range(len(exp)):
    fn = os.path.join(datadir,filename3[i])
    print("Working on ", fn)
    file = nc.Dataset(fn)
    lat30_south_ind[i] = file.variables['YU_OCEAN50_76'][:]
    stc_south_ind[i]   = (np.squeeze(file.variables['ESTC_SOUTH'][:]))
    file.close()
for i in range(len(exp)):
    stc_south_ind_zonal_tm[i] = np.ma.average(stc_south_ind[i][61:69],0)


##------------------------PLOTTING
rc('figure', figsize=(9,11))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

fig = plt.figure(1)

ax = fig.add_subplot(3,2,1)
for i in range(len(exp)-1):
    ax.plot(-lat30_south_pac[i],stc_south_pac_zonal_tm[i]-stc_south_pac_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])
plt.yticks([-.05,-.025,0,.025,.05,.075,.1],[-.05,-.025,0,.025,.05,.075,.1])

plt.title("South",fontsize=16)
ax.set_ylabel("Pacific [PW]",fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,2,2)
for i in range(len(exp)-1):
    ax.plot(lat30_north_pac[i],stc_north_pac_zonal_tm[i]-stc_north_pac_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])
plt.yticks([-.05,-.025,0,.025,.05,.075,.1],[])

plt.title("North",fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##Atlantic
ax = fig.add_subplot(3,2,3)
for i in range(len(exp)-1):
    ax.plot(lat30_north_atl[i],stc_north_atl_zonal_tm[i]-stc_north_atl_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])
plt.yticks([-.05,-.025,0,.025,.05,.075,.1],[-.05,-.025,0,.025,.05,.075,.1])

ax.set_ylabel("Atlantic [PW]",fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,2,4)
for i in range(len(exp)-1):
    ax.plot(-lat30_south_atl[i],stc_south_atl_zonal_tm[i]-stc_south_atl_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[10,15,20,25,30,35])
plt.yticks([-.05,-.025,0,.025,.05,.075,.1],[])

ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

## Indian

ax = fig.add_subplot(3,2,5)
for i in range(len(exp)-1):
    ax.plot(-lat30_south_ind[i],stc_south_ind_zonal_tm[i]-stc_south_ind_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],['10','15','20','25','30','35'])
plt.yticks([-.05,-.025,0,.025,.05,.075,.1],[-.05,-.025,0,.025,.05,.075,.1])

ax.set_ylabel("Indian [PW]",fontsize=16)
ax.legend(loc=1,fontsize=16)
ax.axis([10,35,-.05,.1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ESTC_change_ALL.png',transparent = True, bbox_inches='tight',dpi=600)
