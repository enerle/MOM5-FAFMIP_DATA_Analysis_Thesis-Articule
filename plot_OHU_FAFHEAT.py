#
import sys
import os
import numpy as np
import numpy.ma as ma
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

#exp = ["FAF-heat $T^{'}$","FAF-heat+ $T^{'}$","FAF-heat $T_A^{'}$","FAF-heat+ $T_A^{'}$","FAF-heat $T_R^{'}$","FAF-heat+ $T_R^{'}$"]

exp = ["$H_A^{'}$","$H_R^{'}$"]
#filename  = ['OHU_added_FAFHEAT.nc','OHU_added_FAFHEAT-plus.nc','OHU_redist_FAFHEAT.nc','OHU_redist_FAFHEAT-plus.nc']
filename  = ['OHU_added_FAFHEAT.nc','OHU_redist_FAFHEAT.nc']

#letter = ["(a)","(b)","(c)"]

OHU      = [None]*len(exp)
OHUmean  = [None]*len(exp)
LON      = [None]*len(exp)
LON2     = [None]*len(exp)
LAT      = [None]*len(exp)
LAT2     = [None]*len(exp)

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON[i]     = file.variables['XT_OCEAN'][:]
    LAT[i]     = file.variables['YT_OCEAN'][:]
    OHU[i]     = file.variables['OHU'][:,:]*1e-9 # GJ/m^2
    OHU[i]     = squeeze(OHU[i])
    OHUmean[i] = np.ma.average(OHU[i],axis=(0,1))
    file.close()

#------------------------PLOTTING
#rc('text',usetex=True)
rc('figure', figsize=(11.69,8.27))

#cmap2 = plt.get_cmap('coolwarm')
#cmap2 = cmocean.cm.balance
cmap2 = plt.get_cmap('bwr')
cmap2.set_bad(color = '0.5', alpha = None)

kmin = -15; kmax = 15
#clevs = [-15,-10,-5,-2,-1,-0.5,0.5,1,2,5,10,15]
#clevs = np.arange(kmin,kmax,1)
clevs = np.linspace(kmin,kmax,16)

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)):

    [LON2[i],LAT2[i]] = np.meshgrid(LON[i],LAT[i])
    
    ax = fig.add_subplot(3,2,i+1)
    #cs  = plt.pcolormesh(LON1[i],LAT2[i],OHU[i]-OHUmean[i],shading='flat',cmap=cmap2)
    #cs1 = plt.contourf(LON2[i],LAT2[i],OHU[i]-OHUmean[i],levels=clevs,cmap=cmap2,extend='both')
    cs  = plt.pcolormesh(LON2[i],LAT2[i],OHU[i],shading='flat',cmap=cmap2)
    cs1 = plt.contourf(LON2[i],LAT2[i],OHU[i],levels=clevs,cmap=cmap2,extend='both')

    plt.clim(kmin,kmax)

    #plt.title('%s' % (exp[i]),fontsize=16,color='k')
    plt.title("%s" %exp[i] + " (%.2f $GJm^{-2}$)" %OHUmean[i],fontsize=16)
#OHUmean[i]-OHUmean[-1]
    plt.xticks([]); plt.yticks([])
    
    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)


#Changes in colorbar
cbaxes = fig.add_axes([0.3, 0.64, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs1,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)
#cbar.ax.set_yticklabels(['-20','-15','-10','-5','-2','-1','-0.5','0.5','1','2','5','10','15','20'])
cbar.ax.set_title('[$GJm^{-2}$]',fontsize=14,color='k')

#plt.show()
plt.savefig('OHU_FAFHEAT.png',transparent = True, bbox_inches='tight',dpi=600)
