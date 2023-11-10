import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir  = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'
dirout   = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/Figures'

exp       = ["Stress","Water","Heat","All","control"]
filename1 = ["STC_trans_energy_FAFSTRESS_GLB.nc","STC_trans_energy_FAFWATER_GLB.nc","STC_trans_energy_FAFHEAT_GLB.nc","STC_trans_energy_FAFALL_GLB.nc","STC_trans_energy_flux-only_GLB.nc"]

lat       = [None]*len(exp)
lat30n    = [None]*len(exp)
lat30s    = [None]*len(exp)
latdx     = [None]*len(exp)
mek       = [None]*len(exp)
stc_north = [None]*len(exp)
stc_south = [None]*len(exp)
tau       = [None]*len(exp)
sst       = [None]*len(exp)
dtemp     = [None]*len(exp)
dx        = [None]*len(exp)
dy        = [None]*len(exp)
time      = [None]*len(exp)
mek_zonal_tm       = [None]*len(exp)
stc_north_zonal_tm = [None]*len(exp)
stc_south_zonal_tm = [None]*len(exp)
sst_zonal_tm       = [None]*len(exp)
dtemp_zonal_tm     = [None]*len(exp)
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
    time[i]  = file.variables['TIME'][:]/365 -2188.0
    lat[i]   = file.variables['YT_OCEAN'][:]
    lat30n[i]= file.variables['YU_OCEAN116_142'][:]
    lat30s[i]= file.variables['YU_OCEAN50_76'][:]
    #latdx[i] = file.variables['GRIDLAT_T'][:]
    dx[i]    = file.variables['DX'][:]
    dy[i]    = file.variables['DY'][:]
    mek[i]   = (np.squeeze(file.variables['EKMAN_TRANS'][:])) 
    stc_north[i] = (np.squeeze(file.variables['ESTC_NORTH'][:]))
    stc_south[i] = (np.squeeze(file.variables['ESTC_SOUTH'][:]))
    sst[i]       = np.squeeze(file.variables['TEMP'][:])   
    dtemp[i]     = np.squeeze(file.variables['TEMPGRAD'][:])
    tau[i]       = np.squeeze(file.variables['TAUX'][:])*1e3
    file.close()

for i in range(len(exp)):
    mek_zonal_tm[i]       = np.ma.average(mek[i][61:69],0)
    stc_north_zonal_tm[i] = np.ma.average(stc_north[i][61:69],0)
    stc_south_zonal_tm[i] = np.ma.average(stc_south[i][61:69],0)
    sst_zonal_tm[i]       = np.ma.average(sst[i][61:69],0)
    dtemp_zonal_tm[i]     = np.ma.average(dtemp[i][61:69],0)
    tau_zonal_tm[i]       = np.ma.average(tau[i][61:69],0)

##------------------------PLOTTING
#rc('text', usetex=True)
#rc('figure', figsize=(11.69,8.27))
rc('figure', figsize=(9,11))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

fig = plt.figure(1)

ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(lat30n[i],stc_north_zonal_tm[i]-stc_north_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],[])

