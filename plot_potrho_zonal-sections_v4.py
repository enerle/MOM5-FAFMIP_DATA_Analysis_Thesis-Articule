import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir  = '/home/clima-archive2/rfarneti/RENE/DATA'
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["faf-stress","faf-water","faf-heat","Control"]
names_sh = ["(c) faf-stress","(e) faf-water","(g) faf-heat","(a) Control"]
names_nh = ["(d) faf-stress","(f) faf-water","(h) faf-heat","(b) Control"]

filename1 = ["zonalsection_rholevels_STC_FAFSTRESS.nc","zonalsection_rholevels_STC_FAFWATER.nc","zonalsection_rholevels_STC_FAFHEAT.nc","zonalsection_rholevels_STC_flux-only.nc"]
filename2 = ["zonalsection_velocity_STC_FAFSTRESS.nc","zonalsection_velocity_STC_FAFWATER.nc","zonalsection_velocity_STC_FAFHEAT.nc","zonalsection_velocity_STC_flux-only.nc"]
filename3 = ["zonalsection_trans_STC_FAFSTRESS.nc","zonalsection_trans_STC_FAFWATER.nc","zonalsection_trans_STC_FAFHEAT.nc","zonalsection_trans_STC_flux-only.nc"]
filename4 =  ["zonalsection_trans_rho_STC_FAFSTRESS.nc","zonalsection_trans_rho_STC_FAFWATER.nc","zonalsection_trans_rho_STC_FAFHEAT.nc","zonalsection_trans_rho_STC_flux-only.nc"]

LON         = [None]*len(exp)
DEPTH       = [None]*len(exp)
LON_VEL     = [None]*len(exp)
DEPTH_VEL   = [None]*len(exp)
LON_TRANS   = [None]*len(exp)
DEPTH_TRANS    = [None]*len(exp)
LON_TRANSRHO   = [None]*len(exp)
DEPTH_TRANSRHO = [None]*len(exp)
RHO_NH = [None]*len(exp)
RHO_SH = [None]*len(exp)
VEL_NH = [None]*len(exp)
VEL_SH = [None]*len(exp)
TRANS_NH = [None]*len(exp)
TRANS_SH = [None]*len(exp)
TRANSRHO_NH = [None]*len(exp)
TRANSRHO_SH = [None]*len(exp)

