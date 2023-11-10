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
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_TEMP-tend/DATA_vInt27-50_latInt'
exp     = ["Global (a)","Atlantic (b)","Pacific (c)","Indian (d)","?"]

filename_glb = ["heat_budget_flux-only_GLB_05S-05N.nc","heat_budget_flux-only_GLB_10S-10N.nc","heat_budget_flux-only_GLB_15S-15N.nc","heat_budget_flux-only_GLB_20S-20N.nc","heat_budget_flux-only_GLB_25S-25N.nc","heat_budget_flux-only_GLB_30S-30N.nc","heat_budget_flux-only_GLB_35S-35N.nc","heat_budget_flux-only_GLB_40S-40N.nc","heat_budget_flux-only_GLB_45S-45N.nc","heat_budget_flux-only_GLB_50S-50N.nc","heat_budget_flux-only_GLB_55S-55N.nc","heat_budget_flux-only_GLB_60S-60N.nc","heat_budget_flux-only_GLB.nc"]
filename_atl = ["heat_budget_flux-only_ATL_05S-05N.nc","heat_budget_flux-only_ATL_10S-10N.nc","heat_budget_flux-only_ATL_15S-15N.nc","heat_budget_flux-only_ATL_20S-20N.nc","heat_budget_flux-only_ATL_25S-25N.nc","heat_budget_flux-only_ATL_30S-30N.nc","heat_budget_flux-only_ATL_35S-35N.nc","heat_budget_flux-only_ATL_40S-40N.nc","heat_budget_flux-only_ATL_45S-45N.nc","heat_budget_flux-only_ATL_50S-50N.nc","heat_budget_flux-only_ATL_55S-55N.nc","heat_budget_flux-only_ATL_60S-60N.nc","heat_budget_flux-only_ATL.nc"]
filename_pac = ["heat_budget_flux-only_PAC_05S-05N.nc","heat_budget_flux-only_PAC_10S-10N.nc","heat_budget_flux-only_PAC_15S-15N.nc","heat_budget_flux-only_PAC_20S-20N.nc","heat_budget_flux-only_PAC_25S-25N.nc","heat_budget_flux-only_PAC_30S-30N.nc","heat_budget_flux-only_PAC_35S-35N.nc","heat_budget_flux-only_PAC_40S-40N.nc","heat_budget_flux-only_PAC_45S-45N.nc","heat_budget_flux-only_PAC_50S-50N.nc","heat_budget_flux-only_PAC_55S-55N.nc","heat_budget_flux-only_PAC_60S-60N.nc","heat_budget_flux-only_PAC.nc"]
filename_ind = ["heat_budget_flux-only_IND_05S-05N.nc","heat_budget_flux-only_IND_10S-10N.nc","heat_budget_flux-only_IND_15S-15N.nc","heat_budget_flux-only_IND_20S-20N.nc","heat_budget_flux-only_IND_25S-25N.nc","heat_budget_flux-only_IND_30S-30N.nc","heat_budget_flux-only_IND_35S-35N.nc","heat_budget_flux-only_IND.nc"]
filename_ipa = ["heat_budget_flux-only_IPA_05S-05N.nc","heat_budget_flux-only_IPA_10S-10N.nc","heat_budget_flux-only_IPA_15S-15N.nc","heat_budget_flux-only_IPA_20S-20N.nc","heat_budget_flux-only_IPA_25S-25N.nc","heat_budget_flux-only_IPA_30S-30N.nc","heat_budget_flux-only_IPA_35S-35N.nc","heat_budget_flux-only_IPA_40S-40N.nc","heat_budget_flux-only_IPA_45S-45N.nc","heat_budget_flux-only_IPA_50S-50N.nc","heat_budget_flux-only_IPA_55S-55N.nc","heat_budget_flux-only_IPA_60S-60N.nc","heat_budget_flux-only_IPA.nc"]