plt.title("Change in STC meridional energy transport",fontsize=16)
ax.set_ylabel("[PW]",fontsize=16)
ax.legend(loc=4,fontsize=16)
ax.axis([10,35,-.05,.05])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,1,2)
ax.plot(lat30n[-1],stc_north_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([10,15,20,25,30,35],['10N','15N','20N','25N','30N','35N'])

plt.title("STC meridional energy transport (control)",fontsize=16)
ax.set_ylabel("[PW]",fontsize=16)
ax.axis([10,35,0,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()<
plt.savefig('./Figures/ESTC_change_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(2)
ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(lat[i],mek_zonal_tm[i]-mek_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#plt.xticks([0,10,20,30,40],[])
plt.xticks([-40,-30,-20,-10,0,10,20,30,40],[])

plt.title("Change in Ekman transport",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.legend(loc=4,fontsize=16)
ax.axis([-40,40,-1.5,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,1,2)
ax.plot(lat[-1],mek_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'])

plt.title("Ekman transport (control)",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
#ax.axis([-40,40,-10,40])
ax.axis([-40,40,-40,40])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('./Figures/ESTC_change-ekmantransport_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

rc('figure', figsize=(9,11))
fig = plt.figure(3)
for i in range(len(exp)-1):
    ax1 = fig.add_subplot(4,1,i+1)
    ax1.plot(lat[i],tau_zonal_tm[i]-tau_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0)
    ax2 = ax1.twinx()
    ax2.plot(lat[i],sst_zonal_tm[i]-sst_zonal_tm[-1],color='red',linestyle='solid',linewidth=2.0)

    ax1.set_ylabel("[$10^{-3}$ $N/m^2$]",color='black',fontsize=16)
    ax1.tick_params(axis='y',labelcolor='black',labelsize=16)
    ax1.set_yticks([-4,-2,0,2,4]); ax1.set_yticklabels([-4,-2,0,2,4])
    ax1.axis([-40,40,-4,4])

    ax2.set_ylabel("[$^oC$]",color='red',fontsize=16)
    ax2.tick_params(axis='y',labelcolor='red',labelsize=16)
    ax2.set_yticks([-4,-2,0,2,4]); ax2.set_yticklabels([-4,-2,0,2,4])
    ax2.axis([-40,40,-4,4])

    ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
    ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],[])
plt.title(exp[i],fontsize=16)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'])
ax1.tick_params(axis='x',labelcolor='black',labelsize=16)
plt.xticks(fontsize=16)

#plt.show()
plt.savefig('./Figures/ESTC_change_taux_sst_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

rc('figure', figsize=(9,11))
fig = plt.figure(4)
ax1 = fig.add_subplot(2,1,1)
ax1.plot(lat[-1],tau_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx()
ax2.plot(lat[-1],sst_zonal_tm[-1],color='red',linestyle='solid',linewidth=2.0)

ax1.set_ylabel("[$10^{-3}$ $N/m^2$]",color='black',fontsize=16)
ax1.tick_params(axis='y',labelcolor='black',labelsize=16)
#ax1.set_yticks([-4,-2,0,2,4]); ax1.set_yticklabels([-4,-2,0,2,4])
ax1.axis([-40,40,-80,80])

ax2.tick_params(axis='y',labelcolor='red',labelsize=16)
#ax2.set_yticks([-4,-2,0,2,4]); ax2.set_yticklabels([-4,-2,0,2,4])
ax2.axis([-40,40,10,30])

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],[])
plt.title('Wind stress and SST (control)',fontsize=16)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'])
ax1.tick_params(axis='x',labelcolor='black',labelsize=16)
plt.xticks(fontsize=16)

#plt.show()
plt.savefig('./Figures/ESTC_taux_sst_control_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

######
######

#fig = plt.figure(5)
#ax = fig.add_subplot(1,2,1)
#ax.plot(dx[-1]*1e-7,latdx[-1],color='black',linestyle='solid',linewidth=2.0)

###
#ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
#ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
#ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#plt.yticks([-40,-20,0,20,40,60],['40S','20S',0,'20N','40N','60N'])

#plt.title("Pacific Ocean basin width",fontsize=16)
#ax.set_ylabel("Latitude",fontsize=16); ax.set_xlabel("[$10^7$ m]",fontsize=16)
#ax.axis([0,2,-40,60])

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
#plt.yticks(fontsize=16); plt.xticks(fontsize=16)


#ax = fig.add_subplot(1,2,2)
#ax.plot(dy[-1]*1e-5,latdx[-1],color='black',linestyle='solid',linewidth=2.0)

###
#ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
#ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
#ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#plt.yticks([-40,-20,0,20,40,60],[])
#plt.title("Latitudinal grid width",fontsize=16)
#ax.set_xlabel("[$10^5$ m]",fontsize=16)
#ax.axis([.2,1.2,-40,60])

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
#plt.yticks(fontsize=16); plt.xticks(fontsize=16)

#plt.show()
#plt.savefig('./Figures/ESTC_dx_and_dy_width_PAC.png',transparent = True, bbox_inches='tight',dpi=600)

######
#####

fig = plt.figure(6)
ax = fig.add_subplot(2,1,1)
for i in range(len(exp)):
    ax.plot(lat[i],dtemp_zonal_tm[i]*1e5,color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'])

plt.title("Sea surface temperature gradient",fontsize=16)
ax.set_ylabel("[$1e^{-5}$] $^oC deg^o$",fontsize=16)
ax.legend(loc=4,fontsize=16)
ax.axis([-40,40,-1.5,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,1,2)
ax.plot(lat[-1],dtemp_zonal_tm[-1]*1e5,color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-30,-20,-10,0,10,20,30,40],['40S','30S','20S','10S','0','10N','20N','30N','40N'])

plt.title("Sea surface temperature gradient",fontsize=16)
ax.set_ylabel("[$1e^{-5}$] $^oC deg^o$",fontsize=16)
#ax.axis([-40,60,-1.5,.5])
ax.axis([-40,40,-1.5,.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('./Figures/ESTC_temp-gradient_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(7)
ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(lat[i],sst_zonal_tm[i]-sst_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-20,0,20,40,60],[])

plt.title("Sea surface temperature",fontsize=16)
ax.set_ylabel("[$^oC$]",fontsize=16)
ax.legend(loc=4,fontsize=16)
ax.axis([-40,60,-3,3])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,1,2)
ax.plot(lat[-1],sst_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-20,0,20,40,60],['40S','20S','0','20N','40N','60N'])

plt.title("Sea surface temperature",fontsize=16)
ax.set_ylabel("[$^oC$]",fontsize=16)
ax.axis([-40,60,0,30])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('./Figures/ESTC_temp-zonal_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(8)
ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(lat[i],tau_zonal_tm[i]-tau_zonal_tm[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-20,0,20,40,60],[])

plt.title("Zonal wind stress",fontsize=16)
ax.set_ylabel("[$10^{-3}$ $N/m^2$]",fontsize=16)
ax.legend(loc=4,fontsize=16)
ax.axis([-40,60,-6,6])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

##CONTROL
ax = fig.add_subplot(2,1,2)
ax.plot(lat[-1],tau_zonal_tm[-1],color='black',linestyle='solid',linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([-40,-20,0,20,40,60],['40S','20S','0','20N','40N','60N'])

plt.title("Zonal wind stress",fontsize=16)
ax.set_ylabel("[$10^{-3}$ $N/m^2$] ",fontsize=16)
ax.axis([-40,60,-80,80])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('./Figures/ESTC_taux-zonal_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

