import sys
import os
import numpy as np
import cmocean
import matplotlib as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/ART/DATA_TEMP-tend/DATA_vInt_MLD_BSO_v2'
#datadir2 = '/home/clima-archive2/rfarneti/RENE/DATA'
datadir2 = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp      = ["faf-stress","faf-water","faf-heat","faf-all","control"]
filename = ["STC_temptend_FAFSTRESS_PAC_zonal.nc","STC_temptend_FAFWATER_PAC_zonal.nc","STC_temptend_FAFHEAT_PAC_zonal.nc","STC_temptend_FAFALL_PAC_zonal.nc","STC_temptend_flux-only_PAC_zonal.nc"]
filename2  = ["BSO_PAC_FAFSTRESS.nc","BSO_PAC_FAFWATER.nc","BSO_PAC_FAFHEAT.nc","BSO_PAC_FAFALL.nc","BSO_PAC_flux-only.nc"]
filename3  = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_FAFALL.nc","pot_rho_0_zonalmean_flux-only.nc"]
filename4  = ["MOC_PAC_FAFSTRESS.nc","MOC_PAC_FAFWATER.nc","MOC_PAC_FAFHEAT.nc","MOC_PAC_FAFALL.nc","MOC_PAC_flux-only.nc"]
filename5   = ["MLD_BSO_FAFSTRESS.nc","MLD_BSO_FAFWATER.nc","MLD_BSO_FAFHEAT.nc","MLD_BSO_FAFALL.nc","MLD_BSO_flux-only.nc"]


lat               = [None]*len(filename)
depth             = [None]*len(filename)
lat2              = [None]*len(filename)
depth2            = [None]*len(filename)

time              = [None]*len(filename)
temptend          = [None]*len(filename)
advection         = [None]*len(filename)
submeso           = [None]*len(filename)
neutral_gm        = [None]*len(filename)
diapycnal_mix     = [None]*len(filename)
isopycnal_mix     = [None]*len(filename)
swh               = [None]*len(filename)
residual          = [None]*len(filename)
super_residual    = [None]*len(filename)
eddy              = [None]*len(filename)
advection         = [None]*len(filename)
total             = [None]*len(filename)
unresolved        = [None]*len(filename)
vdiff             = [None]*len(filename)

latrho            = [None]*len(filename)
depthrho          = [None]*len(filename)
latrho2           = [None]*len(filename)
depthrho2         = [None]*len(filename)
bso               = [None]*len(filename)
potrho            = [None]*len(filename)

bso_interp        = [None]*len(exp)
bso_interp_rmean  = [None]*len(exp)
bso_rmean         = [None]*len(exp)

LAT      = [None]*len(exp)
DEPTH    = [None]*len(exp)
LAT2     = [None]*len(exp)
DEPTH2   = [None]*len(exp)
PMOC     = [None]*len(exp)
GMOC     = [None]*len(exp)
PMLD     = [None]*len(exp)


yt = 1e-12 #TW
t = np.arange(0,70)

tyear = 365.25 * 24.0 * 3600.0
dt = np.ones((len(t),50,88))*tyear

#---> Get the Volume Mean Tracers Anomalies
for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    print("Working on %s" % fn)
    file = nc.Dataset(fn)
    lat[i]               = file.variables['YT_OCEAN3_190'][:]
    depth[i]             = file.variables['ST_OCEAN'][:]
    temptend[i]          = np.squeeze(np.mean(file.variables['TEMPTEND_NO_MLD'][61:70,:,:],0))*yt
    advection[i]         = np.squeeze(np.mean(file.variables['ADVECTION_NO_MLD'][61:70,:,:],0))*yt
    submeso[i]           = np.squeeze(np.mean(file.variables['SUBMESO_NO_MLD'][61:70,:,:],0))*yt
    neutral_gm[i]        = np.squeeze(np.mean(file.variables['NEUTRAL_GM_NO_MLD'][61:70,:,:],0))*yt
    diapycnal_mix[i]     = np.squeeze(np.mean(file.variables['VDIFFUSE_DIFF_CBT_NO_MLD'][61:70,:,:],0))*yt
    isopycnal_mix[i]     = np.squeeze(np.mean(file.variables['NEUTRAL_DIFFUSION_NO_MLD'][61:70,:,:],0))*yt
    swh[i]              = np.squeeze(np.mean(file.variables['SWH_NO_MLD'][61:70,:,:],0))*yt
    file.close()

