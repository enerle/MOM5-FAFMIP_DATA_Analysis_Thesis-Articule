import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc
import decimal
from decimal import Decimal

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/ART/DATA_TEMP-tend/DATA_vInt_MLD_BSO_v2'
#datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/ART/DATA_TEMP-tend/DATA_vInt_MLD_BSO'

#exp            = ["Stress","Water","Heat","All","flux-only"]
#filename = ['STC_temptend_FAFSTRESS_NORTH_PAC.nc','STC_temptend_FAFWATER_NORTH_PAC.nc','STC_temptend_FAFHEAT_NORTH_PAC.nc','STC_temptend_FAFALL_NORTH_PAC.nc','STC_temptend_flux-only_NORTH_PAC.nc']

#exp            = ["Stress","Water","Heat","flux-only"]
#filename = ['STC_temptend_FAFSTRESS_NORTH_PAC.nc','STC_temptend_FAFWATER_NORTH_PAC.nc','STC_temptend_FAFHEAT_NORTH_PAC.nc','STC_temptend_flux-only_NORTH_PAC.nc']

exp            = ["Stress","Heat","Control"]
exp            = ["(d) faf-stress","(f) faf-heat","(b) control"]
filename = ['STC_temptend_FAFSTRESS_NORTH_PAC.nc','STC_temptend_FAFHEAT_NORTH_PAC.nc','STC_temptend_flux-only_NORTH_PAC.nc']

#exp            = ["Stress","Water","Heat","Control"]
#exp            = ["(f) faf-stress","(g) faf-water","(h) faf-heat","(e) Control"]
#filename = ['STC_temptend_FAFSTRESS_NORTH_PAC.nc','STC_temptend_FAFWATER_NORTH_PAC.nc','STC_temptend_FAFHEAT_NORTH_PAC.nc','STC_temptend_flux-only_NORTH_PAC.nc']


time              = [None]*len(filename)
temptend          = [None]*len(filename)
advection         = [None]*len(filename) 
submeso           = [None]*len(filename)
neutral_gm        = [None]*len(filename) 
diapycnal_mix     = [None]*len(filename)
isopycnal_mix     = [None]*len(filename)
swh               = [None]*len(filename)
residual          = [None]*len(filename)
super_residual    = [None]*len(filename)
eddy              = [None]*len(filename)
advection         = [None]*len(filename)
total             = [None]*len(filename)
unresolved        = [None]*len(filename)
vdiff             = [None]*len(filename)

temptend_int      = [None]*len(filename)
advection_int     = [None]*len(filename)
submeso_int       = [None]*len(filename)
neutral_gm_int    = [None]*len(filename)
diapycnal_mix_int = [None]*len(filename)
isopycnal_mix_int = [None]*len(filename)
swh_int           = [None]*len(filename)
residual_int      = [None]*len(filename)
super_residual_int= [None]*len(filename)
eddy_int          = [None]*len(filename)
advection_int     = [None]*len(filename)
total_int         = [None]*len(filename)
unresolved_int    = [None]*len(filename)
vdiff_int         = [None]*len(filename)

temptend_stc      = [None]*len(filename)
advection_stc     = [None]*len(filename)
submeso_stc       = [None]*len(filename)
neutral_gm_stc    = [None]*len(filename)
diapycnal_mix_stc = [None]*len(filename)
isopycnal_mix_stc = [None]*len(filename)
swh_stc           = [None]*len(filename)
residual_stc      = [None]*len(filename)
super_residual_stc= [None]*len(filename)
eddy_stc          = [None]*len(filename)
advection_stc     = [None]*len(filename)
total_stc         = [None]*len(filename)
unresolved_stc    = [None]*len(filename)
vdiff_stc         = [None]*len(filename)

