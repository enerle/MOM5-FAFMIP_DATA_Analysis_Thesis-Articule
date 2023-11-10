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
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp      = ["Stress","Water","Heat","All","flux-only"]
filename = ['MOC_RHO_PAC_FAFSTRESS.nc','MOC_RHO_PAC_FAFWATER.nc','MOC_RHO_PAC_FAFHEAT.nc','MOC_RHO_PAC_FAFALL.nc','MOC_RHO_PAC_flux-only.nc']

trans_upp1_int_north = [None]*len(filename)
trans_upp2_int_north = [None]*len(filename)
trans_upp3_int_north = [None]*len(filename)
trans_itm1_int_north = [None]*len(filename)
trans_itm2_int_north = [None]*len(filename)
trans_itm3_int_north = [None]*len(filename)
trans_dpp1_int_north = [None]*len(filename)
trans_dpp2_int_north = [None]*len(filename)
trans_dpp3_int_north = [None]*len(filename)
trans_btt1_int_north = [None]*len(filename)
trans_vsum_int_north = [None]*len(filename)

trans_upp1_wbc_north = [None]*len(filename)
trans_upp2_wbc_north = [None]*len(filename)
trans_upp3_wbc_north = [None]*len(filename)
trans_itm1_wbc_north = [None]*len(filename)
trans_itm2_wbc_north = [None]*len(filename)
trans_itm3_wbc_north = [None]*len(filename)
trans_dpp1_wbc_north = [None]*len(filename)
trans_dpp2_wbc_north = [None]*len(filename)
trans_dpp3_wbc_north = [None]*len(filename)
trans_btt1_wbc_north = [None]*len(filename)
trans_vsum_wbc_north = [None]*len(filename)

trans_upp1_int_south = [None]*len(filename)
trans_upp2_int_south = [None]*len(filename)
trans_upp3_int_south = [None]*len(filename)
trans_itm1_int_south = [None]*len(filename)
trans_itm2_int_south = [None]*len(filename)
trans_itm3_int_south = [None]*len(filename)
trans_dpp1_int_south = [None]*len(filename)
trans_dpp2_int_south = [None]*len(filename)
trans_dpp3_int_south = [None]*len(filename)
trans_btt1_int_south = [None]*len(filename)
trans_vsum_int_south = [None]*len(filename)

trans_upp1_wbc_south = [None]*len(filename)
trans_upp2_wbc_south = [None]*len(filename)
trans_upp3_wbc_south = [None]*len(filename)
trans_itm1_wbc_south = [None]*len(filename)
trans_itm2_wbc_south = [None]*len(filename)
trans_itm3_wbc_south = [None]*len(filename)
trans_dpp1_wbc_south = [None]*len(filename)
trans_dpp2_wbc_south = [None]*len(filename)
trans_dpp3_wbc_south = [None]*len(filename)
trans_btt1_wbc_south = [None]*len(filename)
trans_vsum_wbc_south = [None]*len(filename)

#----
stc_net_trans_north     = [None]*len(filename)
stc_net_trans_north_v2  = [None]*len(filename)
stc_net_trans_north_v3  = [None]*len(filename)
stc_wbc_trans_north     = [None]*len(filename)
stc_wbc_trans_north_res = [None]*len(filename)
stc_int_trans_north     = [None]*len(filename)
stc_ekm_trans_north     = [None]*len(filename)
stc_imb_trans_north     = [None]*len(filename)

ekman_trans_north_v1  = [None]*len(filename)
ekman_trans_north     = [None]*len(filename)
upper_trans_north     = [None]*len(filename)
deep1_trans_north     = [None]*len(filename)
deep2_trans_north     = [None]*len(filename)
deep3_trans_north     = [None]*len(filename)
bottom_trans_north    = [None]*len(filename)
total_trans_north     = [None]*len(filename)

#----
stc_net_trans_south     = [None]*len(filename)
stc_net_trans_south_v2  = [None]*len(filename)
stc_net_trans_south_v3  = [None]*len(filename)
stc_wbc_trans_south     = [None]*len(filename)
stc_wbc_trans_south_res = [None]*len(filename)
stc_int_trans_south     = [None]*len(filename)
stc_ekm_trans_south     = [None]*len(filename)
stc_imb_trans_south     = [None]*len(filename)

ekman_trans_south_v1  = [None]*len(filename)
ekman_trans_south     = [None]*len(filename)
upper_trans_south     = [None]*len(filename)
deep1_trans_south     = [None]*len(filename)
deep2_trans_south     = [None]*len(filename)
deep3_trans_south     = [None]*len(filename)
bottom_trans_south    = [None]*len(filename)
total_trans_south     = [None]*len(filename)


yt = 1e-9 #GW

