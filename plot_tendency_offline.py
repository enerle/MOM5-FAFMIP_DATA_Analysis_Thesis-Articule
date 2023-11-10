import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp          = ["stress","heat","ctl"]
filename_glb = ["heat_budget_PASSIVEHEAT_FAFSTRESS_GLB.nc","heat_budget_FAFHEAT_GLB.nc","heat_budget_PASSIVEHEAT_GLB.nc"]
filename_soc = ["heat_budget_PASSIVEHEAT_FAFSTRESS_SOC.nc","heat_budget_FAFHEAT_SOC.nc","heat_budget_PASSIVEHEAT_SOC.nc"]
filename_atl = ["heat_budget_PASSIVEHEAT_FAFSTRESS_ATL.nc","heat_budget_FAFHEAT_ATL.nc","heat_budget_PASSIVEHEAT_ATL.nc"]
filename_ipa = ["heat_budget_PASSIVEHEAT_FAFSTRESS_IPA.nc","heat_budget_FAFHEAT_IPA.nc","heat_budget_PASSIVEHEAT_IPA.nc"]
filename_pac = ["heat_budget_PASSIVEHEAT_FAFSTRESS_PAC.nc","heat_budget_FAFHEAT_PAC.nc","heat_budget_PASSIVEHEAT_PAC.nc"]
filename_ind = ["heat_budget_PASSIVEHEAT_FAFSTRESS_IND.nc","heat_budget_FAFHEAT_IND.nc","heat_budget_PASSIVEHEAT_IND.nc"]

dTdt_total_glb      = [None]*len(filename_glb)
dTdt_added_glb      = [None]*len(filename_glb)
dTdt_redist_glb     = [None]*len(filename_glb)
temptend_total_glb  = [None]*len(filename_glb)
temptend_added_glb  = [None]*len(filename_glb)
temptend_redist_glb = [None]*len(filename_glb)

dTdt_total_soc      = [None]*len(filename_soc)
dTdt_added_soc      = [None]*len(filename_soc)
dTdt_redist_soc     = [None]*len(filename_soc)
temptend_total_soc  = [None]*len(filename_soc)
temptend_added_soc  = [None]*len(filename_soc)
temptend_redist_soc = [None]*len(filename_soc)

dTdt_total_atl      = [None]*len(filename_atl)
dTdt_added_atl      = [None]*len(filename_atl)
dTdt_redist_atl     = [None]*len(filename_atl)
temptend_total_atl  = [None]*len(filename_atl)
temptend_added_atl  = [None]*len(filename_atl)
temptend_redist_atl = [None]*len(filename_atl)

dTdt_total_ipa      = [None]*len(filename_ipa)
dTdt_added_ipa      = [None]*len(filename_ipa)
dTdt_redist_ipa     = [None]*len(filename_ipa)
temptend_total_ipa  = [None]*len(filename_ipa)
temptend_added_ipa  = [None]*len(filename_ipa)
temptend_redist_ipa = [None]*len(filename_ipa)

dTdt_total_pac      = [None]*len(filename_pac)
dTdt_added_pac      = [None]*len(filename_pac)
dTdt_redist_pac     = [None]*len(filename_pac)
temptend_total_pac  = [None]*len(filename_pac)
temptend_added_pac  = [None]*len(filename_pac)
temptend_redist_pac = [None]*len(filename_pac)

dTdt_total_ind      = [None]*len(filename_ind)
dTdt_added_ind      = [None]*len(filename_ind)
dTdt_redist_ind     = [None]*len(filename_ind)
temptend_total_ind  = [None]*len(filename_ind)
temptend_added_ind  = [None]*len(filename_ind)
temptend_redist_ind = [None]*len(filename_ind)

###
### temp_tendendy = Cp*rho Int(dT/dt)dz  [W/m2]
###

t=np.arange(0,69)
tyear = 365.25 * 24.0 * 3600.0
#dt = np.ones(len(t))*tyear
dt = tyear
yt =1e-15