for i in range(len(filename)):
    residual[i]       = advection[i] + submeso[i] + neutral_gm[i]
    eddy[i]           =                submeso[i] + neutral_gm[i]
    super_residual[i] = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i]
    total[i]          = advection[i] + submeso[i] + neutral_gm[i] + isopycnal_mix[i] + diapycnal_mix[i] + swh[i]
    unresolved[i]     = temptend[i]  - total[i]
    vdiff[i]          = diapycnal_mix[i] + swh[i] + unresolved[i]

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
#    lat_bso[i]   = file.variables['Y'][:]
    bso[i]       = np.squeeze(file.variables['field'][:])
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename3[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    latrho[i]   = file.variables['YT_OCEAN'][:]
    depthrho[i] = file.variables['ST_OCEAN'][:]
    potrho[i]  = file.variables['POT_RHO_0_ZONALMEAN_PAC'][:]-1000.
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename4[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['GRIDLAT_T'][:] #YU_OCEAN'
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    PMOC[i]  = file.variables['PMOC'][:]
    #GMOC[i]  = file.variables['MOC'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir2,filename5[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    #LAT[i]    = file.variables['YT_OCEAN'][:]
    PMLD[i]   = file.variables['PMLD'][:]
    file.close()

####
N=3
for i in range(len(exp)):
    bso_rmean[i] = np.convolve(bso[i][:],np.ones(N)/N, mode='same') #2,

lat_interp = np.linspace(-90,90,300)
for i in range(len(exp)):
    bso_interp_rmean[i] = np.interp(lat_interp,LAT[i],bso_rmean[i])
####

#------------------------PLOTTING
#rc('figure', figsize=(8.27,11.69))
rc('figure', figsize=(11,8.27))

cmap2 = plt.get_cmap('bwr')

#cmap2.set_bad(color = '0.5', alpha = None)

tend_name           = ["(a) NET","ADV","EDDY","ISO","(b) vDIFF","(c) srADV"]
tend_name_fafstress = ["(d) NET","ADV","EDDY","ISO","(e) vDIFF","(f) srADV"]
tend_name_fafwater  = ["(g) NET","ADV","EDDY","ISO","(h) vDIFF","(i) srADV"]
tend_name_fafheat   = ["(j) NET","ADV","EDDY","ISO","(k) vDIFF","(l) srADV"]

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.1,.1)

clevs_moc = [-30,-20,-18,-16,-14,-12,-10,-5,-4,-2.5,-2,-1,0,1,2,2.5,4,5,10,12,14,16,18,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]

v = [-32,32,0,1000]

kmin = -.5; kmax = .5
clevs = np.arange(kmin,kmax+.1,.1)

for i in range(len(exp)-1):
    fig = plt.figure(i)
    fig.subplots_adjust(hspace=0.25,wspace=0.12)
    fig.tight_layout()
    
    fig.suptitle(exp[i],fontweight='normal',fontsize=20,x=.5,y=.95)

    subplots_adjust(wspace=None, hspace=.15)

    [lat2[i],depth2[i]]       = np.meshgrid(lat[i],depth[i])
    [latrho2[i],depthrho2[i]] = np.meshgrid(latrho[i],depthrho[i])
    [LAT2[i],DEPTH2[i]]       = np.meshgrid(LAT[i],DEPTH[i])

    ax = fig.add_subplot(2,3,1)
    cs  = plt.pcolormesh(lat2[i],depth2[i],temptend[i][:,:]-temptend[-1][:,:],shading='gouraud',cmap=cmap2)
    plt.clim(kmin,kmax)

    cc2 = plt.contour(LAT2[i],DEPTH2[i],PMOC[i],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    plt.plot(lat_interp,bso_interp_rmean[i][:],linestyle='solid',color='black',linewidth=1.5)
    plt.plot(LAT[i],PMLD[i][:],linestyle='solid',color='black',linewidth=1.5)

    if i==0: plt.title(tend_name_fafstress[0])
    elif i==1: plt.title(tend_name_fafwater[0])
    elif i==2: plt.title(tend_name_fafheat[0])

    plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

    plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
    plt.yticks([0,200,400,600,800,1000],[0,200,400,600,800,1000],fontsize=12)
    ax.set_ylabel('Depth [m]',fontsize=14)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    ax = fig.add_subplot(2,3,2)
    cs  = plt.pcolormesh(lat2[i],depth2[i],vdiff[i][:,:]-vdiff[-1][:,:],shading='gouraud',cmap=cmap2)
    plt.clim(kmin,kmax)

    cc2 = plt.contour(LAT2[i],DEPTH2[i],PMOC[i],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    plt.plot(lat_interp,bso_interp_rmean[i][:],linestyle='solid',color='black',linewidth=1.5)
    plt.plot(LAT[i],PMLD[i][:],linestyle='solid',color='black',linewidth=1.5)

    if i==0: plt.title(tend_name_fafstress[4])
    elif i==1: plt.title(tend_name_fafwater[4])
    elif i==2: plt.title(tend_name_fafheat[4])


    plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

    plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
    plt.yticks([0,200,400,600,800,1000],[],fontsize=12)
#    ax.set_ylabel('Depth [m]',fontsize=14)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    ax = fig.add_subplot(2,3,3)
    cs  = plt.pcolormesh(lat2[i],depth2[i],super_residual[i][:,:]-super_residual[-1][:,:],shading='gouraud',cmap=cmap2)
    plt.clim(kmin,kmax)

    cc2 = plt.contour(LAT2[i],DEPTH2[i],PMOC[i],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
    plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

    plt.plot(lat_interp,bso_interp_rmean[i][:],linestyle='solid',color='black',linewidth=1.5)
    plt.plot(LAT[i],PMLD[i][:],linestyle='solid',color='black',linewidth=1.5)

    if i==0: plt.title(tend_name_fafstress[5])
    elif i==1: plt.title(tend_name_fafwater[5])
    elif i==2: plt.title(tend_name_fafheat[5])

    plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

    plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
    plt.yticks([0,200,400,600,800,1000],[],fontsize=12)

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

    ax.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

    if i==2: 
        cbaxes = fig.add_axes([0.2, 0.42, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
        cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
        cbar.ax.tick_params(labelsize=12)
        cbar.ax.set_title("TW",fontsize=14,color='k')
    plt.savefig('STC_OHC_PAC_diag_tend_online_zonal_' + exp[i] + '.png',transparent = False,bbox_inches='tight',dpi=300)

#####control

kmin = -2; kmax = 2
clevs = np.arange(kmin,kmax+.1,1.)

clevs_moc = [-30,-20,-18,-16,-14,-12,-10,-5,-2.5,-2,-1,0,1,2,2.5,5,10,15,20,30]
clevs_rho = [24.5,25.0,25.5,26.0,26.6,27.0,27.5,27.75]

fig = plt.figure(100)
fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()

fig.suptitle(exp[-1],fontweight='normal',fontsize=20,x=.5,y=.95)

subplots_adjust(wspace=None, hspace=.15)

[lat2[-1],depth2[-1]]       = np.meshgrid(lat[-1],depth[-1])
[latrho2[-1],depthrho2[-1]] = np.meshgrid(latrho[-1],depthrho[-1])
[LAT2[-1],DEPTH2[-1]]       = np.meshgrid(LAT[-1],DEPTH[-1])

ax = fig.add_subplot(2,3,1)###
cs  = plt.pcolormesh(lat2[-1],depth2[-1],temptend[-1][:,:],shading='gouraud',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[-1],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(tend_name[0])

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,200,400,600,800,1000],[0,200,400,600,800,1000],fontsize=12)
ax.set_ylabel('Depth [m]',fontsize=14)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(2,3,2)###
cs  = plt.pcolormesh(lat2[-1],depth2[-1],vdiff[-1][:,:],shading='gouraud',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[-1],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(tend_name[4])

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5); plt.axvline(x=-33.5,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)

plt.yticks([0,200,400,600,800,1000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

ax = fig.add_subplot(2,3,3)###
cs  = plt.pcolormesh(lat2[-1],depth2[-1],super_residual[-1][:,:],shading='gouraud',cmap=cmap2)
plt.clim(kmin,kmax)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
cc2 = plt.contour(LAT2[-1],DEPTH2[-1],PMOC[-1],levels=clevs_moc,colors='gray',linestyles='solid',linewidths=1)
plt.clabel(cc2,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)

plt.plot(lat_interp,bso_interp_rmean[-1][:],linestyle='solid',color='black',linewidth=1.5)
plt.plot(LAT[-1],PMLD[-1][:],linestyle='solid',color='black',linewidth=1.5)

plt.title(tend_name[5])

plt.axvline(x=0.,color='k',linestyle='--',linewidth=1.5)

plt.xticks([-45,-30,-15,0,15,30,45],[-45,-30,-15,0,15,30,45],fontsize=12)
plt.yticks([0,200,400,600,800,1000],[],fontsize=12)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

ax.axis(v)
ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

cbaxes = fig.add_axes([0.2, 0.42, 0.6, 0.02]) #add_axes : [left, bottom, width, height]
cbar = plt.colorbar(cs,cax=cbaxes,ticks=clevs,extend='both',orientation="horizontal")
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_title("TW",fontsize=14,color='k')

#plt.show()
plt.savefig('STC_OHC_PAC_diag_tend_online_zonal_CTL.png',transparent = False, bbox_inches='tight',dpi=300)


