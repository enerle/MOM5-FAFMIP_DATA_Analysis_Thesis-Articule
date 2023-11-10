import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp      = ["Stress","Water","Heat","All","flux-only"]
filename = ["STC_OHC_FAFSTRESS_GLB_time.nc","STC_OHC_FAFWATER_GLB_time.nc","STC_OHC_FAFHEAT_GLB_time.nc","STC_OHC_FAFALL_GLB_time.nc","STC_OHC_flux-only_GLB_time.nc"]
#filename2 = ["STC_OHC_FAFSTRESS_GLB_zonal.nc","STC_OHC_FAFWATER_GLB_zonal.nc","STC_OHC_FAFHEAT_GLB_zonal.nc","STC_OHC_FAFALL_GLB_zonal.nc","STC_OHC_flux-only_GLB_zonal.nc"]

time        = [None]*len(exp)

OHC_stc     = [None]*len(exp)
OHC_int     = [None]*len(exp)
OHC_tot     = [None]*len(exp)

dTdt_stc    = [None]*len(exp)
dTdt_int    = [None]*len(exp)
dTdt_tot    = [None]*len(exp)

OHC_stc_sum = [None]*len(exp)
OHC_int_sum = [None]*len(exp)
OHC_tot_sum = [None]*len(exp)

t=np.arange(0,69)
tyear = 365.25 * 24.0 * 3600.0
dt = np.ones(len(t))*tyear

yt =1e-15

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time[i]    = file.variables['TIME'][:]/365-2188
    dTdt_tot[i] = yt*((file.variables['OHC_TOT'][1:] - file.variables['OHC_TOT'][:-1])/dt) #dT/dt [W]
    dTdt_stc[i] = yt*((file.variables['OHC_STC'][1:] - file.variables['OHC_STC'][:-1])/dt)
    dTdt_int[i] = yt*((file.variables['OHC_INT'][1:] - file.variables['OHC_INT'][:-1])/dt)

    OHC_tot_sum[i] = np.squeeze(np.mean(dTdt_tot[i][:]))
    OHC_stc_sum[i] = np.squeeze(np.mean(dTdt_stc[i][:]))
    OHC_int_sum[i] = np.squeeze(np.mean(dTdt_int[i][:]))
    file.close()
    
#------------------------PLOTTING
#====================================================
colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i][1:69],dTdt_tot[i][1:69]-dTdt_tot[-1][1:69],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.legend(loc=2,fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Total')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[],fontsize=16)
####

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i][1:69],dTdt_stc[i][1:69]-dTdt_stc[-1][1:69],color=colors[i],linestyle=styles[i],linewidth=2.0)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Overturn')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[],fontsize=16)

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(time[i][1:69],dTdt_int[i][1:69]-dTdt_int[-1][1:69],color=colors[i],linestyle=styles[i],linewidth=2.0)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
ax.set_ylabel('$[PW]$',fontsize=16)
ax.axis([0,70,-.2,.6])

plt.title('Interior')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16)

#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_offline_time.png',transparent = True, bbox_inches='tight',dpi=600)

###################
###################
##control

fig = plt.figure(2)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)
ax = fig.add_subplot(3,1,1)
i=-1
ax.plot(time[i][1:69],dTdt_tot[i][1:69],color='black',linestyle='solid',linewidth=2.0,label='Total')
ax.plot(time[i][1:69],dTdt_stc[i][1:69],color='red',linestyle='solid',linewidth=2.0,label='Overturn')
ax.plot(time[i][1:69],dTdt_int[i][1:69],color='blue',linestyle='solid',linewidth=2.0,label='Interior')
####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$[PW]$',fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=2,fontsize=10)
#ax.axis([0,70,-.05,.20])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line

plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70],fontsize=16)
####

#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_offline_time_CTL.png',transparent = True, bbox_inches='tight',dpi=600)


####
#total heat budget by scenario
###############recuperar del original
v = [-.05,.35]

fig = plt.figure(3)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(2,1,1)

ax.plot(0.8,OHC_stc_sum[0]-OHC_stc_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(1.0,OHC_int_sum[0]-OHC_int_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(1.2,OHC_tot_sum[0]-OHC_tot_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(2.8,OHC_stc_sum[1]-OHC_stc_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(3.0,OHC_int_sum[1]-OHC_int_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(3.2,OHC_tot_sum[1]-OHC_tot_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(4.8,OHC_stc_sum[2]-OHC_stc_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(5.0,OHC_int_sum[2]-OHC_int_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(5.2,OHC_tot_sum[2]-OHC_tot_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(6.8,OHC_stc_sum[3]-OHC_stc_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red',label='$\Delta \partial_t T_{Overturn}$')
ax.plot(7.0,OHC_int_sum[3]-OHC_int_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue',label='$\Delta \partial_t T_{Interior}$')
ax.plot(7.2,OHC_tot_sum[3]-OHC_tot_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black',label='$\Delta \partial_T T_{Total}$')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=2,ncol=1,fontsize=12);

ax.set_ylabel('$[PW]$',fontsize=16)
plt.ylim((v))

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","","","","","","","","","",""],fontsize=16,style='normal')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","stress","","water","","heat","","all","","ctl",""],fontsize=16,style='normal')

#plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_offline_budget.png',transparent = True, bbox_inches='tight',dpi=600)

ax = fig.add_subplot(2,1,2)

ax.plot(0.8,OHC_stc_sum[0],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(1.0,OHC_int_sum[0],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(1.2,OHC_tot_sum[0],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(2.8,OHC_stc_sum[1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(3.0,OHC_int_sum[1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(3.2,OHC_tot_sum[1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(4.8,OHC_stc_sum[2],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(5.0,OHC_int_sum[2],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(5.2,OHC_tot_sum[2],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(6.8,OHC_stc_sum[3],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red')
ax.plot(7.0,OHC_int_sum[3],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue')
ax.plot(7.2,OHC_tot_sum[3],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black')

ax.plot(8.8,OHC_stc_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='red',label='$\partial_t T_{Overturn}$')
ax.plot(9.0,OHC_int_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='blue',label='$\partial_t T_{Interior}$')
ax.plot(9.2,OHC_tot_sum[-1],marker='o',markersize=10,color='k',linewidth=0,markerfacecolor='black',label='$\partial_T T_{Total}$')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=2,ncol=1,fontsize=12);

ax.set_ylabel('$[PW]$',fontsize=16)
plt.ylim((v))

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","","","","","","","","","",""],fontsize=16,style='normal')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","stress","","water","","heat","","all","","ctl",""],fontsize=16,style='normal')

plt.show()
#plt.savefig('STC_OHC_GLB_diag_tend_offline_budget.png',transparent = True, bbox_inches='tight',dpi=600)
