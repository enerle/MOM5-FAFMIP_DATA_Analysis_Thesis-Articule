import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp      = ["Stress","Water","Heat","All","control"]
filename1 = ["ACC_FAFSTRESS.nc","ACC_FAFWATER.nc","ACC_FAFHEAT.nc","ACC_FAFALL.nc","ACC_flux-only.nc"]

ACC   = [None]*len(exp)
time  = [None]*len(exp)
time2 = [None]*len(exp)

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    ACC[i] = file.variables['ACC'][:]
    ACC[i] = np.squeeze(ACC[i])
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']


#------ACC
fig = plt.figure(1)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(time[i],ACC[i]-ACC[-1][0],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("Change in ACC [Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis([0,70,-40,40])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ACC_timeseries.png',transparent = True, bbox_inches='tight',dpi=600)


#------ACC: the same but in percentage
fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(time[i],((ACC[i]-ACC[-1][0])/ACC[-1][0])*100,color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("Change in ACC [%]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis([0,70,-20,20])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('ACC_timeseries_percentage.png',transparent = True, bbox_inches='tight',dpi=600)
