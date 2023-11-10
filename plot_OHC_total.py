import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["Stress","Water","Heat","All","flux-only"]
filename = ["heat_content_FAFSTRESS.nc","heat_content_FAFWATER.nc","heat_content_FAFHEAT.nc","heat_content_FAFALL.nc","heat_content_flux-only.nc"]

OHC     = [None]*len(exp)
LAT     = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['YT_OCEAN'][:]
    OHC[i]   = file.variables['HEAT_CONTENT_500'][:]*1e-21 # ZJ    
    #OHC[i]   = file.variables['HEAT_CONTENT'][:]*1e-21 # ZJ
    OHC[i]   = np.squeeze(OHC[i])
    file.close()

#------------------------PLOTTING
#====================================================
colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(LAT[i],OHC[i]-OHC[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

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

#plt.show()
#plt.savefig('OHC_total_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

##CONTROL

fig = plt.figure(3)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)):
    ax.plot(LAT[i],OHC[i],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2); ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('[ZJ]',fontsize=16)
ax.legend(loc=2,fontsize=16)
ax.axis([-90,90,-1,300])

plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
####

plt.show()
#plt.savefig('OHC_total_zonalmean_CTL.png',transparent = True, bbox_inches='tight',dpi=600)                        