#---> 
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
##NORTHERN HEMISPHERE
    trans_upp1_int_north[i] =file.variables['TRANS0000_INT_NORTH'][:]
    trans_upp2_int_north[i] =file.variables['TRANS0100_INT_NORTH'][:]
    trans_upp3_int_north[i] =file.variables['TRANS0201_INT_NORTH'][:]
    trans_itm1_int_north[i] =file.variables['TRANS0302_INT_NORTH'][:]
    trans_itm2_int_north[i] =file.variables['TRANS0403_INT_NORTH'][:]
    trans_itm3_int_north[i] =file.variables['TRANS0504_INT_NORTH'][:]
    trans_dpp1_int_north[i] =file.variables['TRANS0605_INT_NORTH'][:]
    trans_dpp2_int_north[i] =file.variables['TRANS0706_INT_NORTH'][:]
    trans_dpp3_int_north[i] =file.variables['TRANS0807_INT_NORTH'][:]
    trans_btt1_int_north[i] =file.variables['TRANS0908_INT_NORTH'][:]
    trans_vsum_int_north[i] =file.variables['TRANS0009_INT_NORTH'][:]

    trans_upp1_wbc_north[i] =file.variables['TRANS0000_WBC_NORTH'][:]
    trans_upp2_wbc_north[i] =file.variables['TRANS0100_WBC_NORTH'][:]
    trans_upp3_wbc_north[i] =file.variables['TRANS0201_WBC_NORTH'][:]
    trans_itm1_wbc_north[i] =file.variables['TRANS0302_WBC_NORTH'][:]
    trans_itm2_wbc_north[i] =file.variables['TRANS0403_WBC_NORTH'][:]
    trans_itm3_wbc_north[i] =file.variables['TRANS0504_WBC_NORTH'][:]
    trans_dpp1_wbc_north[i] =file.variables['TRANS0605_WBC_NORTH'][:]
    trans_dpp2_wbc_north[i] =file.variables['TRANS0706_WBC_NORTH'][:]
    trans_dpp3_wbc_north[i] =file.variables['TRANS0807_WBC_NORTH'][:]
    trans_btt1_wbc_north[i] =file.variables['TRANS0908_WBC_NORTH'][:]
    trans_vsum_wbc_north[i] =file.variables['TRANS0009_WBC_NORTH'][:]

##SOUTHERN HEMISPHERE
    trans_upp1_int_south[i] =file.variables['TRANS0000_INT_SOUTH'][:]
    trans_upp2_int_south[i] =file.variables['TRANS0100_INT_SOUTH'][:]
    trans_upp3_int_south[i] =file.variables['TRANS0201_INT_SOUTH'][:]
    trans_itm1_int_south[i] =file.variables['TRANS0302_INT_SOUTH'][:]
    trans_itm2_int_south[i] =file.variables['TRANS0403_INT_SOUTH'][:]
    trans_itm3_int_south[i] =file.variables['TRANS0504_INT_SOUTH'][:]
    trans_dpp1_int_south[i] =file.variables['TRANS0605_INT_SOUTH'][:]
    trans_dpp2_int_south[i] =file.variables['TRANS0706_INT_SOUTH'][:]
    trans_dpp3_int_south[i] =file.variables['TRANS0807_INT_SOUTH'][:]
    trans_btt1_int_south[i] =file.variables['TRANS0908_INT_SOUTH'][:]
    trans_vsum_int_south[i] =file.variables['TRANS0009_INT_SOUTH'][:]

    trans_upp1_wbc_south[i] =file.variables['TRANS0000_WBC_SOUTH'][:]
    trans_upp2_wbc_south[i] =file.variables['TRANS0100_WBC_SOUTH'][:]
    trans_upp3_wbc_south[i] =file.variables['TRANS0201_WBC_SOUTH'][:]
    trans_itm1_wbc_south[i] =file.variables['TRANS0302_WBC_SOUTH'][:]
    trans_itm2_wbc_south[i] =file.variables['TRANS0403_WBC_SOUTH'][:]
    trans_itm3_wbc_south[i] =file.variables['TRANS0504_WBC_SOUTH'][:]
    trans_dpp1_wbc_south[i] =file.variables['TRANS0605_WBC_SOUTH'][:]
    trans_dpp2_wbc_south[i] =file.variables['TRANS0706_WBC_SOUTH'][:]
    trans_dpp3_wbc_south[i] =file.variables['TRANS0807_WBC_SOUTH'][:]
    trans_btt1_wbc_south[i] =file.variables['TRANS0908_WBC_SOUTH'][:]
    trans_vsum_wbc_south[i] =file.variables['TRANS0009_WBC_SOUTH'][:]

    file.close()

for i in range(len(exp)):
#integrado dentro de la celda subtropical (contribucion wbc e interior)
    stc_int_trans_north[i]     = trans_upp2_int_north[i] + trans_upp3_int_north[i] + trans_itm1_int_north[i] + trans_itm2_int_north[i] + trans_itm3_int_north[i]
    stc_wbc_trans_north[i]     = trans_upp2_wbc_north[i] + trans_upp3_wbc_north[i] + trans_itm1_wbc_north[i]
    stc_wbc_trans_north_res[i] = trans_itm2_wbc_north[i] + trans_itm3_wbc_north[i]
    stc_ekm_trans_north[i]     = trans_upp1_wbc_north[i] + trans_upp1_int_north[i]

