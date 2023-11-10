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

exp            = ["Stress","Water","Heat","All","flux-only"]
filename_north = ['STC_temptend_FAFSTRESS_NORTH_PAC.nc','STC_temptend_FAFWATER_NORTH_PAC.nc','STC_temptend_FAFHEAT_NORTH_PAC.nc','STC_temptend_FAFALL_NORTH_PAC.nc','STC_temptend_flux-only_NORTH_PAC.nc']
filename_south = ['STC_temptend_FAFSTRESS_SOUTH_PAC.nc','STC_temptend_FAFWATER_SOUTH_PAC.nc','STC_temptend_FAFHEAT_SOUTH_PAC.nc','STC_temptend_FAFALL_SOUTH_PAC.nc','STC_temptend_flux-only_SOUTH_PAC.nc']

time_north              = [None]*len(filename_north)
temptend_north          = [None]*len(filename_north)
advection_north         = [None]*len(filename_north) 
submeso_north           = [None]*len(filename_north)
neutral_gm_north        = [None]*len(filename_north) 
diapycnal_mix_north     = [None]*len(filename_north)
isopycnal_mix_north     = [None]*len(filename_north)
swh_north               = [None]*len(filename_north)
residual_north          = [None]*len(filename_north)
super_residual_north    = [None]*len(filename_north)
eddy_north              = [None]*len(filename_north)
advection_north         = [None]*len(filename_north)
total_north             = [None]*len(filename_north)
unresolved_north        = [None]*len(filename_north)
vdiff_north             = [None]*len(filename_north)

temptend_int_north      = [None]*len(filename_north)
advection_int_north     = [None]*len(filename_north)
submeso_int_north       = [None]*len(filename_north)
neutral_gm_int_north    = [None]*len(filename_north)
diapycnal_mix_int_north = [None]*len(filename_north)
isopycnal_mix_int_north = [None]*len(filename_north)
swh_int_north           = [None]*len(filename_north)
residual_int_north      = [None]*len(filename_north)
super_residual_int_north= [None]*len(filename_north)
eddy_int_north          = [None]*len(filename_north)
advection_int_north     = [None]*len(filename_north)
total_int_north         = [None]*len(filename_north)
unresolved_int_north    = [None]*len(filename_north)
vdiff_int_north         = [None]*len(filename_north)

temptend_stc_north      = [None]*len(filename_north)
advection_stc_north     = [None]*len(filename_north)
submeso_stc_north       = [None]*len(filename_north)
neutral_gm_stc_north    = [None]*len(filename_north)
diapycnal_mix_stc_north = [None]*len(filename_north)
isopycnal_mix_stc_north = [None]*len(filename_north)
swh_stc_north           = [None]*len(filename_north)
residual_stc_north      = [None]*len(filename_north)
super_residual_stc_north= [None]*len(filename_north)
eddy_stc_north          = [None]*len(filename_north)
advection_stc_north     = [None]*len(filename_north)
total_stc_north         = [None]*len(filename_north)
unresolved_stc_north    = [None]*len(filename_north)
vdiff_stc_north         = [None]*len(filename_north)

time_south              = [None]*len(filename_south)
temptend_south          = [None]*len(filename_south)
advection_south         = [None]*len(filename_south)
submeso_south           = [None]*len(filename_south)
neutral_gm_south        = [None]*len(filename_south)
diapycnal_mix_south     = [None]*len(filename_south)
isopycnal_mix_south     = [None]*len(filename_south)
swh_south               = [None]*len(filename_south)
residual_south          = [None]*len(filename_south)
super_residual_south    = [None]*len(filename_south)
eddy_south              = [None]*len(filename_south)
advection_south         = [None]*len(filename_south)
total_south             = [None]*len(filename_south)
unresolved_south        = [None]*len(filename_south)
vdiff_south             = [None]*len(filename_south)