#yt = 1e-15
yt = 1e-12

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time[i]              = file.variables['TIME'][:]/365-2188
    temptend[i]          = Decimal(np.mean(file.variables['TEMPTEND_TOT'][61:70])*yt)
    advection[i]         = Decimal(np.mean(file.variables['ADVECTION_TOT'][61:70])*yt)
    submeso[i]           = Decimal(np.mean(file.variables['SUBMESO_TOT'][61:70])*yt)
    neutral_gm[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM_TOT'][61:70])*yt)
    diapycnal_mix[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_TOT'][61:70])*yt)
    isopycnal_mix[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_TOT'][61:70])*yt)
    swh[i]               = Decimal(np.mean(file.variables['SWH_TOT'][61:70])*yt)
    
    temptend_stc[i]      = Decimal(np.mean(file.variables['TEMPTEND_STC'][61:70])*yt)
    advection_stc[i]     = Decimal(np.mean(file.variables['ADVECTION_STC'][61:70])*yt)
    submeso_stc[i]       = Decimal(np.mean(file.variables['SUBMESO_STC'][61:70])*yt)
    neutral_gm_stc[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_STC'][61:70])*yt)
    diapycnal_mix_stc[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_STC'][61:70])*yt)
    isopycnal_mix_stc[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_STC'][61:70])*yt)
    swh_stc[i]           = Decimal(np.mean(file.variables['SWH_STC'][61:70])*yt)
    
    temptend_int[i]      = Decimal(np.mean(file.variables['TEMPTEND_INT'][61:70])*yt)
    advection_int[i]     = Decimal(np.mean(file.variables['ADVECTION_INT'][61:70])*yt)
    submeso_int[i]       = Decimal(np.mean(file.variables['SUBMESO_INT'][61:70])*yt)
    neutral_gm_int[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_INT'][61:70])*yt)
    diapycnal_mix_int[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_INT'][61:70])*yt)
    isopycnal_mix_int[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_INT'][61:70])*yt)
    swh_int[i]           = Decimal(np.mean(file.variables['SWH_INT'][61:70])*yt)
    
    file.close()

for i in range(len(filename)):
    residual[i]       = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]           =                submeso[i] + neutral_gm[i]
    super_residual[i] = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i]
    total[i]          = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i] + diapycnal_mix[i] + swh[i]
    unresolved[i]     = temptend[i]  - total[i]
    vdiff[i]          = diapycnal_mix[i] + swh[i] + unresolved[i]

    residual_stc[i]       = advection_stc[i] + submeso_stc[i] + neutral_gm_stc[i]
    eddy_stc[i]           =                    submeso_stc[i] + neutral_gm_stc[i]
    super_residual_stc[i] = advection_stc[i] + submeso_stc[i] + neutral_gm_stc[i] + isopycnal_mix_stc[i]
    total_stc[i]          = advection_stc[i] + submeso_stc[i] + neutral_gm_stc[i] + isopycnal_mix_stc[i] + diapycnal_mix_stc[i] + swh_stc[i]
    unresolved_stc[i]     = temptend_stc[i]  - total_stc[i]
    vdiff_stc[i]          = diapycnal_mix_stc[i] + swh_stc[i] + unresolved_stc[i]

    residual_int[i]       = advection_int[i] + submeso_int[i] + neutral_gm_int[i]
    eddy_int[i]           =                    submeso_int[i] + neutral_gm_int[i]
    super_residual_int[i] = advection_int[i] + submeso_int[i] + neutral_gm_int[i] + isopycnal_mix_int[i]
    total_int[i]          = advection_int[i] + submeso_int[i] + neutral_gm_int[i] + isopycnal_mix_int[i] + diapycnal_mix_int[i] + swh_int[i]
    unresolved_int[i]     = temptend_int[i]  - total_int[i]
    vdiff_int[i]          = diapycnal_mix_int[i] + swh_int[i] +unresolved_int[i]


rc('figure', figsize=(7,14))
#rc('figure', figsize=(8.27,11))
#rc('figure', figsize=(8.27,11.69))
#rc('figure', figsize=(11.69,8.27))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[.5,.5,1],[.7,.7,.7],[1,1,1]]
labels = ["NET","ADV","EDDY","rADV","ISO","vDIFF","srADV"]

fig = plt.figure(1)

#v = [-.05,.11] #this is for the description
v = [-50,110] 

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.2,wspace=0.12)

for i in range(len(exp)-1):
    ax = fig.add_subplot(4,1,i+2)
    ax.plot(1.0,temptend[i]-temptend[-1],            marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0]) #net
    ax.plot(0.6,advection[i]-advection[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1]) #advection
    ax.plot(0.6,eddy[i]-eddy[-1],                    marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
    ax.plot(0.6,residual[i]-residual[-1],            marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
    ax.plot(1.4,isopycnal_mix[i]-isopycnal_mix[-1],  marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
    ax.plot(1.0,vdiff[i]-vdiff[-1],                  marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5]) #diapycnal 
    ax.plot(1.0,super_residual[i]-super_residual[-1],marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6]) #superresidual
    
    ax.plot(3.0,temptend_stc[i]-temptend_stc[-1],            marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0]) 
    ax.plot(2.6,advection_stc[i]-advection_stc[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1]) 
    ax.plot(2.6,eddy_stc[i]-eddy_stc[-1],                    marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2]) 
    ax.plot(2.6,residual_stc[i]-residual_stc[-1],            marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(3.4,isopycnal_mix_stc[i]-isopycnal_mix_stc[-1],  marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4]) 
    ax.plot(3.0,vdiff_stc[i]-vdiff_stc[-1],                  marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5]) 
    ax.plot(3.0,super_residual_stc[i]-super_residual_stc[-1],marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6]) 
     
    ax.plot(5.0,temptend_int[i]-temptend_int[-1],            marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
    ax.plot(4.6,advection_int[i]-advection_int[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
    ax.plot(4.6,eddy_int[i]-eddy_int[-1],                    marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
    ax.plot(4.6,residual_int[i]-residual_int[-1],            marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
    ax.plot(5.4,isopycnal_mix_int[i]-isopycnal_mix_int[-1],  marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
    ax.plot(5.0,vdiff_int[i]-vdiff_int[-1],                  marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])
    ax.plot(5.0,super_residual_int[i]-super_residual_int[-1],marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6],label=labels[6])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    #if i==0: ax.legend(loc=1,ncol=3,fontsize=10);

    ax.set_ylabel("TW",fontsize=16)
    plt.ylim((v))

    plt.title(exp[i],style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
    plt.xticks([0,1,2,3,4,5,6],[])
#    plt.yticks([-4,-2,0,2,4,6,8,10],[])

plt.xticks([0,1,2,3,4,5,6],["","Total","","Shallow","","Deep",""],fontsize=16,style='normal')
#plt.yticks([-4,-2,0,2,4,6,8,10],[])

####plt.show()
###plt.savefig('STC_OHC_PAC_NORTH_diag_tend_online_ART.png',transparent = False, bbox_inches='tight',dpi=300)

###
##control

#v = [-1.5,1.5] #this is for the description
v = [-1500,1500]

#fig = plt.figure(3)
#fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(4,1,1)

ax.plot(1.0,temptend[-1],          marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0]) #net
ax.plot(0.6,advection[-1],         marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1]) #advection
ax.plot(0.6,eddy[-1],              marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
ax.plot(0.6,residual[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
ax.plot(1.4,isopycnal_mix[-1],     marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
ax.plot(1.0,vdiff[-1],             marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5]) #diapycnal
ax.plot(1.0,super_residual[-1],    marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6]) #superresidual

ax.plot(3.0,temptend_stc[-1],      marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(2.6,advection_stc[-1],     marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(2.6,eddy_stc[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2])
ax.plot(2.6,residual_stc[-1],      marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3])
ax.plot(3.4,isopycnal_mix_stc[-1], marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4])
ax.plot(3.0,vdiff_stc[-1],         marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5])
ax.plot(3.0,super_residual_stc[-1],marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6])

ax.plot(5.0,temptend_int[-1],      marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
ax.plot(4.6,advection_int[-1],     marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
ax.plot(4.6,eddy_int[-1],          marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
ax.plot(4.6,residual_int[-1],      marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
ax.plot(5.4,isopycnal_mix_int[-1], marker='o',markersize=6,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
ax.plot(5.0,vdiff_int[-1],         marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])
ax.plot(5.0,super_residual_int[-1],marker='o',markersize=9,color='k',linewidth=0,markerfacecolor=colors[6],label=labels[6])

######

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#ax.legend(loc=1,ncol=2,fontsize=9);

ax.set_ylabel("TW",fontsize=16)
plt.ylim((v))

plt.title(exp[-1],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6],[])
#plt.yticks([-150,-100,-50,50,100,150],[])

fig.suptitle("Northern Hemisphere",fontweight='normal',fontsize=15,x=.20,y=.98)

#plt.show()

plt.savefig('STC_OHC_PAC_NORTH_diag_tend_online_CTL_FAFMIP_vART_vmay27.png',transparent = False, bbox_inches='tight',dpi=300)


