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

#exp       = ["Stress","Water","Heat","All","flux-only"]
#filename1 = ["curl_FAFSTRESS_PAC.nc","curl_FAFWATER_PAC.nc","curl_FAFHEAT_PAC.nc","curl_FAFALL_PAC.nc","curl_flux-only_PAC.nc"]
#filename2 = ["zonalmean_curl_FAFSTRESS_PAC.nc","zonalmean_curl_FAFWATER_PAC.nc","zonalmean_curl_FAFHEAT_PAC.nc","zonalmean_curl_FAFALL_PAC.nc","zonalmean_curl_flux-only_PAC.nc"]

exp       = ["Stress","flux-only"]
filename1 = ["curl_FAFSTRESS_PAC.nc","curl_flux-only_PAC.nc"]
filename2 = ["zonalmean_curl_FAFSTRESS_PAC.nc","zonalmean_curl_flux-only_PAC.nc"]

curl       = [None]*len(exp)
curl_zonal = [None]*len(exp)
lon        = [None]*len(exp)
lat        = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename1[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    lon[i]    = file.variables['XU_OCEAN'][:]
    lat[i]    = file.variables['YU_OCEAN'][:]
#    lon[i]    = file.variables['GRIDLON_C'][:]
#    lat[i]    = file.variables['GRIDLAT_C'][:]
#    lon[i]    = file.variables['GRIDLON_T'][:]
#    lat[i]    = file.variables['GRIDLAT_T1_180'][:]
    curl[i]   = file.variables['CURL_GLB'][:,:]*1e7
#curl[i]   = np.mean(file.variables['CURL'][:,:],0)*1e7
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    lat[i]          = file.variables['YU_OCEAN'][:]
#    lat[i]          = file.variables['YU_OCEAN1_180'][:]
#    lat[i]          = file.variables['GRIDLAT_C'][:]
#    lat[i]          = file.variables['GRIDLAT_T1_180'][:]
    curl_zonal[i]   = file.variables['CURL_PAC'][:]*1e7
    file.close()

#------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

cmap2 = plt.get_cmap('bwr')
####cmap2.set_bad(color = '0.5', alpha = None)
cmap2.set_bad(color='0.7',alpha=1.)

kmin = -2; kmax = 2
clevs  = [-2,-1.5,-1,-.5,-.25,.25,.5,1,1.5,2]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

ax  = fig.add_subplot(3,1,1)
#cs  = plt.pcolormesh(lon[-1],lat[-1],curl[-1][:,:],levels=clevs,shading='gouraud',cmap=cmap2)
cs  = plt.contourf(curl[-1][:,:],cmap=cmap2,levels=clevs,extend='both')
plt.clim(kmin,kmax)

plt.title('%s' % (exp[-1]),fontsize=14,color='k')

plt.xticks([]); plt.yticks([])
    
ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)    
ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

cbar = plt.colorbar(cs,ticks=clevs,extend='both',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_title("kg m$^{-2}$ s$^{-2}$ 10$^7$",fontsize=12)

#####

#kmin = -.5; kmax = .5
#clevs  = [-.5,-.4,-0.3,-0.2,-.1,-0.05,0.05,0.1,0.2,0.3,.4,.5]
kmin = -.2; kmax = .2
clevs  = [-0.2,-.15,-.1,-0.05,0.05,0.1,.15,0.2]

ax  = fig.add_subplot(3,1,2)
cs  = plt.contourf(curl[0][:,:]-curl[-1][:,:],cmap=cmap2,levels=clevs,extend='both')
plt.clim(kmin,kmax)

plt.title('%s' % (exp[0]),fontsize=14,color='k')

plt.xticks([]); plt.yticks([])

ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

#Changes in colorbar
cbar = plt.colorbar(cs,ticks=clevs,extend='both',orientation="vertical",fraction=.1)
cbar.ax.tick_params(labelsize=12)
cbar.ax.set_title("kg m$^{-2}$ s$^{-2}$ 10$^7$",fontsize=12)

#plt.show()
#plt.savefig('test_21nov.png',transparent = True, bbox_inches='tight',dpi=600)

##-------------ZONAL MEAN
colors = ['black','red','gray']
styles = ['solid','solid','solid']

fig = plt.figure(2)
ax = fig.add_subplot(1,1,1)

ax.plot(lat[-1],curl_zonal[-1][:],linestyle='solid',color='gray',linewidth=2.0,label='control')
ax.plot(lat[0],curl_zonal[0][:],linestyle='solid',color='black',linewidth=2.0,label='faf-stress')
ax.plot(lat[-1],10*(curl_zonal[0][:]-curl_zonal[-1][:]),linestyle='solid',color='red',linewidth=2.0,label='anom.*10')

####
ax.spines['top'].set_linewidth(2); ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

ax.set_ylabel("kg m$^{-2}$ s$^{-2}$ 10$^7$",fontsize=16)
#ax.set_ylim(kmin,kmax)
ax.legend(loc=4,fontsize=16)

ax.axis([-40,60,-1.5,1.5])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
plt.xticks([-40,-30,-20,-10,0,10,20,30,40,50,60],['40S','30S','20S','10S','0','10','20N','30N','40N','50N','60N'],fontsize=16)

#plt.show()
plt.savefig('PAC_curl_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