temptend_int_south      = [None]*len(filename_south)
advection_int_south     = [None]*len(filename_south)
submeso_int_south       = [None]*len(filename_south)
neutral_gm_int_south    = [None]*len(filename_south)
diapycnal_mix_int_south = [None]*len(filename_south)
isopycnal_mix_int_south = [None]*len(filename_south)
swh_int_south           = [None]*len(filename_south)
residual_int_south      = [None]*len(filename_south)
super_residual_int_south= [None]*len(filename_south)
eddy_int_south          = [None]*len(filename_south)
advection_int_south     = [None]*len(filename_south)
total_int_south         = [None]*len(filename_south)
unresolved_int_south    = [None]*len(filename_south)
vdiff_int_south         = [None]*len(filename_south)

temptend_stc_south      = [None]*len(filename_south)
advection_stc_south     = [None]*len(filename_south)
submeso_stc_south       = [None]*len(filename_south)
neutral_gm_stc_south    = [None]*len(filename_south)
diapycnal_mix_stc_south = [None]*len(filename_south)
isopycnal_mix_stc_south = [None]*len(filename_south)
swh_stc_south           = [None]*len(filename_south)
residual_stc_south      = [None]*len(filename_south)
super_residual_stc_south= [None]*len(filename_south)
eddy_stc_south          = [None]*len(filename_south)
advection_stc_south     = [None]*len(filename_south)
total_stc_south         = [None]*len(filename_south)
unresolved_stc_south    = [None]*len(filename_south)
vdiff_stc_south         = [None]*len(filename_south)

