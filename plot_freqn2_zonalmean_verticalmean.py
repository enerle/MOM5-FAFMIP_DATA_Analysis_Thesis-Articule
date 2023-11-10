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
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'
exp       = ["faf-stress","faf-water","faf-heat","control"]
filename1 = ["freqn2_FAFSTRESS_PAC.nc","freqn2_FAFWATER_PAC.nc","freqn2_FAFHEAT_PAC.nc","freqn2_flux-only_PAC.nc"]

freqn2  = [None]*len(exp)
lat     = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename1[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    lat[i]    = file.variables['GRIDLAT_T'][:]
    freqn2[i] = file.variables['F500'][:]*1e4
    file.close()

##-------------ZONAL MEAN

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

rc('figure', figsize=(11.69,8.27))

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)
ax = fig.add_subplot(1,1,1)

#for i in range(len(exp)-1):
#    ax.plot(lat[i],freqn2[i][:]-freqn2[-1][:],linestyle='solid',color=colors[i],linewidth=2.0,label=exp[i])

ax.plot(lat[i],freqn2[0][:]-freqn2[-1][:],linestyle='solid',color=colors[0],linewidth=2.0,label=exp[0])
ax.plot(lat[i],freqn2[1][:]-freqn2[-1][:],linestyle='solid',color=colors[1],linewidth=2.0,label=exp[1])
ax.plot(lat[i],freqn2[2][:]-freqn2[-1][:],linestyle='solid',color=colors[2],linewidth=2.0,label=exp[2])

####
ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("10$^{-4}$ s$^{-2}$",fontsize=16,color='k')
ax.legend(loc=2,fontsize=16)

ax.axis([-40,60,-.05,.15])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
#plt.xticks([-75,-60,-45,-30,-15,0,15,30,45,60,75],["75S","60S","45S","30S","15S","0","15N","30N","45N","60N","75N"],fontsize=12)
plt.xticks([-40,-30,-20,-10,0,10,20,30,40,50,60],['40S','30S','20S','10S','0','10','20N','30N','40N','50N','60N'],fontsize=16)

#ax.axis([-80,70,-.05,.15])

#plt.show()
plt.savefig('STC_freqn2_zonalverticalmean_500m_PAC.png',transparent = True, bbox_inches='tight',dpi=600)

