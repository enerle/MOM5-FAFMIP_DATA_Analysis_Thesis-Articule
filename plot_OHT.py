import sys
import os
import numpy as np
#import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = ' /home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["faf-stress","faf-water","faf-heat","faf-all","Control"]

filename3 = ["OHT_FAFSTRESS.nc","OHT_FAFWATER.nc","OHT_FAFHEAT.nc","OHT_FAFALL.nc","OHT_flux-only.nc"]

YY   = [None]*len(exp)
ATHT = [None]*len(exp)
GLHT = [None]*len(exp)
IPHT = [None]*len(exp)
SOHT = [None]*len(exp)

#---> Get the OHT
PW = 1e-15

for i in range(len(exp)):  
    fn = os.path.join(datadir,filename3[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    YY[i] = file.variables['YU_OCEAN'][:]
    ATHT[i] = file.variables['ATOHT'][:]*PW
    GLHT[i] = file.variables['GLOHT'][:]*PW
    IPHT[i] = file.variables['IPOHT'][:]*PW
    SOHT[i] = file.variables['SOOHT'][:]*PW
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

#-----------------------------------------------------------------------
##-----Plot OHT
#-----------------------------------------------------------------------

fig = plt.figure(1)

v=[-90,90,-.2,.2]
#v=[-90,90,-2,2]

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)-1):
    ax.plot(YY[i],GLHT[i]-GLHT[-1], color=colors[i],linewidth=2,linestyle=styles[i],label = exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("PW",fontsize=16)
ax.axis(v)

plt.title('Global (GLB)',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],[],fontsize=16)
plt.yticks([-.2,-.1,0,.1,.2],[-.2,-.1,0,.1,.2],fontsize=16)

##-----
ax = fig.add_subplot(2,2,2)
for i in range(len(exp)-1):
    ax.plot(YY[i],ATHT[i]-ATHT[-1], color=colors[i],linewidth=2,linestyle=styles[i],label = exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
ax.axis(v)

plt.title('Atlantic (ATL)',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],[])
plt.yticks([-.2,-.1,0,.1,.2],[])

##-----
ax = fig.add_subplot(2,2,3)
for i in range(len(exp)-1):
    ax.plot(YY[1],IPHT[i]-IPHT[-1], color=colors[i],linewidth=2,linestyle=styles[i],label = exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("PW",fontsize=16)
ax.axis(v)

plt.title('Indo Pacific (IPA)',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
plt.yticks([-.2,-.1,0,.1,.2],[-.2,-.1,0,.1,.2],fontsize=16)

##-----
ax = fig.add_subplot(2,2,4)
for i in range(len(exp)-1):
    ax.plot(YY[i],SOHT[i]-SOHT[-1], color=colors[i],linewidth=2,linestyle=styles[i],label = exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis(v)

plt.title('Southern Ocean (SOC)',style='normal',fontsize=16)
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)
plt.yticks([-.2,-.1,0,.1,.2],[])

#plt.show()
plt.savefig('OHT.png',transparent = True, bbox_inches='tight',dpi=600)