temptend_glb       = [None]*len(filename_glb)
advection_glb      = [None]*len(filename_glb) 
submeso_glb        = [None]*len(filename_glb)
neutral_gm_glb     = [None]*len(filename_glb) 
diapycnal_mix_glb  = [None]*len(filename_glb)
isopycnal_mix_glb  = [None]*len(filename_glb)
swh_glb            = [None]*len(filename_glb)
residual_glb       = [None]*len(filename_glb)
super_residual_glb = [None]*len(filename_glb)
eddy_glb           = [None]*len(filename_glb)
advection_glb      = [None]*len(filename_glb)
total_glb          = [None]*len(filename_glb)
unresolved_glb     = [None]*len(filename_glb)
vdiff_glb          = [None]*len(filename_glb)

temptend_atl       = [None]*len(filename_atl)
advection_atl      = [None]*len(filename_atl) 
submeso_atl        = [None]*len(filename_atl)
neutral_gm_atl     = [None]*len(filename_atl) 
diapycnal_mix_atl  = [None]*len(filename_atl)
isopycnal_mix_atl  = [None]*len(filename_atl)
swh_atl            = [None]*len(filename_atl)
residual_atl       = [None]*len(filename_atl)
super_residual_atl = [None]*len(filename_atl)
eddy_atl           = [None]*len(filename_atl)
advection_atl      = [None]*len(filename_atl)
total_atl          = [None]*len(filename_atl)
unresolved_atl     = [None]*len(filename_atl)
vdiff_atl          = [None]*len(filename_atl)

temptend_ipa       = [None]*len(filename_ipa)
advection_ipa      = [None]*len(filename_ipa) 
submeso_ipa        = [None]*len(filename_ipa)
neutral_gm_ipa     = [None]*len(filename_ipa) 
diapycnal_mix_ipa  = [None]*len(filename_ipa)
isopycnal_mix_ipa  = [None]*len(filename_ipa)
swh_ipa            = [None]*len(filename_ipa)
residual_ipa       = [None]*len(filename_ipa)
super_residual_ipa = [None]*len(filename_ipa)
eddy_ipa           = [None]*len(filename_ipa)
advection_ipa      = [None]*len(filename_ipa)
total_ipa          = [None]*len(filename_ipa)
unresolved_ipa     = [None]*len(filename_ipa)
vdiff_ipa          = [None]*len(filename_ipa)

temptend_pac       = [None]*len(filename_pac)
advection_pac      = [None]*len(filename_pac) 
submeso_pac        = [None]*len(filename_pac)
neutral_gm_pac     = [None]*len(filename_pac) 
diapycnal_mix_pac  = [None]*len(filename_pac)
isopycnal_mix_pac  = [None]*len(filename_pac)
swh_pac            = [None]*len(filename_pac)
residual_pac       = [None]*len(filename_pac)
super_residual_pac = [None]*len(filename_pac)
eddy_pac           = [None]*len(filename_pac)
advection_pac      = [None]*len(filename_pac)
total_pac          = [None]*len(filename_pac)
unresolved_pac     = [None]*len(filename_pac)
vdiff_pac          = [None]*len(filename_pac)

temptend_ind       = [None]*len(filename_ind)
advection_ind      = [None]*len(filename_ind) 
submeso_ind        = [None]*len(filename_ind)
neutral_gm_ind     = [None]*len(filename_ind) 
diapycnal_mix_ind  = [None]*len(filename_ind)
isopycnal_mix_ind  = [None]*len(filename_ind)
swh_ind            = [None]*len(filename_ind)
residual_ind       = [None]*len(filename_ind)
super_residual_ind = [None]*len(filename_ind)
eddy_ind           = [None]*len(filename_ind)
advection_ind      = [None]*len(filename_ind)
total_ind          = [None]*len(filename_ind)
unresolved_ind     = [None]*len(filename_ind)
vdiff_ind          = [None]*len(filename_ind)

