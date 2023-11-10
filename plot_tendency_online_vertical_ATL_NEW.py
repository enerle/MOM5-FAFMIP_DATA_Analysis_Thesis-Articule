import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc
import decimal
from decimal import Decimal

##multiplicar por area para obtener unidades de watt

datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_TEMP-tend'
filename = ["heat_budget_FAFSTRESS_vertical_ATL.nc","heat_budget_FAFWATER_vertical_ATL.nc","heat_budget_FAFHEAT_vertical_ATL.nc","heat_budget_flux-only_vertical_ATL.nc"]

depth          = [None]*len(filename)
temptend       = [None]*len(filename)
advection      = [None]*len(filename)
submeso        = [None]*len(filename)
neutral_gm     = [None]*len(filename)
diapycnal_mix  = [None]*len(filename)
isopycnal_mix  = [None]*len(filename)
swh            = [None]*len(filename)
residual       = [None]*len(filename)
super_residual = [None]*len(filename)
eddy           = [None]*len(filename)
advection      = [None]*len(filename)
total          = [None]*len(filename)
unresolved     = [None]*len(filename)
vdiff          = [None]*len(filename)

yt = 1e-12 #TW

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    depth[i]             = file.variables['ST_OCEAN27_50'][:]
    temptend[i]          = np.squeeze(file.variables['TEMPTEND'][:])*yt
    advection[i]         = np.squeeze(file.variables['ADVECTION'][:])*yt
    submeso[i]           = np.squeeze(file.variables['SUBMESO'][:])*yt
    neutral_gm[i]        = np.squeeze(file.variables['NEUTRAL_GM'][:])*yt
    diapycnal_mix[i]     = np.squeeze(file.variables['VDIFFUSE_DIFF_CBT'][:])*yt
    isopycnal_mix[i]     = np.squeeze(file.variables['NEUTRAL_DIFFUSION'][:])*yt
    swh[i]               = np.squeeze(file.variables['SWH'][:])*yt
#    temptend[i]          = Decimal(file.variables['TEMPTEND'])
#    advection[i]         = Decimal(file.variables['ADVECTION'])
#    submeso[i]           = Decimal(file.variables['SUBMESO'])
#    neutral_gm[i]        = Decimal(file.variables['NEUTRAL_GM'])
#    diapycnal_mix[i]     = Decimal(file.variables['VDIFFUSE_DIFF_CBT'])
#    isopycnal_mix[i]     = Decimal(file.variables['NEUTRAL_DIFFUSION'])
#    swh[i]               = Decimal(file.variables['SWH'])
    file.close()

for i in range(len(filename)):
    residual[i]       = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]           =                submeso[i] + neutral_gm[i]
    super_residual[i] = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i]
    total[i]          = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i] + diapycnal_mix[i] + swh[i]
    unresolved[i]     = temptend[i]  - total[i]
    vdiff[i]          = diapycnal_mix[i] + swh[i] + unresolved[i]

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

#for i in range(len(filename)):
i=2
ax  = fig.add_subplot(2,2,1)
ax.plot(temptend[i][:],-depth[i][:],linestyle='-',linewidth=2,color=[0,0,0],label='NET')
ax.plot(advection[i],-depth[i][:],linestyle='-',linewidth=2,color=[1,0,0],label='ADV')
ax.plot(eddy[i],-depth[i][:],linestyle='-',linewidth=2,color=[1,.5,.5],label='EDDY')
ax.plot(residual[i], -depth[i][:],linestyle=':',linewidth=1.5,color=[0,0,0],label='rADV')
ax.plot(isopycnal_mix[i],-depth[i][:],linestyle='-',linewidth=2,color=[0,0,1],label='ISO')
ax.plot(vdiff[i],-depth[i][:],linestyle='-',linewidth=2,color=[.5,.5,1],label='vDIFF')
ax.plot(super_residual[i],-depth[i][:],linestyle='-',linewidth=2,color=[.5,.5,.5],label='srADV')
##no hacer anomalias, se ve horrible

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

plt.title('Total ocean heat budget (c)',style='normal',fontsize=14)
ax.set_ylabel('Depth (m)',fontsize=14)
ax.set_xlabel('TW m$^{-2}$',fontsize=14)
ax.legend(loc=3,fontsize=9)
#ax.axis([-80,80,-5500,0])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[0,-1000,-2000,-3000,-4000,-5000])

ax  = fig.add_subplot(2,2,2)
ax.plot((super_residual[i]+vdiff[i])-(super_residual[-1]+vdiff[-1]),-depth[i][:],linestyle='-',linewidth=2,color='black',label='NET')
ax.plot(vdiff[i]-vdiff[-1],-depth[i][:],linestyle='-',linewidth=2,color=[.5,.5,1],label='vDIFF')
ax.plot(super_residual[i]-super_residual[-1],-depth[i][:],linestyle='-',linewidth=2,color=[.5,.5,.5],label='srADV')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

plt.title('Super-residual framework (d)',style='normal',fontsize=14)
ax.set_xlabel('TW m$^{-2}$',fontsize=14)
ax.legend(loc=4,fontsize=9)
ax.axis([-5,20,-5500,0])
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[])

#plt.show()
plt.savefig('tendency_online_vertical_FAFHEAT_ATL.png',transparent = False, bbox_inches='tight',dpi=300)