##Correction for surface cell mass imbalance:
##Here we considere the net trans imbalance of the column is given by the cell alone implying any
##imbalace take place either in the WBC contribution or the interior one (the last based on the sign of the anomaly)
##MODIFIED (22sep22): imbalace justed to be considered to happen in the surface, now is in the WBC flow
    stc_net_trans_north[i] = trans_vsum_wbc_north[i] + trans_vsum_int_north[i] #total vertical sum
    if stc_net_trans_north[i] > 0.:
        stc_wbc_trans_north[i] = stc_wbc_trans_north[i] - stc_net_trans_north[i]
        stc_int_trans_north[i] = stc_int_trans_north[i]
    elif stc_net_trans_north[i] < 0.:
        stc_wbc_trans_north[i] = stc_wbc_trans_north[i]
        stc_int_trans_north[i] = stc_int_trans_north[i] - stc_net_trans_north[i]

##!!residual mass transport by cell (deep water mass production) assesment of non-recirculating water within the cell 
##(northward flow not including for ekman compensation). To note we use the surface as our reference flow (for calibrating the other flows). 
##to note, imbalances are tackle  only through compensations of the flow insider the wbc
##since we considerer it as the main dynamic structure available and responsable for any recirculation
    stc_imb_trans_north[i] = stc_ekm_trans_north[i] + stc_wbc_trans_north[i] + stc_int_trans_north[i] #in balance should be zero
    if stc_imb_trans_north[i] > 0.:
        stc_wbc_trans_north[i]     = stc_wbc_trans_north[i]     - stc_imb_trans_north[i]
        stc_wbc_trans_north_res[i] = stc_wbc_trans_north_res[i] + stc_imb_trans_north[i]
    elif stc_imb_trans_north[i] < 0.:
        stc_wbc_trans_north[i]     = stc_wbc_trans_north[i]     + stc_imb_trans_north[i]
        stc_wbc_trans_north_res[i] = stc_wbc_trans_north_res[i] - stc_imb_trans_north[i]

#imbalance secundario de la celda (dado que under water no esta en balance)
#(y aun no entiendo porque el imbalance persite (razon fisica o numerica?)
    stc_net_trans_north_v2[i] = stc_ekm_trans_north[i]  + stc_wbc_trans_north[i]  + stc_int_trans_north[i]
    if stc_net_trans_north_v2[i] > 0.:
        stc_wbc_trans_north[i] = stc_wbc_trans_north[i]-stc_net_trans_north_v2[i]
        stc_wbc_trans_north_res[i] = stc_wbc_trans_north_res[i] + stc_net_trans_north_v2[i]
    else:
        stc_int_trans_north[i] = stc_int_trans_north[i]-stc_net_trans_north_v2[i]
        stc_wbc_trans_north_res[i] = stc_wbc_trans_north_res[i] + stc_net_trans_north_v2[i]
    stc_net_trans_north_v3[i] = stc_ekm_trans_north[i]  + stc_wbc_trans_north[i]  + stc_int_trans_north[i]

#integrado en toda la columna (total=wbc+int)
    ekman_trans_north[i]  = stc_ekm_trans_north[i]
    upper_trans_north[i]  = stc_wbc_trans_north[i]  + stc_wbc_trans_north_res[i] + stc_int_trans_north[i] 
    deep1_trans_north[i]  = trans_dpp1_wbc_north[i] + trans_dpp1_int_north[i] 
    deep2_trans_north[i]  = trans_dpp2_wbc_north[i] + trans_dpp2_int_north[i]
    deep3_trans_north[i]  = trans_dpp3_wbc_north[i] + trans_dpp3_int_north[i]
    bottom_trans_north[i] = trans_btt1_wbc_north[i] + trans_btt1_int_north[i]
    total_trans_north[i]  = ekman_trans_north[i] + upper_trans_north[i] + deep1_trans_north[i] + deep2_trans_north[i] + deep3_trans_north[i] + bottom_trans_north[i]

##-----------------------
##----SOUTHERN HEMISPHERE
##-----------------------
#integrado dentro de la celda subtropical (contribucion wbc e interior)
    stc_int_trans_south[i]     = trans_upp2_int_south[i] + trans_upp3_int_south[i] + trans_itm1_int_south[i] + trans_itm2_int_south[i] + trans_itm3_int_south[i]
    stc_wbc_trans_south[i]     = trans_upp2_wbc_south[i] + trans_upp3_wbc_south[i] + trans_itm1_wbc_south[i]
    stc_wbc_trans_south_res[i] = trans_itm2_wbc_south[i] + trans_itm3_wbc_south[i]
    stc_ekm_trans_south[i]     = trans_upp1_wbc_south[i] + trans_upp1_int_south[i]

#correction for surface cell mass imbalance
    stc_net_trans_south[i] = trans_vsum_wbc_south[i] + trans_vsum_int_south[i] #total vertical sum
    if stc_net_trans_south[i] > 0.:
        stc_wbc_trans_south[i] = stc_wbc_trans_south[i] 
        stc_int_trans_south[i] = stc_int_trans_south[i] - stc_net_trans_south[i]
    elif stc_net_trans_south[i] < 0.:
        stc_wbc_trans_south[i] = stc_wbc_trans_south[i] - stc_net_trans_south[i]
        stc_int_trans_south[i] = stc_int_trans_south[i] 