yt = 1e-12 

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename_glb)):
    fn = os.path.join(datadir,filename_glb[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_glb[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_glb[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_glb[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_glb[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_glb[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_glb[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_glb[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_glb)):
    residual_glb[i]       = advection_glb[i] + submeso_glb[i] + neutral_gm_glb[i]
    eddy_glb[i]           =                    submeso_glb[i] + neutral_gm_glb[i]
    super_residual_glb[i] = advection_glb[i] + submeso_glb[i] + neutral_gm_glb[i] + isopycnal_mix_glb[i]
    total_glb[i]          = advection_glb[i] + submeso_glb[i] + neutral_gm_glb[i] + isopycnal_mix_glb[i] + diapycnal_mix_glb[i] + swh_glb[i]
    unresolved_glb[i]     = temptend_glb[i]  - total_glb[i]
    vdiff_glb[i]          = diapycnal_mix_glb[i] + swh_glb[i] + unresolved_glb[i]

for i in range(len(filename_atl)):
    fn = os.path.join(datadir,filename_atl[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_atl[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_atl[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_atl[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_atl[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_atl[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_atl[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_atl[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_atl)):
    residual_atl[i]       = advection_atl[i] + submeso_atl[i] + neutral_gm_atl[i]
    eddy_atl[i]           =                    submeso_atl[i] + neutral_gm_atl[i]
    super_residual_atl[i] = advection_atl[i] + submeso_atl[i] + neutral_gm_atl[i] + isopycnal_mix_atl[i]
    total_atl[i]          = advection_atl[i] + submeso_atl[i] + neutral_gm_atl[i] + isopycnal_mix_atl[i] + diapycnal_mix_atl[i] + swh_atl[i]
    unresolved_atl[i]     = temptend_atl[i]  - total_atl[i]
    vdiff_atl[i]          = diapycnal_mix_atl[i] + swh_atl[i] + unresolved_atl[i]

for i in range(len(filename_ipa)):
    fn = os.path.join(datadir,filename_ipa[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_ipa[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_ipa[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_ipa[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_ipa[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_ipa[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_ipa[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_ipa[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_ipa)):
    residual_ipa[i]       = advection_ipa[i] + submeso_ipa[i] + neutral_gm_ipa[i]
    eddy_ipa[i]           =                    submeso_ipa[i] + neutral_gm_ipa[i]
    super_residual_ipa[i] = advection_ipa[i] + submeso_ipa[i] + neutral_gm_ipa[i] + isopycnal_mix_ipa[i]
    total_ipa[i]          = advection_ipa[i] + submeso_ipa[i] + neutral_gm_ipa[i] + isopycnal_mix_ipa[i] + diapycnal_mix_ipa[i] + swh_ipa[i]
    unresolved_ipa[i]     = temptend_ipa[i]  - total_ipa[i]
    vdiff_ipa[i]          = diapycnal_mix_ipa[i] + swh_ipa[i] + unresolved_ipa[i]

for i in range(len(filename_pac)):
    fn = os.path.join(datadir,filename_pac[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_pac[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_pac[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_pac[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_pac[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_pac[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_pac[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_pac[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_pac)):
    residual_pac[i]       = advection_pac[i] + submeso_pac[i] + neutral_gm_pac[i]
    eddy_pac[i]           =                    submeso_pac[i] + neutral_gm_pac[i]
    super_residual_pac[i] = advection_pac[i] + submeso_pac[i] + neutral_gm_pac[i] + isopycnal_mix_pac[i]
    total_pac[i]          = advection_pac[i] + submeso_pac[i] + neutral_gm_pac[i] + isopycnal_mix_pac[i] + diapycnal_mix_pac[i] + swh_pac[i]
    unresolved_pac[i]     = temptend_pac[i]  - total_pac[i]
    vdiff_pac[i]          = diapycnal_mix_pac[i] + swh_pac[i] + unresolved_pac[i]

for i in range(len(filename_ind)):
    fn = os.path.join(datadir,filename_ind[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_ind[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_ind[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_ind[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_ind[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_ind[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_ind[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_ind[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_ind)):
    residual_ind[i]       = advection_ind[i] + submeso_ind[i] + neutral_gm_ind[i]
    eddy_ind[i]           =                    submeso_ind[i] + neutral_gm_ind[i]
    super_residual_ind[i] = advection_ind[i] + submeso_ind[i] + neutral_gm_ind[i] + isopycnal_mix_ind[i]
    total_ind[i]          = advection_ind[i] + submeso_ind[i] + neutral_gm_ind[i] + isopycnal_mix_ind[i] + diapycnal_mix_ind[i] + swh_ind[i]
    unresolved_ind[i]     = temptend_ind[i]  - total_ind[i]
    vdiff_ind[i]          = diapycnal_mix_ind[i] + swh_ind[i] + unresolved_ind[i]

rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(7,14))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["NET","ADV","EDDY","rADV","ISO","vDIFF","srADV","unres"]

v = [-2500,2500]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

##Global
ax = fig.add_subplot(4,1,1)
ax.plot(temptend_glb[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(advection_glb[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_glb[:],          marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_glb[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_glb[:], marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(vdiff_glb[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(super_residual_glb[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=3,ncol=3,fontsize=9);

ax.set_ylabel("TW",fontsize=16)
#ax.set_xlabel("$Latitude$",fontsize=16)
ax.axis([0,13,-2500,2500])

plt.title(exp[0],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","T"],fontsize=16,style='normal')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[],fontsize=16,style='normal')

#plt.savefig('tendency_online_CTL_latInt-sens_GLB.png',transparent = False, bbox_inches='tight',dpi=300)

#
#fig = plt.figure(2)
#fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)
#
##Atlantic
ax = fig.add_subplot(4,1,2)
ax.plot(temptend_atl[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(advection_atl[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_atl[:],          marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_atl[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_atl[:], marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(vdiff_atl[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(super_residual_atl[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("TW",fontsize=16)
ax.axis([-1,13,-600,600])

plt.title(exp[1],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[],fontsize=16,style='normal')

##Pacific
ax = fig.add_subplot(4,1,3)
ax.plot(temptend_pac[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(advection_pac[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_pac[:],          marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_pac[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_pac[:], marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(vdiff_pac[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(super_residual_pac[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("TW",fontsize=16)
ax.axis([-1,13,-600,600])

plt.title(exp[2],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],[],fontsize=16,style='normal')

##indian
ax = fig.add_subplot(4,1,4)
ax.plot(temptend_ind[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
ax.plot(advection_ind[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
ax.plot(eddy_ind[:],          marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
ax.plot(residual_ind[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
ax.plot(isopycnal_mix_ind[:], marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
ax.plot(vdiff_ind[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
ax.plot(super_residual_ind[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#ax.legend(loc=4,ncol=3,fontsize=9);

ax.set_ylabel("TW",fontsize=16)
#plt.ylim([-300,300])
ax.axis([-1,13,-600,600])

plt.title(exp[3],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","T"],fontsize=16,style='normal')
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","T"],fontsize=16,style='normal')


###Indian
#ax = fig.add_subplot(4,1,4)
#ax.plot(temptend_ind[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[0],label=labels[0])
#ax.plot(advection_ind[:],     marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[1],label=labels[1])
#ax.plot(eddy_ind[:],          marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[2],label=labels[2])
#ax.plot(residual_ind[:],      marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[3],label=labels[3])
#ax.plot(isopycnal_mix_ind[:], marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[4],label=labels[4])
#ax.plot(vdiff_ind[:],         marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[5],label=labels[5])
#ax.plot(super_residual_ind[:],marker='o',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[6],label=labels[6])
#ax.plot(unresolved_ind[:],    marker='*',markersize=6,color='k',linewidth=.5,markerfacecolor=colors[7],label=labels[7])
#
#ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
#ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
#ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
#
#ax.legend(loc=4,ncol=3,fontsize=9);
#
#ax.set_ylabel("$PW$",fontsize=16)
#ax.set_xlabel("$Latitude$",fontsize=16)
#plt.ylim((v))
#
#plt.title(exp[4],style='normal',fontsize=16)
#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["5","10","15","20","25","30","35","40","45","50","55","60","T"],fontsize=16,style='normal')

#plt.show()
plt.savefig('tendency_online_CTL_latInt-sens.png',transparent = False, bbox_inches='tight',dpi=300)