for i in range(len(filename1)):
    fn = os.path.join(datadir,filename1[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON[i]    = file.variables['GRIDLON_T'][:]
    DEPTH[i]  = file.variables['ST_OCEAN'][:]
    RHO_NH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24N'][:,:,:])-1000. 
    RHO_SH[i] = np.squeeze(file.variables['POT_RHO_PASOC_24S'][:,:,:])-1000.
    file.close()

for i in range(len(filename2)):
    fn = os.path.join(datadir,filename2[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON_VEL[i]    = file.variables['XU_OCEAN'][:]
    DEPTH_VEL[i]  = file.variables['ST_OCEAN'][:]
    VEL_NH[i] = np.squeeze(file.variables['VEL_PAC_24N'][:,:,:])*10
    VEL_SH[i] = np.squeeze(file.variables['VEL_PAC_24S'][:,:,:])*10
    file.close()

for i in range(len(filename3)):
    fn = os.path.join(datadir,filename3[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON_TRANS[i]    = file.variables['XT_OCEAN'][:]
    DEPTH_TRANS[i]  = file.variables['ST_OCEAN'][:]
    TRANS_NH[i] = np.squeeze(file.variables['TRANS_PAC_24N'][:,:,:])
    TRANS_SH[i] = np.squeeze(file.variables['TRANS_PAC_24S'][:,:,:])
    file.close()

for i in range(len(filename4)):
    fn = os.path.join(datadir,filename4[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    LON_TRANSRHO[i]    = file.variables['GRID_XT_OCEAN'][:]
    DEPTH_TRANSRHO[i]  = file.variables['POTRHO'][:]
    TRANSRHO_NH[i] = np.squeeze(file.variables['TRANS_RHO_PAC_24N'][:,:,:])
    TRANSRHO_SH[i] = np.squeeze(file.variables['TRANS_RHO_PAC_24S'][:,:,:])
    file.close()
###Y ESTO COMO LO GRAFICO???


#------------------------PLOTTING

rc('figure', figsize=(8.27,11.69))
#rc('figure', figsize=(11,8.27))
#rc('figure',figsize=(6.4,7.2))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.1,.1)
clevs_rho2 = [0,31.8668,33.8931,35.3538] #ekman, upper and bso
v = [152,250,0,1100]

cmap      = plt.get_cmap('bwr')
kmin_vel  = -.3; kmax_vel = .3
clevs_vel = np.arange(kmin_vel,kmax_vel,.05)

kmin_trans  = -.25; kmax_trans = .25
clevs_vel = np.arange(kmin_trans,kmax_trans+.05,.05)

fig = plt.figure(1)

fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()

##SOUTH
k=1
for i in range(len(exp)-1):
    ax = fig.add_subplot(3,2,k)   
    cs = plt.contourf(LON_TRANS[i],DEPTH_TRANS[i],TRANS_SH[i][:,:]-TRANS_SH[-1][:,:],levels=clevs_vel,cmap=cmap,extend='both')
    plt.clim(kmin_trans,kmax_trans)
    cc2 = plt.contour(LON[i]+360,DEPTH[i],RHO_SH[i],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2)
    cc3 = plt.contour(LON[-1]+360,DEPTH[-1],RHO_SH[-1],levels=clevs_rho2,colors='gray',linestyles='solid',linewidths=2) #control
    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
    plt.title(names_sh[i],fontsize=14)
    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
    
    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ax.set_ylabel('Depth [m]',fontsize=14)

    plt.plot(np.ones(100)*(-195+360),linspace(60,650,100),color='gray',linestyle='--',linewidth=1.5)

    plt.xticks([])
    k=k+2
  
##NORTH
clevs_rho2 = [0,32.1096,33.8931,36.2835]
v = [122,245,0,1100]

k=2
for i in range(len(exp)-1):
    ax = fig.add_subplot(3,2,k)
    cs = plt.contourf(LON_TRANS[i],DEPTH_TRANS[i],TRANS_NH[i][:,:]-TRANS_NH[-1][:,:],levels=clevs_vel,cmap=cmap,extend='both')
    plt.clim(kmin_trans,kmax_trans)
    cc2 = plt.contour(LON[i]+360,DEPTH[i],RHO_NH[i],levels=clevs_rho2,colors='black',linestyles='solid',linewidths=2)
    cc3 = plt.contour(LON[-1]+360,DEPTH[-1],RHO_NH[-1],levels=clevs_rho2,colors='gray',linestyles='solid',linewidths=2) #control
    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
    plt.title(names_nh[i],fontsize=14)
    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    plt.plot(np.ones(10)*(-215+360),linspace(80,1030,10),color='gray',linestyle='--',linewidth=1.5)

    plt.xticks([])
    plt.yticks([0,200,400,600,800,1000],[])

    k=k+2

cbaxes = fig.add_axes([0.26, 0.05, 0.5, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs_vel,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=9)
cbar.ax.set_title("Sv",fontsize=14,color='k')

plt.savefig('trans_density_longitudinal_sections_control.png',transparent = False, bbox_inches='tight',dpi=300)

kmin_trans  = -1; kmax_trans = 1
clevs_vel = np.arange(kmin_trans,kmax_trans+.2,.2)

fig = plt.figure(2)

v = [152,250,0,1100]
clevs_rho2 = [0,31.8668,33.8931,35.3538] #ekman, upper and bso

ax = fig.add_subplot(3,2,1)
cs = plt.contourf(LON_TRANS[-1],DEPTH_TRANS[-1],TRANS_SH[-1][:,:],levels=clevs_vel,cmap=cmap,extend='both')
plt.clim(kmin_trans,kmax_trans)
cc2 = plt.contour(LON[-1]+360,DEPTH[-1],RHO_SH[-1],levels=clevs_rho2,colors='gray',linestyles='solid',linewidths=2)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
plt.title(names_sh[-1],fontsize=14)
ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
ax.set_ylabel('Depth [m]',fontsize=14)

plt.plot(np.ones(100)*(-195+360),linspace(60,650,100),color='gray',linestyle='--',linewidth=1.5)

plt.xticks([])

v = [122,245,0,1100]
clevs_rho2 = [0,32.1096,33.8931,36.2835]

ax = fig.add_subplot(3,2,2)
cs = plt.contourf(LON_TRANS[-1],DEPTH_TRANS[i-1],TRANS_NH[-1][:,:],levels=clevs_vel,cmap=cmap,extend='both')
plt.clim(kmin_trans,kmax_trans)
cc2 = plt.contour(LON[-1]+360,DEPTH[-1],RHO_NH[-1],levels=clevs_rho2,colors='gray',linestyles='solid',linewidths=2) #control
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
plt.title(names_nh[-1],fontsize=14)
ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linestyle(':')
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.plot(np.ones(10)*(-215+360),linspace(80,1030,10),color='gray',linestyle='--',linewidth=1.5)

plt.xticks([])
plt.yticks([0,200,400,600,800,1000],[])

cbaxes = fig.add_axes([0.26, 0.60, 0.5, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs_vel,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=9)
cbar.ax.set_title("Sv",fontsize=14,color='k')
plt.savefig('trans_density_longitudinal_sections_fafmip.png',transparent = False, bbox_inches='tight',dpi=300)

plt.show()
