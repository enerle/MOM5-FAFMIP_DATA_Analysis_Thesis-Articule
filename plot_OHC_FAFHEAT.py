import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp = ["Heat","Added","Redistributed","flux-only"]
var = ["Heat","Added heat","Redistributed heat","Added + Redist"]

filename = ['heat_content_FAFHEAT.nc','heat_content_added_FAFHEAT.nc','heat_content_redist_FAFHEAT.nc','heat_content_flux-only.nc']
#filename = ['heat_content_FAFHEAT-plus.nc','heat_content_added_FAFHEAT.nc','heat_content_redist_FAFHEAT-plus.nc','heat_content_flux-only.nc']

OHC     = [None]*len(exp)
LAT     = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['YT_OCEAN'][:]
    OHC[i]   = file.variables['HEAT_CONTENT_1000'][:]*1e-21 # ZJ
    OHC[i]   = np.squeeze(OHC[i])
    file.close()

OHC[0] = OHC[0]-OHC[-1]

#------------------------PLOTTING
#====================================================
colors = ['black','red','blue','green']
styles = ['solid','solid','solid','dashed']

#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(LAT[i],OHC[i],color=colors[i],linestyle=styles[i],linewidth=2.0,label=var[i])

ax.plot(LAT[1],OHC[1]+OHC[2],color=colors[3],linestyle=styles[3],linewidth=2.0,label=var[3])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[ZJ]',fontsize=16)
ax.legend(loc=3,fontsize=16)
ax.axis([-90,90,-15,20])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
####

plt.show()
#plt.savefig('OHC_FAFHEAT_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)