yt = 1e-12 

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename_north)):
    fn = os.path.join(datadir,filename_north[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_north[i]              = file.variables['TIME'][:]/365-2188
    temptend_north[i]          = Decimal(np.mean(file.variables['TEMPTEND_TOT'][61:70])*yt)
    advection_north[i]         = Decimal(np.mean(file.variables['ADVECTION_TOT'][61:70])*yt)
    submeso_north[i]           = Decimal(np.mean(file.variables['SUBMESO_TOT'][61:70])*yt)
    neutral_gm_north[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM_TOT'][61:70])*yt)
    diapycnal_mix_north[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_TOT'][61:70])*yt)
    isopycnal_mix_north[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_TOT'][61:70])*yt)
    swh_north[i]               = Decimal(np.mean(file.variables['SWH_TOT'][61:70])*yt)
    
    temptend_stc_north[i]      = Decimal(np.mean(file.variables['TEMPTEND_STC'][61:70])*yt)
    advection_stc_north[i]     = Decimal(np.mean(file.variables['ADVECTION_STC'][61:70])*yt)
    submeso_stc_north[i]       = Decimal(np.mean(file.variables['SUBMESO_STC'][61:70])*yt)
    neutral_gm_stc_north[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_STC'][61:70])*yt)
    diapycnal_mix_stc_north[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_STC'][61:70])*yt)
    isopycnal_mix_stc_north[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_STC'][61:70])*yt)
    swh_stc_north[i]           = Decimal(np.mean(file.variables['SWH_STC'][61:70])*yt)
    
    temptend_int_north[i]      = Decimal(np.mean(file.variables['TEMPTEND_INT'][61:70])*yt)
    advection_int_north[i]     = Decimal(np.mean(file.variables['ADVECTION_INT'][61:70])*yt)
    submeso_int_north[i]       = Decimal(np.mean(file.variables['SUBMESO_INT'][61:70])*yt)
    neutral_gm_int_north[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_INT'][61:70])*yt)
    diapycnal_mix_int_north[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_INT'][61:70])*yt)
    isopycnal_mix_int_north[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_INT'][61:70])*yt)
    swh_int_north[i]           = Decimal(np.mean(file.variables['SWH_INT'][61:70])*yt)
    
    file.close()

for i in range(len(filename_north)):
    residual_north[i]       = advection_north[i] + submeso_north[i] + neutral_gm_north[i]
    eddy_north[i]           =                      submeso_north[i] + neutral_gm_north[i]
    super_residual_north[i] = advection_north[i] + submeso_north[i] + neutral_gm_north[i] + isopycnal_mix_north[i]
    total_north[i]          = advection_north[i] + submeso_north[i] + neutral_gm_north[i] + isopycnal_mix_north[i] + diapycnal_mix_north[i] + swh_north[i]
    unresolved_north[i]     = temptend_north[i]  - total_north[i]
    vdiff_north[i]          = diapycnal_mix_north[i] + swh_north[i] + unresolved_north[i]

    residual_stc_north[i]       = advection_stc_north[i] + submeso_stc_north[i] + neutral_gm_stc_north[i]
    eddy_stc_north[i]           =                          submeso_stc_north[i] + neutral_gm_stc_north[i]
    super_residual_stc_north[i] = advection_stc_north[i] + submeso_stc_north[i] + neutral_gm_stc_north[i] + isopycnal_mix_stc_north[i]
    total_stc_north[i]          = advection_stc_north[i] + submeso_stc_north[i] + neutral_gm_stc_north[i] + isopycnal_mix_stc_north[i] + diapycnal_mix_stc_north[i] + swh_stc_north[i]
    unresolved_stc_north[i]     = temptend_stc_north[i]  - total_stc_north[i]
    vdiff_stc_north[i]          = diapycnal_mix_stc_north[i] + swh_stc_north[i] + unresolved_stc_north[i]

    residual_int_north[i]       = advection_int_north[i] + submeso_int_north[i] + neutral_gm_int_north[i]
    eddy_int_north[i]           =                          submeso_int_north[i] + neutral_gm_int_north[i]
    super_residual_int_north[i] = advection_int_north[i] + submeso_int_north[i] + neutral_gm_int_north[i] + isopycnal_mix_int_north[i]
    total_int_north[i]          = advection_int_north[i] + submeso_int_north[i] + neutral_gm_int_north[i] + isopycnal_mix_int_north[i] + diapycnal_mix_int_north[i] + swh_int_north[i]
    unresolved_int_north[i]     = temptend_int_north[i]  - total_int_north[i]
    vdiff_int_north[i]          = diapycnal_mix_int_north[i] + swh_int_north[i] +unresolved_int_north[i]


## note, unadvection is  the former term named remaining
#to note if we do:  super_residual + diapycnal + unadvection = net
#at any case

for i in range(len(filename_south)):

    fn = os.path.join(datadir,filename_south[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    time_south[i]              = file.variables['TIME'][:]/365-2188
    temptend_south[i]          = Decimal(np.mean(file.variables['TEMPTEND_TOT'][61:70])*yt)
    advection_south[i]         = Decimal(np.mean(file.variables['ADVECTION_TOT'][61:70])*yt)
    submeso_south[i]           = Decimal(np.mean(file.variables['SUBMESO_TOT'][61:70])*yt)
    neutral_gm_south[i]        = Decimal(np.mean(file.variables['NEUTRAL_GM_TOT'][61:70])*yt)
    diapycnal_mix_south[i]     = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_TOT'][61:70])*yt)
    isopycnal_mix_south[i]     = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_TOT'][61:70])*yt)
    swh_south[i]               = Decimal(np.mean(file.variables['SWH_TOT'][61:70])*yt)

    temptend_stc_south[i]      = Decimal(np.mean(file.variables['TEMPTEND_STC'][61:70])*yt)
    advection_stc_south[i]     = Decimal(np.mean(file.variables['ADVECTION_STC'][61:70])*yt)
    submeso_stc_south[i]       = Decimal(np.mean(file.variables['SUBMESO_STC'][61:70])*yt)
    neutral_gm_stc_south[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_STC'][61:70])*yt)
    diapycnal_mix_stc_south[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_STC'][61:70])*yt)
    isopycnal_mix_stc_south[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_STC'][61:70])*yt)
    swh_stc_south[i]           = Decimal(np.mean(file.variables['SWH_STC'][61:70])*yt)

    temptend_int_south[i]      = Decimal(np.mean(file.variables['TEMPTEND_INT'][61:70])*yt)
    advection_int_south[i]     = Decimal(np.mean(file.variables['ADVECTION_INT'][61:70])*yt)
    submeso_int_south[i]       = Decimal(np.mean(file.variables['SUBMESO_INT'][61:70])*yt)
    neutral_gm_int_south[i]    = Decimal(np.mean(file.variables['NEUTRAL_GM_INT'][61:70])*yt)
    diapycnal_mix_int_south[i] = Decimal(np.mean(file.variables['VDIFFUSE_DIFF_CBT_INT'][61:70])*yt)
    isopycnal_mix_int_south[i] = Decimal(np.mean(file.variables['NEUTRAL_DIFFUSION_INT'][61:70])*yt)
    swh_int_south[i]           = Decimal(np.mean(file.variables['SWH_INT'][61:70])*yt)

    file.close()

for i in range(len(filename_south)):
    residual_south[i]       = advection_south[i] + submeso_south[i] + neutral_gm_south[i]
    eddy_south[i]           =                      submeso_south[i] + neutral_gm_south[i]
    super_residual_south[i] = advection_south[i] + submeso_south[i] + neutral_gm_south[i] + isopycnal_mix_south[i]
    total_south[i]          = advection_south[i] + submeso_south[i] + neutral_gm_south[i] + isopycnal_mix_south[i] + diapycnal_mix_south[i] + swh_south[i]
    unresolved_south[i]     = temptend_south[i]  - total_south[i]
    vdiff_south[i]          = diapycnal_mix_south[i] + swh_south[i] + unresolved_south[i]

    residual_stc_south[i]       = advection_stc_south[i] + submeso_stc_south[i] + neutral_gm_stc_south[i]
    eddy_stc_south[i]           =                          submeso_stc_south[i] + neutral_gm_stc_south[i]
    super_residual_stc_south[i] = advection_stc_south[i] + submeso_stc_south[i] + neutral_gm_stc_south[i] + isopycnal_mix_stc_south[i]
    total_stc_south[i]          = advection_stc_south[i] + submeso_stc_south[i] + neutral_gm_stc_south[i] + isopycnal_mix_stc_south[i] + diapycnal_mix_stc_south[i] + swh_stc_south[i]
    unresolved_stc_south[i]     = temptend_stc_south[i]  - total_stc_south[i]
    vdiff_stc_south[i]          = diapycnal_mix_stc_south[i] + swh_stc_south[i] + unresolved_stc_south[i]

    residual_int_south[i]       = advection_int_south[i] + submeso_int_south[i] + neutral_gm_int_south[i]
    eddy_int_south[i]           =                          submeso_int_south[i] + neutral_gm_int_south[i]
    super_residual_int_south[i] = advection_int_south[i] + submeso_int_south[i] + neutral_gm_int_south[i] + isopycnal_mix_int_south[i]
    total_int_south[i]          = advection_int_south[i] + submeso_int_south[i] + neutral_gm_int_south[i] + isopycnal_mix_int_south[i] + diapycnal_mix_int_south[i] + swh_int_south[i]
    unresolved_int_south[i]     = temptend_int_south[i]  - total_int_south[i]
    vdiff_int_south[i]          = diapycnal_mix_int_south[i] + swh_int_south[i] + unresolved_int_south[i]


rc('text', usetex=True)

print("& exp & NET &ADV & EDDY & ISO & DIA & SWH & UNRES & R-ADV & SR-ADV & VDIFF ")
for i in range(len(exp)):
    print("%s " %exp[i])
    print("\centering $STC_N$" + " & %.1f " %temptend_stc_north[i] + " & %.1f " %advection_stc_north[i] + " & %.1f " %eddy_stc_north[i] + " & %.1f " %isopycnal_mix_stc_north[i] + " & %.1f " %diapycnal_mix_stc_north[i] + " & %.1f " %swh_stc_north[i] + " & %.1f " %unresolved_stc_north[i] + " & %.1f " %residual_stc_north[i] + " & %.1f " %super_residual_stc_north[i] + " & %.1f " %vdiff_stc_north[i])
    print("\centering $INT_N$" + " & %.1f " %temptend_int_north[i] + " & %.1f " %advection_int_north[i] + " & %.1f " %eddy_int_north[i] + " & %.1f " %isopycnal_mix_int_north[i] + " & %.1f " %diapycnal_mix_int_north[i] + " & %.1f " %swh_int_north[i] + " & %.1f " %unresolved_int_north[i] + " & %.1f " %residual_int_north[i] + " & %.1f " %super_residual_int_north[i] + " & %.1f " %vdiff_int_north[i])
    print("\centering $TOT_N$" + " & %.1f " %temptend_north[i] + " & %.1f " %advection_north[i] + " & %.1f " %eddy_north[i] + " & %.1f " %isopycnal_mix_north[i] + " & %.1f " %diapycnal_mix_north[i] + " & %.1f " %swh_north[i] + " & %.1f " %unresolved_north[i] + " & %.1f " %residual_north[i] + " & %.1f " %super_residual_north[i] + " & %.1f " %vdiff_north[i])
    print("\centering $STC_S$" + " & %.1f " %temptend_stc_south[i] + " & %.1f " %advection_stc_south[i] + " & %.1f " %eddy_stc_south[i] + " & %.1f " %isopycnal_mix_stc_south[i] + " & %.1f " %diapycnal_mix_stc_south[i] + " & %.1f " %swh_stc_south[i] + " & %.1f " %unresolved_stc_south[i] + " & %.1f " %residual_stc_south[i] + " & %.1f " %super_residual_stc_south[i] + " & %.1f " %vdiff_stc_south[i])
    print("\centering $INT_S$" + " & %.1f " %temptend_int_south[i] + " & %.1f " %advection_int_south[i] + " & %.1f " %eddy_int_south[i] + " & %.1f " %isopycnal_mix_int_south[i] + " & %.1f " %diapycnal_mix_int_south[i] + " & %.1f " %swh_int_south[i] + " & %.1f " %unresolved_int_south[i] + " & %.1f " %residual_int_south[i] + " & %.1f " %super_residual_int_south[i] + " & %.1f " %vdiff_int_south[i])
    print("\centering $TOT_S$" + " & %.1f " %temptend_south[i] + " & %.1f " %advection_south[i] + " & %.1f " %eddy_south[i] + " & %.1f " %isopycnal_mix_south[i] + " & %.1f " %diapycnal_mix_south[i] + " & %.1f " %swh_south[i] + " & %.1f " %unresolved_south[i] + " & %.1f " %residual_south[i] + " & %.1f " %super_residual_south[i] + " & %.1f " %vdiff_south[i])

print('-----------------------------------')
print('TRANSIENT CHANGE TABLES (ie. after control substraction)')
print('-----------------------------------')

print("& exp & NET &ADV & EDDY & ISO & DIA & SWH & UNRES & R-ADV & SR-ADV & VDIFF ")
for i in range(len(exp)-1):
    print("%s " %exp[i])
    print("\centering $STC_N$" + " & %.1f " %(temptend_stc_north[i]-temptend_stc_north[-1]) + " & %.1f " %(advection_stc_north[i]-advection_stc_north[-1]) + " & %.1f " %(eddy_stc_north[i]-eddy_stc_north[-1])  + " & %.1f " %(isopycnal_mix_stc_north[i]-isopycnal_mix_stc_north[-1]) + " & %.1f " %(diapycnal_mix_stc_north[i]-diapycnal_mix_stc_north[-1]) + " & %.1f " %(swh_stc_north[i]-swh_stc_north[-1]) + " & %.1f " %(unresolved_stc_north[i]-unresolved_stc_north[-1]) + " & %.1f " %(residual_stc_north[i]-residual_stc_north[-1]) + " & %.1f " %(super_residual_stc_north[i]-super_residual_stc_north[-1]) + " & %.1f " %(vdiff_stc_north[i]-vdiff_stc_north[-1]))
    print("\centering $INT_N$" + " & %.1f " %(temptend_int_north[i]-temptend_int_north[-1]) + " & %.1f " %(advection_int_north[i]-advection_int_north[-1]) + " & %.1f " %(eddy_int_north[i]-eddy_int_north[-1])  + " & %.1f " %(isopycnal_mix_int_north[i]-isopycnal_mix_int_north[-1]) + " & %.1f " %(diapycnal_mix_int_north[i]-diapycnal_mix_int_north[-1]) + " & %.1f " %(swh_int_north[i]-swh_int_north[-1]) + " & %.1f " %(unresolved_int_north[i]-unresolved_int_north[-1]) + " & %.1f " %(residual_int_north[i]-residual_int_north[-1]) + " & %.1f " %(super_residual_int_north[i]-super_residual_int_north[-1]) + " & %.1f " %(vdiff_int_north[i]-vdiff_int_north[-1]))
    print("\centering $TOT_N$" + " & %.1f " %(temptend_north[i]-temptend_north[-1]) + " & %.1f " %(advection_north[i]-advection_north[-1]) + " & %.1f " %(eddy_north[i]-eddy_north[-1]) + " & %.1f " %(isopycnal_mix_north[i]-isopycnal_mix_north[-1]) + " & %.1f " %(diapycnal_mix_north[i]-diapycnal_mix_north[-1]) + " & %.1f " %(swh_north[i]-swh_north[-1]) + " & %.1f " %(unresolved_north[i]-unresolved_north[-1]) + " & %.1f " %(residual_north[i]-residual_north[-1]) + " & %.1f " %(super_residual_north[i]-super_residual_north[-1]) + " & %.1f " %(vdiff_north[i]-vdiff_north[-1]))
    print("\centering $STC_S$" + " & %.1f " %(temptend_stc_south[i]-temptend_stc_south[-1]) + " & %.1f " %(advection_stc_south[i]-advection_stc_south[-1]) + " & %.1f " %(eddy_stc_south[i]-eddy_stc_south[-1])  + " & %.1f " %(isopycnal_mix_stc_south[i]-isopycnal_mix_stc_south[-1]) + " & %.1f " %(diapycnal_mix_stc_south[i]-diapycnal_mix_stc_south[-1]) + " & %.1f " %(swh_stc_south[i]-swh_stc_south[-1]) + " & %.1f " %(unresolved_stc_south[i]-unresolved_stc_south[-1]) + " & %.1f " %(residual_stc_south[i]-residual_stc_south[-1]) + " & %.1f " %(super_residual_stc_south[i]-super_residual_stc_south[-1]) + " & %.1f " %(vdiff_stc_south[i]-vdiff_stc_south[-1]))
    print("\centering $INT_S$" + " & %.1f " %(temptend_int_south[i]-temptend_int_south[-1]) + " & %.1f " %(advection_int_south[i]-advection_int_south[-1]) + " & %.1f " %(eddy_int_south[i]-eddy_int_south[-1])  + " & %.1f " %(isopycnal_mix_int_south[i]-isopycnal_mix_int_south[-1]) + " & %.1f " %(diapycnal_mix_int_south[i]-diapycnal_mix_int_south[-1]) + " & %.1f " %(swh_int_south[i]-swh_int_south[-1]) + " & %.1f " %(unresolved_int_south[i]-unresolved_int_south[-1]) + " & %.1f " %(residual_int_south[i]-residual_int_south[-1]) + " & %.1f " %(super_residual_int_south[i]-super_residual_int_south[-1]) + " & %.1f " %(vdiff_int_south[i]-vdiff_int_south[-1]))
    print("\centering $TOT_S$" + " & %.1f " %(temptend_south[i]-temptend_south[-1]) + " & %.1f " %(advection_south[i]-advection_south[-1]) + " & %.1f " %(eddy_south[i]-eddy_south[-1]) + " & %.1f " %(isopycnal_mix_south[i]-isopycnal_mix_south[-1]) + " & %.1f " %(diapycnal_mix_south[i]-diapycnal_mix_south[-1]) + " & %.1f " %(swh_south[i]-swh_south[-1]) + " & %.1f " %(unresolved_south[i]-unresolved_south[-1]) + " & %.1f " %(residual_south[i]-residual_south[-1]) + " & %.1f " %(super_residual_south[i]-super_residual_south[-1]) + " & %.1f " %(vdiff_south[i]-vdiff_south[-1]))


