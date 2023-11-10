import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = ' /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["faf-stress","faf-water","faf-heat","faf-all","Control"]

filename2 = ["MOC_FAFSTRESS.nc","MOC_FAFWATER.nc","MOC_FAFHEAT.nc","MOC_FAFALL.nc","MOC_flux-only.nc"]

time  = [None]*len(exp)

AMOC_41N = [None]*len(exp)
AMOC_26N = [None]*len(exp)
AMOC_30S = [None]*len(exp)
AABW     = [None]*len(exp)

#---> Get the AMOC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename2[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    AMOC_41N[i] = file.variables['AMOC_41N'][:]
    AMOC_26N[i] = file.variables['AMOC_26N'][:]
    AMOC_30S[i] = file.variables['AMOC_30S'][:]
    AABW[i]    = file.variables['AABW'][:]
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

##------AMOC
fig = plt.figure(1)
fig.subplots_adjust(top=.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)-1):
    ax.plot(time[i],AMOC_41N[i]-AMOC_41N[-1][0],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time (years)",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.axis([0,70,-10,10])

plt.title('AMOC 41 $^o$ N',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-10,11,2.5),fontsize=16)
###

ax = fig.add_subplot(2,2,2)
for i in range(len(exp)-1):
    ax.plot(time[i],AABW[i]-AABW[-1][0],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_xlabel("Time (years)",fontsize=16)
ax.legend(loc=4,ncol=2, fontsize=16)
ax.axis([0,70,-10,10])

plt.title('AABW 50 $^o$ S',fontsize=16,color='k')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks(np.arange(0,71,10),fontsize=16)
plt.yticks(np.arange(-10,11,2.5),[],fontsize=16)
###

#plt.show()
plt.savefig('MOC_AMOC_timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

