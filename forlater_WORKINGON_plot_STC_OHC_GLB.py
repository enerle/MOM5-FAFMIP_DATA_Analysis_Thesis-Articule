import sys
import os
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp       = ["Stress","Water","Heat","All","flux-only"]
filename1 = ["STC_OHC_FAFSTRESS_GLB_time_v2.nc","STC_OHC_FAFWATER_GLB_time_v2.nc","STC_OHC_FAFHEAT_GLB_time_v2.nc","STC_OHC_FAFALL_GLB_time_v2.nc","STC_OHC_flux-only_GLB_time_v2.nc"]

OHC_tot     = [None]*len(exp)
OHC_stc     = [None]*len(exp)
OHC_int     = [None]*len(exp)

LAT         = [None]*len(exp)

yt = 1e-21

for i in range(len(filename1)):
    fn = os.path.join(datadir,filename1[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]     = file.variables['YT_OCEAN53_134'][:]
    OHC_tot[i] = np.squeeze(np.mean(file.variables['OHC_TOT_ZONAL'][:],axis=0))*yt
    OHC_stc[i] = np.squeeze(np.mean(file.variables['OHC_STC_ZONAL'][:],axis=0))*yt
    OHC_int[i] = np.squeeze(np.mean(file.variables['OHC_INT_ZONAL'][:],axis=0))*yt 
    file.close()

#------------------------PLOTTING
#====================================================
colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

#rc('text', usetex=True)
#rc('figure', figsize=(11.69,8.27))
rc('figure', figsize=(8.27,11.69)) 

#OCEAN HEAT CONTENT WITHIN THE SUBTROPICAL CELL AND THE INTERIOR OCEAN
fig = plt.figure(1)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(LAT[i],OHC_tot[i]-OHC_tot[-1],color=colors[i],linestyle='solid',linewidth=2.0)

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$\Delta$ OHC [ZJ]',fontsize=16)
ax.axis([-30,30,-15,15])

plt.title('Total')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-30,-20,-10,0,10,20,30],[])

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(LAT[i],OHC_stc[i]-OHC_stc[-1],color=colors[i],linestyle='solid',linewidth=2.0)

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$\Delta$ OHC [ZJ]',fontsize=16)
ax.axis([-30,30,-100,100])

plt.title('Overturn')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-30,-20,-10,0,10,20,30],[])

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(LAT[i],OHC_int[i]-OHC_int[-1],color=colors[i],linestyle='solid',linewidth=2.0,label=exp[i])

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('$\Delta$ OHC [ZJ]',fontsize=16)
ax.legend(loc=3,fontsize=12)
ax.axis([-30,30,-100,100])

plt.title('Interior')
plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-30,-20,-10,0,10,20,30],['30S','20S','10S','0','10N','20N','30N'],fontsize=16)
####

#plt.show()
#plt.savefig('STC_OHC_GLB.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(2)
ax = fig.add_subplot(2,1,1)
i=-1
ax.plot(LAT[i],OHC_tot[i],color='black',linestyle='solid',linewidth=2.0,label='Total')
ax.plot(LAT[i],OHC_stc[i],color='red',linestyle='solid',linewidth=2.0,label='Overturn')
ax.plot(LAT[i],OHC_int[i],color='blue',linestyle='solid',linewidth=2.0,label='Interior')

####
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.set_ylabel('OHC [ZJ]',fontsize=16)
ax.legend(loc=2,fontsize=12)
#ax.axis([-30,30,0,100])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-30,-20,-10,0,10,20,30],['30S','20S','10S','0','10N','20N','30N'],fontsize=16)

plt.show()
#plt.savefig('STC_OHC_GLB_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