#residual mass transport by cell (deep water mass production)
    stc_imb_trans_south[i] = stc_ekm_trans_south[i] + stc_wbc_trans_south[i] + stc_int_trans_south[i] #in balance should be zero
    if stc_imb_trans_south[i] > 0.:
        stc_wbc_trans_south[i]     = stc_wbc_trans_south[i]     + stc_imb_trans_south[i]
        stc_wbc_trans_south_res[i] = stc_wbc_trans_south_res[i] - stc_imb_trans_south[i]
    elif stc_imb_trans_south[i] < 0.:
        stc_wbc_trans_south[i]     = stc_wbc_trans_south[i]     - stc_imb_trans_south[i]
        stc_wbc_trans_south_res[i] = stc_wbc_trans_south_res[i] + stc_imb_trans_south[i]

#imbalance secundario de la celda
    stc_net_trans_south_v2[i] = stc_ekm_trans_south[i]  + stc_wbc_trans_south[i]  + stc_int_trans_south[i]
    if stc_net_trans_south_v2[i] > 0.:
        stc_wbc_trans_south[i] = stc_wbc_trans_south[i]-stc_net_trans_south_v2[i]
        stc_wbc_trans_south_res[i] = stc_wbc_trans_south_res[i] + stc_net_trans_south_v2[i]
    else:
        stc_int_trans_south[i] = stc_int_trans_south[i]-stc_net_trans_south_v2[i]
        stc_wbc_trans_south_res[i] = stc_wbc_trans_south_res[i] + stc_net_trans_south_v2[i]
    stc_net_trans_south_v3[i] = stc_ekm_trans_south[i]  + stc_wbc_trans_south[i]  + stc_int_trans_south[i]

#integrado en toda la columna (total=wbc+int)
    ekman_trans_south[i]  = stc_ekm_trans_south[i]
    upper_trans_south[i]  = stc_wbc_trans_south[i]  + stc_wbc_trans_south_res[i] + stc_int_trans_south[i]
    deep1_trans_south[i]  = trans_dpp1_wbc_south[i] + trans_dpp1_int_south[i]
    deep2_trans_south[i]  = trans_dpp2_wbc_south[i] + trans_dpp2_int_south[i]
    deep3_trans_south[i]  = trans_dpp3_wbc_south[i] + trans_dpp3_int_south[i]
    bottom_trans_south[i] = trans_btt1_wbc_south[i] + trans_btt1_int_south[i]
    total_trans_south[i]  = ekman_trans_south[i] + upper_trans_south[i] + deep1_trans_south[i] + deep2_trans_south[i] + deep3_trans_south[i] + bottom_trans_south[i]

#####################
#####################

profile = [None]*len(filename)
profile_anom = [None]*len(filename)
profile_south = [None]*len(filename)
profile_south_anom = [None]*len(filename)

for i in range(len(filename)):
    profile[i] = [float(ekman_trans_north[i]),float(upper_trans_north[i]),float(deep1_trans_north[i]),float(deep2_trans_north[i]),float(deep3_trans_north[i]),float(bottom_trans_north[i])]

for i in range(len(filename)-1):
    profile_anom[i] =  [float(ekman_trans_north[i]-ekman_trans_north[-1]),float(upper_trans_north[i]-upper_trans_north[-1]),float(deep1_trans_north[i]-deep1_trans_north[-1]),float(deep2_trans_north[i]-deep2_trans_north[-1]),float(deep3_trans_north[i]-deep3_trans_north[-1]),float(bottom_trans_north[i]-bottom_trans_north[-1])]

for i in range(len(filename)):
    profile_south[i] = [float(ekman_trans_south[i]),float(upper_trans_south[i]),float(deep1_trans_south[i]),float(deep2_trans_south[i]),float(deep3_trans_south[i]),float(bottom_trans_south[i])]

for i in range(len(filename)-1):
    profile_south_anom[i] =  [float(ekman_trans_south[i]-ekman_trans_south[-1]),float(upper_trans_south[i]-upper_trans_south[-1]),float(deep1_trans_south[i]-deep1_trans_south[-1]),float(deep2_trans_south[i]-deep2_trans_south[-1]),float(deep3_trans_south[i]-deep3_trans_south[-1]),float(bottom_trans_south[i]-bottom_trans_south[-1])]

#####################
##figures
#####################
#
#rc('figure', figsize=(6.4,4.8)) #default
#rc('figure', figsize=(8.27,11.69))
#rc('figure', figsize=(11.69,8.27))
rc('figure',figsize=(6.4,7.2))

vnames = ['Surface','Upper','Interm.','Deep','Deep 2','Bottom']
v = [-17,17,-.5,5.5]

for i in range(len(exp)):

    fig = plt.figure(100+i)
    fig.subplots_adjust(wspace=0.3)

    ax = fig.add_subplot(2,2,1)###
    barh(list(vnames),profile_south[i],height=[.8,.8,.8,.8,.8,.8],left=None,align='center',color=[.85,.85,.85],edgecolor='black')

    plt.axvline(x=0.,color='k',linestyle='-',linewidth=2.0)
    plt.axhline(y=0.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=1.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=2.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=3.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=4.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=5.5,color='k',linestyle=':',linewidth=1)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(0); ax.spines['right'].set_linewidth(0)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=0)

