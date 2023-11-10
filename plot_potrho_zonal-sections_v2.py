import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'

#exp      = ["Stress","Water","Heat","All","flux-only"]
#filename = ["zonalsection_rholevels_STC_FAFSTRESS.nc","zonalsection_rholevels_STC_FAFWATER.nc","zonalsection_rholevels_STC_FAFHEAT.nc","zonalsection_rholevels_STC_FAFALL.nc","zonalsection_rholevels_STC_flux-only.nc"]

exp      = ["Stress","Water","Heat","Control"]
filename = ["zonalsection_rholevels_STC_FAFSTRESS.nc","zonalsection_rholevels_STC_FAFWATER.nc","zonalsection_rholevels_STC_FAFHEAT.nc","zonalsection_rholevels_STC_flux-only.nc"]

LON    = [None]*len(exp)
DEPTH  = [None]*len(exp)
RHO_NH = [None]*len(exp)
RHO_SH = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON[i]    = file.variables['GRIDLON_T'][:]
    DEPTH[i]  = file.variables['ST_OCEAN'][:]
    RHO_NH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24N'][:,:,:])-1000. 
    RHO_SH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24S'][:,:,:])-1000.
    file.close()

#------------------------PLOTTING
rc('figure', figsize=(8.27,11.69))
#rc('figure', figsize=(11,8.27))
#rc('figure',figsize=(6.4,7.2))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.1,.1)

clevs_rho1 = [31.8668,32.7973,33.8931,34.6656,35.0366,35.3538,36.20,36.80,36.90]
clevs_rho2 = [0,31.8668,35.3538] #ekman, upper and bso

v = [-208,-71,0,1100]

fig = plt.figure(1)

fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()
subplots_adjust(wspace=None, hspace=.15)

##SOUTH
ax = fig.add_subplot(3,2,1)   
cc1 = plt.contour(LON[1],DEPTH[1],RHO_SH[1],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[1],DEPTH[1],RHO_SH[1],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[1][0:86],DEPTH[1][:],RHO_SH[1][:,0:86],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.title("South",fontsize=14)
plt.xticks([])
plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,3)
cc1 = plt.contour(LON[2],DEPTH[2],RHO_SH[2],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[2],DEPTH[i],RHO_SH[2],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[2][0:86],DEPTH[2][:],RHO_SH[2][:,0:86],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,5)
cc1 = plt.contour(LON[3],DEPTH[3],RHO_SH[3],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[3],DEPTH[i],RHO_SH[2],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[3][0:86],DEPTH[3][:],RHO_SH[3][:,0:86],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

##NORTH
clevs_rho1 = [32.1096,32.7334,33.9313,34.6682,36.2835,36.5690,36.7336,36.85,36.90]
clevs_rho2 = [0,32.1096,36.2835]

v = [-238,-112,0,1100] #v = [-238,-112,0,750]

ax = fig.add_subplot(3,2,2)
cc1 = plt.contour(LON[1],DEPTH[1],RHO_NH[1],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[1],DEPTH[1],RHO_NH[1],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[1][0:66],DEPTH[1][:],RHO_NH[1][:,0:66],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.title("North",fontsize=14)
plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,4)
cc1 = plt.contour(LON[2],DEPTH[2],RHO_NH[2],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[2],DEPTH[i],RHO_NH[2],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[2][0:66],DEPTH[2][:],RHO_NH[2][:,0:66],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(3,2,6)
cc1 = plt.contour(LON[3],DEPTH[3],RHO_NH[3],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[3],DEPTH[i],RHO_NH[2],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[3][0:66],DEPTH[3][:],RHO_NH[3][:,0:66],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

plt.savefig('stc_section_rholevels.png',transparent = False, bbox_inches='tight',dpi=300)

##control simulation 
fig = plt.figure(2)

fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()
subplots_adjust(wspace=None, hspace=.15)

#SOUTH
clevs_rho1 = [31.8668,32.7973,33.8931,34.6656,35.0366,35.3538,36.20,36.80,36.90]
clevs_rho2 = [0,31.8668,35.3538] #ekman, upper and bs
v = [-208,-71,0,1100]
#v = [-208,-111,0,1100]

ax = fig.add_subplot(3,2,1)
cc1 = plt.contour(LON[-1],DEPTH[-1],RHO_SH[-1],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[-1],DEPTH[-1],RHO_SH[-1],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5) #WBC
cc3 = plt.contour(LON[-1][0:86],DEPTH[-1][:],RHO_SH[-1][:,0:86],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.title("South",fontsize=14)
plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#NORTH
clevs_rho1 = [32.1096,32.7334,33.9313,34.6682,36.2835,36.5690,36.7336,36.85,36.90]
clevs_rho2 = [0,32.1096,36.2835]
v = [-238,-112,0,1100] #v = [-238,-112,0,750]

ax = fig.add_subplot(3,2,2)
cc1 = plt.contour(LON[1],DEPTH[1],RHO_NH[1],levels=clevs_rho1,colors='gray',linestyles='solid',linewidths=.5)
#plt.clabel(cc1,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
cc2 = plt.contour(LON[1],DEPTH[1],RHO_NH[1],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2.5)
cc3 = plt.contour(LON[1][0:66],DEPTH[1][:],RHO_NH[1][:,0:66],levels=[33.8931],colors='black',linestyles='solid',linewidths=2.5)

plt.title("North",fontsize=14)
plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#plt.show()
plt.savefig('stc_section_rholevels_flux-only.png',transparent = False, bbox_inches='tight',dpi=300)