for i in range(len(filename_glb)):
    fn = os.path.join(datadir,filename_glb[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_glb[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_glb[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt) 
    dTdt_redist_glb[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_glb[i]  = np.squeeze(np.mean(dTdt_total_glb[i][:]))
    temptend_added_glb[i]  = np.squeeze(np.mean(dTdt_added_glb[i][:]))
    temptend_redist_glb[i] = np.squeeze(np.mean(dTdt_redist_glb[i][:]))
    file.close()

for i in range(len(filename_soc)):
    fn = os.path.join(datadir,filename_soc[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_soc[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_soc[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt)
    dTdt_redist_soc[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_soc[i]  = np.squeeze(np.mean(dTdt_total_soc[i][:]))
    temptend_added_soc[i]  = np.squeeze(np.mean(dTdt_added_soc[i][:]))
    temptend_redist_soc[i] = np.squeeze(np.mean(dTdt_redist_soc[i][:]))
    file.close()

for i in range(len(filename_atl)):
    fn = os.path.join(datadir,filename_atl[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_atl[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_atl[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt)
    dTdt_redist_atl[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_atl[i]  = np.squeeze(np.mean(dTdt_total_atl[i][:]))
    temptend_added_atl[i]  = np.squeeze(np.mean(dTdt_added_atl[i][:]))
    temptend_redist_atl[i] = np.squeeze(np.mean(dTdt_redist_atl[i][:]))
    file.close()

for i in range(len(filename_ipa)):
    fn = os.path.join(datadir,filename_ipa[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_ipa[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_ipa[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt)
    dTdt_redist_ipa[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_ipa[i]  = np.squeeze(np.mean(dTdt_total_ipa[i][:]))
    temptend_added_ipa[i]  = np.squeeze(np.mean(dTdt_added_ipa[i][:]))
    temptend_redist_ipa[i] = np.squeeze(np.mean(dTdt_redist_ipa[i][:]))
    file.close()

for i in range(len(filename_pac)):
    fn = os.path.join(datadir,filename_pac[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_pac[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_pac[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt)
    dTdt_redist_pac[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_pac[i]  = np.squeeze(np.mean(dTdt_total_pac[i][:]))
    temptend_added_pac[i]  = np.squeeze(np.mean(dTdt_added_pac[i][:]))
    temptend_redist_pac[i] = np.squeeze(np.mean(dTdt_redist_pac[i][:]))
    file.close()

for i in range(len(filename_ind)):
    fn = os.path.join(datadir,filename_ind[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
#    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_total_ind[i]  = yt*((file.variables['HEAT_TOTAL'][1:]  - file.variables['HEAT_TOTAL'][:-1])/dt) #dT/dt [W]
    dTdt_added_ind[i]  = yt*((file.variables['HEAT_ADDED'][1:]  - file.variables['HEAT_ADDED'][:-1])/dt)
    dTdt_redist_ind[i] = yt*((file.variables['HEAT_REDIST'][1:] - file.variables['HEAT_REDIST'][:-1])/dt)

    temptend_total_ind[i]  = np.squeeze(np.mean(dTdt_total_ind[i][:]))
    temptend_added_ind[i]  = np.squeeze(np.mean(dTdt_added_ind[i][:]))
    temptend_redist_ind[i] = np.squeeze(np.mean(dTdt_redist_ind[i][:]))
    file.close()

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

colors = ["black","red","blue"]
labels = ["total","added","redist"]

v = [-.1,.5]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):
    ax = fig.add_subplot(3,1,i+1)
    
    ax.plot(1.0,temptend_total_glb[i]-temptend_total_glb[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #total
    ax.plot(0.8,temptend_added_glb[i]-temptend_added_glb[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #added
    ax.plot(1.2,temptend_redist_glb[i]-temptend_redist_glb[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #redist

    ax.plot(3.0,temptend_total_soc[i]-temptend_total_soc[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(2.8,temptend_added_soc[i]-temptend_added_soc[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(3.2,temptend_redist_soc[i]-temptend_redist_soc[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

    ax.plot(5.0,temptend_total_atl[i]-temptend_total_atl[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(4.8,temptend_added_atl[i]-temptend_added_atl[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(5.2,temptend_redist_atl[i]-temptend_redist_atl[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

    ax.plot(7.0,temptend_total_ipa[i]-temptend_total_ipa[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(6.8,temptend_added_ipa[i]-temptend_added_ipa[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(7.2,temptend_redist_ipa[i]-temptend_redist_ipa[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

    ax.plot(9.0,temptend_total_pac[i]-temptend_total_pac[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(8.8,temptend_added_pac[i]-temptend_added_pac[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(9.2,temptend_redist_pac[i]-temptend_redist_pac[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

    ax.plot(11.0,temptend_total_ind[i]-temptend_total_ind[-1],  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
    ax.plot(10.8,temptend_added_ind[i]-temptend_added_ind[-1],  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
    ax.plot(10.8,temptend_redist_ind[i]-temptend_redist_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    
    if i==2: ax.legend(loc=1,ncol=3,fontsize=9);

    ax.set_ylabel("$PW$",fontsize=16)
    plt.ylim((v))

    plt.title(exp[i],style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","","","","","","","","","","","",""],fontsize=16,style='normal')

plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","GLB","","SOC","","ATL","","IPA","","PAC","","IND",""],fontsize=16,style='normal')

plt.show()
#plt.savefig('tendency_online_1.png',transparent = False, bbox_inches='tight',dpi=300) 

#### CONTROL
#v = [-2.5,2.5]

fig = plt.figure(2)
ax = fig.add_subplot(3,1,1)

i=-1

ax.plot(1.0,temptend_total_glb[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #total
ax.plot(0.8,temptend_added_glb[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #added
ax.plot(1.2,temptend_redist_glb[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #redist

ax.plot(3.0,temptend_total_soc[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(2.8,temptend_added_soc[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(3.2,temptend_redist_soc[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

ax.plot(5.0,temptend_total_atl[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(4.8,temptend_added_atl[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(5.2,temptend_redist_atl[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

ax.plot(7.0,temptend_total_ipa[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(6.8,temptend_added_ipa[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(7.2,temptend_redist_ipa[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

ax.plot(9.0,temptend_total_pac[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(8.8,temptend_added_pac[-1],   marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(9.2,temptend_redist_pac[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])

ax.plot(11.0,temptend_total_ind[-1],  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
ax.plot(10.8,temptend_added_ind[-1],  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
ax.plot(10.8,temptend_redist_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

if i==2: ax.legend(loc=1,ncol=3,fontsize=9);

ax.set_ylabel("$PW$",fontsize=16)
#plt.ylim((v))

plt.title(exp[i],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","","","","","","","","","","","",""],fontsize=16,style='normal')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","GLB","","SOC","","ATL","","IPA","","PAC","","IND",""],fontsize=16,style='normal')

plt.show()
#plt.savefig('tendency_online_2.png',transparent = False, bbox_inches='tight',dpi=300)
