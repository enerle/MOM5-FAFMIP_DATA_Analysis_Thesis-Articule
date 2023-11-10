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

exp      = ["Stress","Water","Heat","All","flux-only"]
filename = ["DSL_FAFSTRESS.nc","DSL_FAFWATER.nc","DSL_FAFHEAT.nc","DSL_FAFALL.nc","DSL_flux-only.nc"]

DSL      = [None]*len(exp)
DSLzonal = [None]*len(exp)
LON      = [None]*len(exp)
LON2     = [None]*len(exp)
LAT      = [None]*len(exp)
LAT2     = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LON[i]   = file.variables['XT_OCEAN'][:]
    LAT[i]   = file.variables['YT_OCEAN'][:]
    DSL[i]   = file.variables['DSL'][:,:]
    file.close()

for i in range(len(exp)):
    DSLzonal[i] = np.ma.average(DSL[i],axis=1)

#------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

cmap2 = plt.get_cmap('bwr')
cmap2.set_bad(color = '0.5', alpha = None)

kmin = -.3; kmax = .3
#clevs = np.linspace(kmin,kmax,12)
#clevs = np.arange(kmin,kmax+.05,.05)
clevs  = [-0.3,-0.15,-0.1,-0.05,0.05,0.1,0.15,0.3]

fig = plt.figure(1)
#fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)


for i in range(len(exp)-1):

    [LON2[i],LAT2[i]] = np.meshgrid(LON[i],LAT[i])
    
    ax  = fig.add_subplot(3,2,i+1)
    cs  = plt.pcolormesh(DSL[i]-DSL[-1],shading='flat',cmap=cmap2)
    cs1 = plt.contourf(DSL[i]-DSL[-1],levels=clevs,cmap=cmap2,extend='both')

    #plt.clim(kmin,kmax)
    plt.title('%s' % (exp[i]),fontsize=14,color='k')
    #plt.yticks(fontsize=10)

    plt.xticks([]); plt.yticks([])
    
    ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)    
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

#Changes in colorbar
cbaxes = fig.add_axes([0.3, 0.32, 0.4, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs1,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=12)
#cbar.ax.set_yticklabels(['-0.15','-0.1','-0.05','-0.02','0.02','0.05','0.1','0.15'])
cbar.ax.set_title("$\zeta^{'}$ [m]",fontsize=14,color='k')

#plt.show()
plt.savefig('DSL.png',transparent = True, bbox_inches='tight',dpi=600)

##-------------ZONAL MEAN
letter = ["(a)","(b)","(c)","(d)","(e)","(f)","(h)","(g)"]
colors = ['black','blue','red','green']
styles = ['solid','solid','solid','solid']

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(LAT[i],DSLzonal[i]-DSLzonal[-1],linestyle=styles[i],color=colors[i],linewidth=2.0,label=exp[i])

####
ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$\zeta^{'}$ [m]",fontsize=16)
#ax.set_ylim(kmin,kmax)
ax.legend(loc=4,fontsize=16)

ax.axis([-90,90,-0.4,0.4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)

#plt.show()
plt.savefig('DSL_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

#########################################
##
#------------------------PLOTTING CONTROL
##
#########################################

#rc('text',usetex=True)
#rc('figure', figsize=(11.69,8.27))
rc('figure', figsize=(8.27,11.69))

cmap2 = plt.get_cmap('coolwarm')
#cmap2 = cmocean.cm.balance
cmap2.set_bad(color = '0.5', alpha = None)

kmin = -2; kmax = 2
clevs = [-2,-1.5,-1,-.75,-.5,-.25,0,.25,.5,.75,1,1.5,2]

fig = plt.figure(3)
fig.subplots_adjust(hspace=0.25,wspace=0.2)

[LON2[-1],LAT2[-1]] = np.meshgrid(LON[-1],LAT[-1])

ax1 = plt.subplot2grid((2,5),(0,0),colspan=4)
cs  = plt.pcolormesh(DSL[-1],shading='flat',cmap=cmap2)
cs1 = plt.contourf(DSL[-1],levels=clevs,cmap=cmap2,extend='both')
plt.clim(kmin,kmax)

plt.xticks([]); plt.yticks([])

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

cbaxes = fig.add_axes([0.2, 0.50, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs1,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal",fraction=.1)
cbar.ax.tick_params(labelsize=10)
#cbar.ax.set_yticklabels(clevs)
cbar.ax.set_title("$\zeta$ [m]",fontsize=14,color='k')

ax2 = plt.subplot2grid((2,5),(0,4),colspan=1) #zonal mean
ax2.plot(DSLzonal[-1],LAT[-1],'-',color='k',linewidth=1.5)
ax2.axis([-2,2,-90,90])

plt.axvline(x=0.0,color='k',linestyle='--',linewidth=1.5) #includes zero line
plt.xticks([-2,-1,0,1,2])
plt.yticks([])

ax2.spines['top'].set_linewidth(2);  ax2.spines['bottom'].set_linewidth(2)
ax2.spines['left'].set_linewidth(2); ax2.spines['right'].set_linewidth(2)
ax2.xaxis.set_tick_params(width=2);  ax2.yaxis.set_tick_params(width=2)

#plt.show()
plt.savefig('DSL_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

##-------------ZONAL MEAN
rc('figure', figsize=(11.69,8.27))
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

fig = plt.figure(4)
ax = fig.add_subplot(1,1,1)

for i in range(len(exp)-1):
    ax.plot(LAT[i],DSLzonal[i],linestyle=styles[i],color=colors[i],linewidth=2.0,label=exp[i])

ax.plot(LAT[-1],DSLzonal[-1],color='gray',linestyle='solid',linewidth=2.0,label='flux-only')

####
ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("$\zeta$ [m]",fontsize=16)
#ax.set_ylim(kmin,kmax)
ax.legend(loc=4,fontsize=16)

ax.axis([-90,90,-2,1])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=16)

#plt.show()
plt.savefig('DSL_zonalmean_CTL.png',transparent = True, bbox_inches='tight',dpi=600)