#ax.set_xlabel("$[Sv]$",fontsize=16)
#plt.title('South',fontsize=16)
    plt.xticks([-16,-12,-8,-4,0,4,8,12,16],[-16,-12,-8,-4,0,4,8,12,16],fontsize=8)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    ax = fig.add_subplot(2,2,2)###
    barh(list(vnames),profile[i],height=[.8,.8,.8,.8,.8,.8],left=None,align='center',color=[.85,.85,.85],edgecolor='black')

    plt.axvline(x=0.,color='k',linestyle='-',linewidth=2.0)
    plt.axhline(y=0.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=1.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=2.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=3.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=4.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=5.5,color='k',linestyle=':',linewidth=1)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(0); ax.spines['right'].set_linewidth(0)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=0)

#ax.set_xlabel("$[Sv]$",fontsize=16)
#plt.title('North',fontsize=16)
    plt.yticks([0,1,2,3,4,5,6],[],fontsize=11)
    plt.xticks([-16,-12,-8,-4,0,4,8,12,16],[-16,-12,-8,-4,0,4,8,12,16],fontsize=8)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    plt.savefig('mass_flux_stc_' + exp[i] + '_total.png',transparent = False,bbox_inches='tight',dpi=300)

###########
###Anomalias
v = [-4.5,4.5,-.5,5.5]

for i in range(len(exp)-1):

    fig = plt.figure(i)
    fig.subplots_adjust(wspace=0.3)

    ax = fig.add_subplot(2,2,1)###
    barh(list(vnames),profile_south_anom[i],height=[.8,.8,.8,.8,.8,.8],left=None,align='center',color=[.85,.85,.85],edgecolor='black')

    plt.axvline(x=0.,color='k',linestyle='-',linewidth=2.0)
    plt.axhline(y=0.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=1.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=2.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=3.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=4.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=5.5,color='k',linestyle=':',linewidth=1)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(0); ax.spines['right'].set_linewidth(0)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=0)

#    ax.set_xlabel("$[Sv]$",fontsize=16)
#    plt.title('South',fontsize=16)
    plt.xticks([-4,-3,-2,-1,0,1,2,3,4],[-4,-3,-2,-1,0,1,2,3,4],fontsize=10)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    ax = fig.add_subplot(2,2,2)###
    barh(list(vnames),profile_anom[i],height=[.8,.8,.8,.8,.8,.8],left=None,align='center',color=[.85,.85,.85],edgecolor='black')

    plt.axvline(x=0.,color='k',linestyle='-',linewidth=2.0)
    plt.axhline(y=0.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=1.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=2.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=3.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=4.5,color='k',linestyle=':',linewidth=1)
    plt.axhline(y=5.5,color='k',linestyle=':',linewidth=1)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(0); ax.spines['right'].set_linewidth(0)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=0)

#    ax.set_xlabel("$[Sv]$",fontsize=16)
#    plt.title('North',fontsize=16)
    plt.yticks([0,1,2,3,4,5,6],[],fontsize=11)
    plt.xticks([-4,-3,-2,-1,0,1,2,3,4],[-4,-3,-2,-1,0,1,2,3,4],fontsize=10)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    plt.savefig('mass_flux_stc_' + exp[i] + '.png',transparent = False,bbox_inches='tight',dpi=300)

#plt.show()

####################
##tables
####################

rc('text', usetex=True)
print("=================NORTHERN HEMISPHERE")
print("& Level $ Stress $ Water $ Heat $ All $control")
print("\centering \emph{Surface} "  + " & %.2f " %ekman_trans_north[0]       + " & %.2f " %ekman_trans_north[1]       + " & %.2f " %ekman_trans_north[2]       + " & %.2f " %ekman_trans_north[3]       + " & %.2f " %ekman_trans_north[4])
print("\centering \emph{WBC}"       + " & %.2f " %stc_wbc_trans_north[0]     + " & %.2f " %stc_wbc_trans_north[1]     + " & %.2f " %stc_wbc_trans_north[2]     + " & %.2f " %stc_wbc_trans_north[3]     + " & %.2f " %stc_wbc_trans_north[4])
print("\centering \emph{Interior}"  + " & %.2f " %stc_int_trans_north[0]     + " & %.2f " %stc_int_trans_north[1]     + " & %.2f " %stc_int_trans_north[2]     + " & %.2f " %stc_int_trans_north[3]     + " & %.2f " %stc_int_trans_north[4])
print("\centering \emph{Residual}"  + " & %.2f " %stc_wbc_trans_north_res[0] + " & %.2f " %stc_wbc_trans_north_res[1] + " & %.2f " %stc_wbc_trans_north_res[2] + " & %.2f " %stc_wbc_trans_north_res[3] + " & %.2f " %stc_wbc_trans_north_res[4])
print("--------------------------")
print("\centering \emph{Surface}"   +  " & %.2f " %ekman_trans_north[0] + " & %.2f " %ekman_trans_north[1]  + " & %.2f " %ekman_trans_north[2]  + " & %.2f " %ekman_trans_north[3]  +  " & %.2f " %ekman_trans_north[4])
print("\centering \emph{Upper}"     +  " & %.2f " %upper_trans_north[0] + " & %.2f " %upper_trans_north[1]  + " & %.2f " %upper_trans_north[2]  + " & %.2f " %upper_trans_north[3]  + " & %.2f " %upper_trans_north[4])
print("\centering \emph{Intermd.}"    + " & %.2f " %deep1_trans_north[0]  + " & %.2f " %deep1_trans_north[1]  + " & %.2f " %deep1_trans_north[2]  + " & %.2f " %deep1_trans_north[3]  + " & %.2f " %deep1_trans_north[4])
print("\centering \emph{Deep 1}"    + " & %.2f " %deep2_trans_north[0]  + " & %.2f " %deep2_trans_north[1]  + " & %.2f " %deep2_trans_north[2]  + " & %.2f " %deep2_trans_north[3]  + " & %.2f " %deep2_trans_north[4])
print("\centering \emph{Deep 2}"    + " & %.2f " %deep3_trans_north[0]  + " & %.2f " %deep3_trans_north[1]  + " & %.2f " %deep3_trans_north[2]  + " & %.2f " %deep3_trans_north[3]  + " & %.2f " %deep3_trans_north[4])
print("\centering \emph{Bottom}"    + " & %.2f " %bottom_trans_north[0] + " & %.2f " %bottom_trans_north[1] + " & %.2f " %bottom_trans_north[2] + " & %.2f " %bottom_trans_north[3] + " & %.2f " %bottom_trans_north[4])
print("\centering \emph{Net Trans.}" + " & %.2f " %stc_net_trans_north[0]     + " & %.2f " %stc_net_trans_north[1]     + " & %.2f " %stc_net_trans_north[2]     + " & %.2f " %stc_net_trans_north[3]     + " & %.2f " %stc_net_trans_north[4])

