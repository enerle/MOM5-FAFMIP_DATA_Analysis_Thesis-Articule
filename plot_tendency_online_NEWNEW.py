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
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_TEMP-tend/DATA_vInt27-50'

exp          = ["faf-stress (b)","faf-water (c)","faf-heat (d)","Control (a)"]
filename_glb = ["heat_budget_FAFSTRESS_GLB.nc","heat_budget_FAFWATER_GLB.nc","heat_budget_FAFHEAT_GLB.nc","heat_budget_flux-only_GLB.nc"]
filename_atl = ["heat_budget_FAFSTRESS_ATL.nc","heat_budget_FAFWATER_ATL.nc","heat_budget_FAFHEAT_ATL.nc","heat_budget_flux-only_ATL.nc"]
filename_ipa = ["heat_budget_FAFSTRESS_IPA.nc","heat_budget_FAFWATER_IPA.nc","heat_budget_FAFHEAT_IPA.nc","heat_budget_flux-only_IPA.nc"]
filename_pac = ["heat_budget_FAFSTRESS_PAC.nc","heat_budget_FAFWATER_PAC.nc","heat_budget_FAFHEAT_PAC.nc","heat_budget_flux-only_PAC.nc"]
filename_ind = ["heat_budget_FAFSTRESS_IND.nc","heat_budget_FAFWATER_IND.nc","heat_budget_FAFHEAT_IND.nc","heat_budget_flux-only_IND.nc"]
filename_soc = ["heat_budget_FAFSTRESS_SOC.nc","heat_budget_FAFWATER_SOC.nc","heat_budget_FAFHEAT_SOC.nc","heat_budget_flux-only_SOC.nc"]

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

temptend_soc       = [None]*len(filename_soc)
advection_soc      = [None]*len(filename_soc) 
submeso_soc        = [None]*len(filename_soc)
neutral_gm_soc     = [None]*len(filename_soc) 
diapycnal_mix_soc  = [None]*len(filename_soc)
isopycnal_mix_soc  = [None]*len(filename_soc)
swh_soc            = [None]*len(filename_soc)
residual_soc       = [None]*len(filename_soc)
super_residual_soc = [None]*len(filename_soc)
eddy_soc           = [None]*len(filename_soc)
advection_soc      = [None]*len(filename_soc)
total_soc          = [None]*len(filename_soc)
unresolved_soc     = [None]*len(filename_soc)
vdiff_soc          = [None]*len(filename_soc)

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

