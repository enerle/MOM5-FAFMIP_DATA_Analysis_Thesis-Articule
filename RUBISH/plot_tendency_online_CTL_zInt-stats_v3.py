import sys
import os
import numpy as np
from scipy.stats import pearsonr
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

##multiplicar por area para obtener unidades de watt

datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA_TEMP-tend'
filename = 'temp_diag_tend-FAFHEAT.nc'
#filename = 'temp_diag_tend-flux-only.nc'
fn = os.path.join(datadir,filename)
file = nc.Dataset(fn)
depth      = file.variables['st_ocean'][:]
temptend   = np.squeeze(np.mean(file.variables['temp_tendency'][:,:,:,:],axis=(2,3)))
advection  = np.squeeze(np.mean(file.variables['temp_advection'][:,:,:,:],axis=(2,3)))
submeso    = np.squeeze(np.mean(file.variables['temp_submeso'][:,:,:,:],axis=(2,3)))
neutral_gm = np.squeeze(np.mean(file.variables['neutral_gm_temp'][:,:,:,:],axis=(2,3)))
diapycnal  = np.squeeze(np.mean(file.variables['temp_vdiffuse_diff_cbt'][:,:,:,:],axis=(2,3)))
isopycnal  = np.squeeze(np.mean(file.variables['neutral_diffusion_temp'][:,:,:,:],axis=(2,3)))
swh        = np.squeeze(np.mean(file.variables['sw_heat'][:,:,:,:],axis=(2,3))) 

residual       = advection + submeso + neutral_gm
eddy           =             submeso + neutral_gm
super_residual = advection + submeso + neutral_gm + isopycnal
total          = advection + submeso + neutral_gm + isopycnal + diapycnal + swh
unresolved     = temptend  - total
vdiff          = (diapycnal + swh) +  unresolved

temptend_mean       = np.mean(temptend,axis=0)
advection_mean      = np.squeeze(np.mean(advection,axis=0))
eddy_mean           = np.squeeze(np.mean(eddy,axis=0))
residual_mean       = np.squeeze(np.mean(residual,axis=0))
isopycnal_mean      = np.squeeze(np.mean(isopycnal,axis=0))
diapycnal_mean      = np.squeeze(np.mean(diapycnal,axis=0))
total_mean          = np.squeeze(np.mean(total,axis=0))
super_residual_mean = np.squeeze(np.mean(super_residual,axis=0))
vdiff_mean          = np.squeeze(np.mean(vdiff,axis=0))
unresolved_mean     = np.squeeze(np.mean(unresolved,axis=0))      
swh_mean            = np.squeeze(np.mean(swh,axis=0))
temptend_std        = np.squeeze(np.std(temptend,axis=0))

#rc('text', usetex=True)
rc('figure', figsize=(8.27,11.69))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax  = fig.add_subplot(2,2,1)
ax.plot(temptend_mean[27:50], -depth[27:50],linestyle='-',linewidth=2,color=[0,0,0],label='NET')
ax.plot(advection_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[1,0,0],label='ADV')
ax.plot(eddy_mean[27:50],     -depth[27:50],linestyle='-',linewidth=2,color=[1,.5,.5],label='EDDY')
ax.plot(residual_mean[27:50], -depth[27:50],linestyle=':',linewidth=1.5,color=[0,0,0],label='rADV')
ax.plot(isopycnal_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[0,0,1],label='ISO')
ax.plot(diapycnal_mean[27:50],    -depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,1],label='DIA')
ax.plot(swh_mean[27:50],    -depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,1],label='SWH')
#ax.plot(super_residual_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,.5],label='srADV')
#ax.plot(unresolved_mean[27:50],-depth[27:50],linestyle='-',linewidth=1,color=[.2,.2,.2],label='unres')

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

plt.title('Total ocean heat budget (a)',style='normal',fontsize=14)
ax.set_ylabel('Depth (m)',fontsize=14)
ax.set_xlabel('W m$^{-2}$',fontsize=14)
ax.legend(loc=3,fontsize=9)
ax.axis([-.6,.6,-5500,0])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[0,-1000,-2000,-3000,-4000,-5000])

ax  = fig.add_subplot(2,2,2)
ax.plot(super_residual_mean[27:50]+vdiff_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color='black',label='NET')
ax.plot(vdiff_mean[27:50],    -depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,1],label='vDIFF')
ax.plot(super_residual_mean[27:50],-depth[27:50],linestyle='-',linewidth=2,color=[.5,.5,.5],label='srADV')


ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

plt.title('Super-residual framework (b)',style='normal',fontsize=14)
ax.set_xlabel('W m$^{-2}$',fontsize=14)
ax.legend(loc=4,fontsize=9)
ax.axis([-.06,.15,-5500,0])
plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2)
plt.yticks([0,-1000,-2000,-3000,-4000,-5000],[])

plt.show()
#plt.savefig('tendency_online_CTL_zInt-stats_V2.png',transparent = False, bbox_inches='tight',dpi=300)