print("=================NORTHERN HEMISPHERE (anomalies)")
print("& Level $ Stress $ Water $ Heart $ All $ control")
print("\centering \emph{Surface} " +  " & %.2f " %(ekman_trans_north[0]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[1]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[2]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[3]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[4]-ekman_trans_north[-1]))
print("\centering \emph{WBC}"      + " & %.2f " %(stc_wbc_trans_north[0]-stc_wbc_trans_north[-1]) + " & %.2f " %(stc_wbc_trans_north[1]-stc_wbc_trans_north[-1])  + " & %.2f " %(stc_wbc_trans_north[2]-stc_wbc_trans_north[-1])  + " & %.2f " %(stc_wbc_trans_north[3]-stc_wbc_trans_north[-1]) + " & %.2f " %(stc_wbc_trans_north[4]-stc_wbc_trans_north[-1]))
print("\centering \emph{Interior}" + " & %.2f " %(stc_int_trans_north[0]-stc_int_trans_north[-1]) + " & %.2f " %(stc_int_trans_north[1]-stc_int_trans_north[-1]) + " & %.2f " %(stc_int_trans_north[2]-stc_int_trans_north[-1]) + " & %.2f " %(stc_int_trans_north[3]-stc_int_trans_north[-1]) + " & %.2f " %(stc_int_trans_north[4]-stc_int_trans_north[-1]))
print("\centering \emph{Residual}" + " & %.2f " %(stc_wbc_trans_north_res[0]-stc_wbc_trans_north_res[-1]) + " & %.2f " %(stc_wbc_trans_north_res[1]-stc_wbc_trans_north_res[-1]) + " & %.2f " %(stc_wbc_trans_north_res[2]-stc_wbc_trans_north_res[-1]) + " & %.2f " %(stc_wbc_trans_north_res[3]-stc_wbc_trans_north_res[-1]) + " & %.2f " %(stc_wbc_trans_north_res[4]-stc_wbc_trans_north_res[-1]))
print("--------------------------")
print("\centering \emph{Surface} " +  " & %.2f " %(ekman_trans_north[0]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[1]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[2]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[3]-ekman_trans_north[-1]) + " & %.2f " %(ekman_trans_north[4]-ekman_trans_north[-1]))
print("\centering \emph{Upper}" +  " & %.2f " %(upper_trans_north[0]-upper_trans_north[-1]) + " & %.2f " %(upper_trans_north[1]-upper_trans_north[-1]) + " & %.2f " %(upper_trans_north[2]-upper_trans_north[-1]) + " & %.2f " %(upper_trans_north[3]-upper_trans_north[-1]) + " & %.2f " %(upper_trans_north[4]-upper_trans_north[-1]))
print("\centering \emph{Deep 1}" + " & %.2f " %(deep1_trans_north[0]-deep1_trans_north[-1]) + " & %.2f " %(deep1_trans_north[1]-deep1_trans_north[-1]) + " & %.2f " %(deep1_trans_north[2]-deep1_trans_north[-1]) + " & %.2f " %(deep1_trans_north[3]-deep1_trans_north[-1]) + " & %.2f " %(deep1_trans_north[4]-deep1_trans_north[-1]))
print("\centering \emph{Deep 2}" + " & %.2f " %(deep2_trans_north[0]-deep2_trans_north[-1]) + " & %.2f " %(deep2_trans_north[1]-deep2_trans_north[-1]) + " & %.2f " %(deep2_trans_north[2]-deep2_trans_north[-1]) + " & %.2f " %(deep2_trans_north[3]-deep2_trans_north[-1]) + " & %.2f " %(deep2_trans_north[4]-deep2_trans_north[-1]))
print("\centering \emph{Deep 3}" + " & %.2f " %(deep3_trans_north[0]-deep3_trans_north[-1]) + " & %.2f " %(deep3_trans_north[1]-deep3_trans_north[-1]) + " & %.2f " %(deep3_trans_north[2]-deep3_trans_north[-1]) + " & %.2f " %(deep3_trans_north[3]-deep3_trans_north[-1]) + " & %.2f " %(deep3_trans_north[4]-deep3_trans_north[-1]))
print("\centering \emph{Bottom}" + " & %.2f " %(bottom_trans_north[0]-bottom_trans_north[-1]) + " & %.2f " %(bottom_trans_north[1]-bottom_trans_north[-1]) + " & %.2f " %(bottom_trans_north[2]-bottom_trans_north[-1]) + " & %.2f " %(bottom_trans_north[3]-bottom_trans_north[-1]) + " & %.2f " %(bottom_trans_north[4]-bottom_trans_north[-1]))
print("\centering \emph{Net Trans.}" + " & %.2f " %(stc_net_trans_north[0]-stc_net_trans_north[-1]) + " & %.2f " %(stc_net_trans_north[1]-stc_net_trans_north[-1]) + " & %.2f " %(stc_net_trans_north[2]-stc_net_trans_north[-1]) + " & %.2f " %(stc_net_trans_north[3]-stc_net_trans_north[-1]) + " & %.2f " %(stc_net_trans_north[4]-stc_net_trans_north[-1]))