for i in range(len(filename_soc)):
    fn = os.path.join(datadir,filename_soc[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    temptend_soc[i]          = Decimal(np.mean(file.variables['TEMPTEND'][61:70])*yt)
    advection_soc[i]         = Decimal(np.mean(file.variables['ADVECTION'][61:70])*yt)
    submeso_soc[i]           = Decimal(np.mean(file.variables['SUBMESO'][61:70])*yt)
    neutral_gm_soc[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM'][61:70])*yt)
    diapycnal_mix_soc[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT'][61:70])*yt)
    isopycnal_mix_soc[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION'][61:70])*yt)
    swh_soc[i]               = Decimal(np.mean(file.variables['SWH'][61:70])*yt)
    file.close()
for i in range(len(filename_soc)):
    residual_soc[i]       = advection_soc[i] + submeso_soc[i] + neutral_gm_soc[i]
    eddy_soc[i]           =                    submeso_soc[i] + neutral_gm_soc[i]
    super_residual_soc[i] = advection_soc[i] + submeso_soc[i] + neutral_gm_soc[i] + isopycnal_mix_soc[i]
    total_soc[i]          = advection_soc[i] + submeso_soc[i] + neutral_gm_soc[i] + isopycnal_mix_soc[i] + diapycnal_mix_soc[i] + swh_soc[i]
    unresolved_soc[i]     = temptend_soc[i]  - total_soc[i]
    vdiff_soc[i]          = diapycnal_mix_soc[i] + swh_soc[i] + unresolved_soc[i]

rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(7,14))

colors = [[0,0,0],[1,0,0],[1,.5,.5],[1,.95,0],[.5,.5,1],[.7,.7,.7],[1,1,1],[1,1,1]]
labels = ["NET","ADV","EDDY","rADV","ISO","vDIFF","srADV","unres"]

v = [-200,500]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):
    ax = fig.add_subplot(4,1,i+2)
    ax.plot(1.0,temptend_glb[i]-temptend_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #net
    ax.plot(0.8,advection_glb[i]-advection_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #advection
    ax.plot(0.8,eddy_glb[i]-eddy_glb[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
    ax.plot(0.8,residual_glb[i]-residual_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
    ax.plot(1.2,isopycnal_mix_glb[i]-isopycnal_mix_glb[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
    ax.plot(1.0,vdiff_glb[i]-vdiff_glb[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) #vertical diffusion
    ax.plot(1.0,super_residual_glb[i]-super_residual_glb[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6]) #super residual

    ax.plot(3.0,temptend_soc[i]-temptend_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(2.8,advection_soc[i]-advection_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(2.8,eddy_soc[i]-eddy_soc[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(2.8,residual_soc[i]-residual_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(3.2,isopycnal_mix_soc[i]-isopycnal_mix_soc[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(3.0,vdiff_soc[i]-vdiff_soc[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(3.0,super_residual_soc[i]-super_residual_soc[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

    ax.plot(5.0,temptend_atl[i]-temptend_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(4.8,advection_atl[i]-advection_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(4.8,eddy_atl[i]-eddy_atl[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(4.8,residual_atl[i]-residual_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(5.2,isopycnal_mix_atl[i]-isopycnal_mix_atl[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(5.0,vdiff_atl[i]-vdiff_atl[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(5.0,super_residual_atl[i]-super_residual_atl[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

#    ax.plot(7.0,temptend_ipa[i]-temptend_ipa[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
#    ax.plot(6.8,advection_ipa[i]-advection_ipa[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
#    ax.plot(6.8,eddy_ipa[i]-eddy_ipa[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
#    ax.plot(6.8,residual_ipa[i]-residual_ipa[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
#    ax.plot(7.2,isopycnal_mix_ipa[i]-isopycnal_mix_ipa[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
#    ax.plot(7.0,vdiff_ipa[i]-vdiff_ipa[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
#    ax.plot(7.0,super_residual_ipa[i]-super_residual_ipa[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

    ax.plot(7.0,temptend_pac[i]-temptend_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
    ax.plot(6.8,advection_pac[i]-advection_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
    ax.plot(6.8,eddy_pac[i]-eddy_pac[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
    ax.plot(6.8,residual_pac[i]-residual_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
    ax.plot(7.2,isopycnal_mix_pac[i]-isopycnal_mix_pac[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
    ax.plot(7.0,vdiff_pac[i]-vdiff_pac[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
    ax.plot(7.0,super_residual_pac[i]-super_residual_pac[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

    ax.plot(9.0,temptend_ind[i]-temptend_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
    ax.plot(8.8,advection_ind[i]-advection_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
    ax.plot(8.8,eddy_ind[i]-eddy_ind[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
    ax.plot(8.8,residual_ind[i]-residual_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
    ax.plot(9.2,isopycnal_mix_ind[i]-isopycnal_mix_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
    ax.plot(9.0,vdiff_ind[i]-vdiff_ind[-1],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])
    ax.plot(9.0,super_residual_ind[i]-super_residual_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6],label=labels[6])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

#    if i==2: ax.legend(loc=1,ncol=3,fontsize=9);

    ax.set_ylabel("TW",fontsize=16)
    plt.ylim((v))

    plt.title(exp[i],style='normal',fontsize=16)
    plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
#    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12],["","","","","","","","","","","","",""],fontsize=16,style='normal')
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","","","","","","","","","",""],fontsize=16,style='normal')

plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","GLB","","SOC","","ATL","","PAC","","IND",""],fontsize=16,style='normal')

#plt.show()
#plt.savefig('tendency_online_FAFMIP.png',transparent = False, bbox_inches='tight',dpi=300)

v = [-2000,2000]

#fig = plt.figure(2)
#fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(4,1,1)
ax.plot(1.0,temptend_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0]) #net
ax.plot(0.8,advection_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1]) #advection
ax.plot(0.8,eddy_glb[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2]) #eddy
ax.plot(0.8,residual_glb[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3]) #residual
ax.plot(1.2,isopycnal_mix_glb[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4]) #isopycnal
ax.plot(1.0,vdiff_glb[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5]) #vertical diffusion
ax.plot(1.0,super_residual_glb[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6]) #super residual

ax.plot(3.0,temptend_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(2.8,advection_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(2.8,eddy_soc[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
ax.plot(2.8,residual_soc[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
ax.plot(3.2,isopycnal_mix_soc[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
ax.plot(3.0,vdiff_soc[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
ax.plot(3.0,super_residual_soc[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

ax.plot(5.0,temptend_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(4.8,advection_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(4.8,eddy_atl[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
ax.plot(4.8,residual_atl[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
ax.plot(5.2,isopycnal_mix_atl[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
ax.plot(5.0,vdiff_atl[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
ax.plot(5.0,super_residual_atl[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

ax.plot(7.0,temptend_pac[i]-temptend_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0])
ax.plot(6.8,advection_pac[i]-advection_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1])
ax.plot(6.8,eddy_pac[i]-eddy_pac[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2])
ax.plot(6.8,residual_pac[i]-residual_pac[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3])
ax.plot(7.2,isopycnal_mix_pac[i]-isopycnal_mix_pac[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4])
ax.plot(7.0,vdiff_pac[i]-vdiff_pac[-1],            marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5])
ax.plot(7.0,super_residual_pac[i]-super_residual_pac[-1], marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6])

ax.plot(9.0,temptend_ind[i]-temptend_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[0],label=labels[0])
ax.plot(8.8,advection_ind[i]-advection_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[1],label=labels[1])
ax.plot(8.8,eddy_ind[i]-eddy_ind[-1],                  marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[2],label=labels[2])
ax.plot(8.8,residual_ind[i]-residual_ind[-1],          marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[3],label=labels[3])
ax.plot(9.2,isopycnal_mix_ind[i]-isopycnal_mix_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[4],label=labels[4])
ax.plot(9.0,vdiff_ind[i]-vdiff_ind[-1],                marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[5],label=labels[5])
ax.plot(9.0,super_residual_ind[i]-super_residual_ind[-1],marker='o',markersize=8,color='k',linewidth=0,markerfacecolor=colors[6],label=labels[6])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=1,ncol=2,fontsize=9);

ax.set_ylabel("TW",fontsize=16)
plt.ylim((v))

plt.title(exp[-1],style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","","","","","","","","","",""],fontsize=16,style='normal')
#plt.xticks([0,1,2,3,4,5,6,7,8,9,10],["","GLB","","SOC","","ATL","","IPA","","PAC",""],fontsize=16,style='normal')

#plt.show()
###plt.savefig('tendency_online_CTL.png',transparent = False, bbox_inches='tight',dpi=300)
#plt.savefig('tendency_online_CTL_and_FAFMIP.png',transparent = False, bbox_inches='tight',dpi=300)


print("& exp & NET &ADV & EDDY & ISO & DIA & SWH & UNRES & R-ADV & SR-ADV & VDIFF ")
for i in range(len(exp)-1):
    print("%s " %exp[i])
    print("\centering GLB" + " & %.1f " %(temptend_glb[i]-temptend_glb[-1]) + " & %.1f " %(advection_glb[i]-advection_glb[-1]) + " & %.1f " %(eddy_glb[i]-eddy_glb[-1])  + " & %.1f " %(isopycnal_mix_glb[i]-isopycnal_mix_glb[-1]) + " & %.1f " %(diapycnal_mix_glb[i]-diapycnal_mix_glb[-1]) + " & %.1f " %(swh_glb[i]-swh_glb[-1]) + " & %.1f " %(unresolved_glb[i]-unresolved_glb[-1]) + " & %.1f " %(residual_glb[i]-residual_glb[-1]) + " & %.1f " %(super_residual_glb[i]-super_residual_glb[-1]) + " & %.1f " %(vdiff_glb[i]-vdiff_glb[-1]))
    print("\centering SOC" + " & %.1f " %(temptend_soc[i]-temptend_soc[-1]) + " & %.1f " %(advection_soc[i]-advection_soc[-1]) + " & %.1f " %(eddy_soc[i]-eddy_soc[-1])  + " & %.1f " %(isopycnal_mix_soc[i]-isopycnal_mix_soc[-1]) + " & %.1f " %(diapycnal_mix_soc[i]-diapycnal_mix_soc[-1]) + " & %.1f " %(swh_soc[i]-swh_soc[-1]) + " & %.1f " %(unresolved_soc[i]-unresolved_soc[-1]) + " & %.1f " %(residual_soc[i]-residual_soc[-1]) + " & %.1f " %(super_residual_soc[i]-super_residual_soc[-1]) + " & %.1f " %(vdiff_soc[i]-vdiff_soc[-1]))
    print("\centering ATL" + " & %.1f " %(temptend_atl[i]-temptend_atl[-1]) + " & %.1f " %(advection_atl[i]-advection_atl[-1]) + " & %.1f " %(eddy_atl[i]-eddy_atl[-1])  + " & %.1f " %(isopycnal_mix_atl[i]-isopycnal_mix_atl[-1]) + " & %.1f " %(diapycnal_mix_atl[i]-diapycnal_mix_atl[-1]) + " & %.1f " %(swh_atl[i]-swh_atl[-1]) + " & %.1f " %(unresolved_atl[i]-unresolved_atl[-1]) + " & %.1f " %(residual_atl[i]-residual_atl[-1]) + " & %.1f " %(super_residual_atl[i]-super_residual_atl[-1]) + " & %.1f " %(vdiff_atl[i]-vdiff_atl[-1]))
    print("\centering PAC" + " & %.1f " %(temptend_pac[i]-temptend_pac[-1]) + " & %.1f " %(advection_pac[i]-advection_pac[-1]) + " & %.1f " %(eddy_pac[i]-eddy_pac[-1])  + " & %.1f " %(isopycnal_mix_pac[i]-isopycnal_mix_pac[-1]) + " & %.1f " %(diapycnal_mix_pac[i]-diapycnal_mix_pac[-1]) + " & %.1f " %(swh_pac[i]-swh_pac[-1]) + " & %.1f " %(unresolved_pac[i]-unresolved_pac[-1]) + " & %.1f " %(residual_pac[i]-residual_pac[-1]) + " & %.1f " %(super_residual_pac[i]-super_residual_pac[-1]) + " & %.1f " %(vdiff_pac[i]-vdiff_pac[-1]))
    print("\centering IND" + " & %.1f " %(temptend_ind[i]-temptend_ind[-1]) + " & %.1f " %(advection_ind[i]-advection_ind[-1]) + " & %.1f " %(eddy_ind[i]-eddy_ind[-1])  + " & %.1f " %(isopycnal_mix_ind[i]-isopycnal_mix_ind[-1]) + " & %.1f " %(diapycnal_mix_ind[i]-diapycnal_mix_ind[-1]) + " & %.1f " %(swh_ind[i]-swh_ind[-1]) + " & %.1f " %(unresolved_ind[i]-unresolved_ind[-1]) + " & %.1f " %(residual_ind[i]-residual_ind[-1]) + " & %.1f " %(super_residual_ind[i]-super_residual_ind[-1]) + " & %.1f " %(vdiff_ind[i]-vdiff_ind[-1]))


##control

print("& exp & NET &ADV & EDDY & ISO & DIA & SWH & UNRES & R-ADV & SR-ADV & VDIFF ")
for i in range(len(exp)):
    print("%s " %exp[i])
    print("\centering GLB" + " & %.1f " %(temptend_glb[i]) + " & %.1f " %(advection_glb[i]) + " & %.1f " %(eddy_glb[i])  + " & %.1f " %(isopycnal_mix_glb[i]) + " & %.1f " %(diapycnal_mix_glb[i]) + " & %.1f " %(swh_glb[i]) + " & %.1f " %(unresolved_glb[i]) + " & %.1f " %(residual_glb[i]) + " & %.1f " %(super_residual_glb[i]) + " & %.1f " %(vdiff_glb[i]))
    print("\centering SOC" + " & %.1f " %(temptend_soc[i]) + " & %.1f " %(advection_soc[i]) + " & %.1f " %(eddy_soc[i])  + " & %.1f " %(isopycnal_mix_soc[i]) + " & %.1f " %(diapycnal_mix_soc[i]) + " & %.1f " %(swh_soc[i]) + " & %.1f " %(unresolved_soc[i]) + " & %.1f " %(residual_soc[i]) + " & %.1f " %(super_residual_soc[i]) + " & %.1f " %(vdiff_soc[i]))
    print("\centering ATL" + " & %.1f " %(temptend_atl[i]) + " & %.1f " %(advection_atl[i]) + " & %.1f " %(eddy_atl[i])  + " & %.1f " %(isopycnal_mix_atl[i]) + " & %.1f " %(diapycnal_mix_atl[i]) + " & %.1f " %(swh_atl[i]) + " & %.1f " %(unresolved_atl[i]) + " & %.1f " %(residual_atl[i]) + " & %.1f " %(super_residual_atl[i]) + " & %.1f " %(vdiff_atl[i])
    print("\centering PAC" + " & %.1f " %(temptend_pac[i]) + " & %.1f " %(advection_pac[i]) + " & %.1f " %(eddy_pac[i])  + " & %.1f " %(isopycnal_mix_pac[i]) + " & %.1f " %(diapycnal_mix_pac[i]) + " & %.1f " %(swh_pac[i]) + " & %.1f " %(unresolved_pac[i]) + " & %.1f " %(residual_pac[i]) + " & %.1f " %(super_residual_pac[i]) + " & %.1f " %(vdiff_pac[i]))
    print("\centering IND" + " & %.1f " %(temptend_ind[i]) + " & %.1f " %(advection_ind[i]) + " & %.1f " %(eddy_ind[i])  + " & %.1f " %(isopycnal_mix_ind[i]) + " & %.1f " %(diapycnal_mix_ind[i]) + " & %.1f " %(swh_ind[i]) + " & %.1f " %(unresolved_ind[i]) + " & %.1f " %(residual_ind[i]) + " & %.1f " %(super_residual_ind[i]) + " & %.1f " %(vdiff_ind[i]))






