print("=================SOUTHERN HEMISPHERE")
print("& Level $ Stress $ Water $ Heat $ All $control")
print("\centering \emph{Surface} "  + " & %.2f " %ekman_trans_south[0]       + " & %.2f " %ekman_trans_south[1]       + " & %.2f " %ekman_trans_south[2]       + " & %.2f " %ekman_trans_south[3]       + " & %.2f " %ekman_trans_south[4])
print("\centering \emph{WBC}"       + " & %.2f " %stc_wbc_trans_south[0]     + " & %.2f " %stc_wbc_trans_south[1]     + " & %.2f " %stc_wbc_trans_south[2]     + " & %.2f " %stc_wbc_trans_south[3]     + " & %.2f " %stc_wbc_trans_south[4])
print("\centering \emph{Interior}"  + " & %.2f " %stc_int_trans_south[0]     + " & %.2f " %stc_int_trans_south[1]     + " & %.2f " %stc_int_trans_south[2]     + " & %.2f " %stc_int_trans_south[3]     + " & %.2f " %stc_int_trans_south[4])
print("\centering \emph{Residual}"  + " & %.2f " %stc_wbc_trans_south_res[0] + " & %.2f " %stc_wbc_trans_south_res[1] + " & %.2f " %stc_wbc_trans_south_res[2] + " & %.2f " %stc_wbc_trans_south_res[3] + " & %.2f " %stc_wbc_trans_south_res[4])
print("--------------------------")
print("\centering \emph{Surface}"   +  " & %.2f " %ekman_trans_south[0] + " & %.2f " %ekman_trans_south[1]  + " & %.2f " %ekman_trans_south[2]  + " & %.2f " %ekman_trans_south[3]  +  " & %.2f " %ekman_trans_south[4])
print("\centering \emph{Upper}"     +  " & %.2f " %upper_trans_south[0] + " & %.2f " %upper_trans_south[1]  + " & %.2f " %upper_trans_south[2]  + " & %.2f " %upper_trans_south[3]  + " & %.2f " %upper_trans_south[4])
print("\centering \emph{Intermd.}"    + " & %.2f " %deep1_trans_south[0]  + " & %.2f " %deep1_trans_south[1]  + " & %.2f " %deep1_trans_south[2]  + " & %.2f " %deep1_trans_south[3]  + " & %.2f " %deep1_trans_south[4])
print("\centering \emph{Deep 1}"    + " & %.2f " %deep2_trans_south[0]  + " & %.2f " %deep2_trans_south[1]  + " & %.2f " %deep2_trans_south[2]  + " & %.2f " %deep2_trans_south[3]  + " & %.2f " %deep2_trans_south[4])
print("\centering \emph{Deep 2}"    + " & %.2f " %deep3_trans_south[0]  + " & %.2f " %deep3_trans_south[1]  + " & %.2f " %deep3_trans_south[2]  + " & %.2f " %deep3_trans_south[3]  + " & %.2f " %deep3_trans_south[4])
print("\centering \emph{Bottom}"    + " & %.2f " %bottom_trans_south[0] + " & %.2f " %bottom_trans_south[1] + " & %.2f " %bottom_trans_south[2] + " & %.2f " %bottom_trans_south[3] + " & %.2f " %bottom_trans_south[4])
print("\centering \emph{Net Trans.}" + " & %.2f " %stc_net_trans_south[0]     + " & %.2f " %stc_net_trans_south[1]     + " & %.2f " %stc_net_trans_south[2]     + " & %.2f " %stc_net_trans_south[3]     + " & %.2f " %stc_net_trans_south[4])

print("=================SOUTHERN HEMISPHERE (anomalies)")
print("& Level $ Stress $Water $ Heart $ All $ control")
print("\centering \emph{Surface} " +  " & %.2f " %(ekman_trans_south[0]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[1]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[2]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[3]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[4]-ekman_trans_south[-1]))
print("\centering \emph{WBC}"      + " & %.2f " %(stc_wbc_trans_south[0]-stc_wbc_trans_south[-1]) + " & %.2f " %(stc_wbc_trans_south[1]-stc_wbc_trans_south[-1])  + " & %.2f " %(stc_wbc_trans_south[2]-stc_wbc_trans_south[-1])  + " & %.2f " %(stc_wbc_trans_south[3]-stc_wbc_trans_south[-1]) + " & %.2f " %(stc_wbc_trans_south[4]-stc_wbc_trans_south[-1]))
print("\centering \emph{Interior}" + " & %.2f " %(stc_int_trans_south[0]-stc_int_trans_south[-1]) + " & %.2f " %(stc_int_trans_south[1]-stc_int_trans_south[-1]) + " & %.2f " %(stc_int_trans_south[2]-stc_int_trans_south[-1]) + " & %.2f " %(stc_int_trans_south[3]-stc_int_trans_south[-1]) + " & %.2f " %(stc_int_trans_south[4]-stc_int_trans_south[-1]))
print("\centering \emph{Residual}" + " & %.2f " %(stc_wbc_trans_south_res[0]-stc_wbc_trans_south_res[-1]) + " & %.2f " %(stc_wbc_trans_south_res[1]-stc_wbc_trans_south_res[-1]) + " & %.2f " %(stc_wbc_trans_south_res[2]-stc_wbc_trans_south_res[-1]) + " & %.2f " %(stc_wbc_trans_south_res[3]-stc_wbc_trans_south_res[-1]) + " & %.2f " %(stc_wbc_trans_south_res[4]-stc_wbc_trans_south_res[-1]))
print("--------------------------")
print("\centering \emph{Surface} " +  " & %.2f " %(ekman_trans_south[0]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[1]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[2]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[3]-ekman_trans_south[-1]) + " & %.2f " %(ekman_trans_south[4]-ekman_trans_south[-1]))
print("\centering \emph{Upper}" +  " & %.2f " %(upper_trans_south[0]-upper_trans_south[-1]) + " & %.2f " %(upper_trans_south[1]-upper_trans_south[-1]) + " & %.2f " %(upper_trans_south[2]-upper_trans_south[-1]) + " & %.2f " %(upper_trans_south[3]-upper_trans_south[-1]) + " & %.2f " %(upper_trans_south[4]-upper_trans_south[-1]))
print("\centering \emph{Deep 1}" + " & %.2f " %(deep1_trans_south[0]-deep1_trans_south[-1]) + " & %.2f " %(deep1_trans_south[1]-deep1_trans_south[-1]) + " & %.2f " %(deep1_trans_south[2]-deep1_trans_south[-1]) + " & %.2f " %(deep1_trans_south[3]-deep1_trans_south[-1]) + " & %.2f " %(deep1_trans_south[4]-deep1_trans_south[-1]))
print("\centering \emph{Deep 2}" + " & %.2f " %(deep2_trans_south[0]-deep2_trans_south[-1]) + " & %.2f " %(deep2_trans_south[1]-deep2_trans_south[-1]) + " & %.2f " %(deep2_trans_south[2]-deep2_trans_south[-1]) + " & %.2f " %(deep2_trans_south[3]-deep2_trans_south[-1]) + " & %.2f " %(deep2_trans_south[4]-deep2_trans_south[-1]))
print("\centering \emph{Deep 3}" + " & %.2f " %(deep3_trans_south[0]-deep3_trans_south[-1]) + " & %.2f " %(deep3_trans_south[1]-deep3_trans_south[-1]) + " & %.2f " %(deep3_trans_south[2]-deep3_trans_south[-1]) + " & %.2f " %(deep3_trans_south[3]-deep3_trans_south[-1]) + " & %.2f " %(deep3_trans_south[4]-deep3_trans_south[-1]))
print("\centering \emph{Bottom}" + " & %.2f " %(bottom_trans_south[0]-bottom_trans_south[-1]) + " & %.2f " %(bottom_trans_south[1]-bottom_trans_south[-1]) + " & %.2f " %(bottom_trans_south[2]-bottom_trans_south[-1]) + " & %.2f " %(bottom_trans_south[3]-bottom_trans_south[-1]) + " & %.2f " %(bottom_trans_south[4]-bottom_trans_south[-1]))
print("\centering \emph{Net Trans.}" + " & %.2f " %(stc_net_trans_south[0]-stc_net_trans_south[-1]) + " & %.2f " %(stc_net_trans_south[1]-stc_net_trans_south[-1]) + " & %.2f " %(stc_net_trans_south[2]-stc_net_trans_south[-1]) + " & %.2f " %(stc_net_trans_south[3]-stc_net_trans_south[-1]) + " & %.2f " %(stc_net_trans_south[4]-stc_net_trans_south[-1]))



