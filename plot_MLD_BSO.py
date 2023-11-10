#
import sys
import os
import numpy as np
import numpy.ma as ma
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc
from netCDF4 import Dataset

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'
#datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp        = ["Stress","Water","Heat","All","Control"]
filename   = ["MLD_BSO_FAFSTRESS.nc","MLD_BSO_FAFWATER.nc","MLD_BSO_FAFHEAT.nc","MLD_BSO_FAFALL.nc","MLD_BSO_flux-only.nc"]
filename2  = ["MOC_PAC_FAFSTRESS.nc","MOC_PAC_FAFWATER.nc","MOC_PAC_FAFHEAT.nc","MOC_PAC_FAFALL.nc","MOC_PAC_flux-only.nc"]
#filename2  = ["MOC_FAFSTRESS.nc","MOC_FAFWATER.nc","MOC_FAFHEAT.nc","MOC_FAFALL.nc","MOC_FAFSTRESSx2.nc","MOC_FAFHEATx2.nc","MOC_flux-only.nc"]
#filename3  = ["pot_rho_0_zonalmean_FAFSTRESS.nc","pot_rho_0_zonalmean_FAFWATER.nc","pot_rho_0_zonalmean_FAFHEAT.nc","pot_rho_0_zonalmean_FAFALL.nc","pot_rho_0_zonalmean_FAFSTRESSx2.nc","pot_rho_0_zonalmean_FAFHEATx2.nc","pot_rho_0_zonalmean_flux-only.nc"]

LAT      = [None]*len(exp)
DEPTH    = [None]*len(exp)
LAT2     = [None]*len(exp)
DEPTH2   = [None]*len(exp)
POTRHO   = [None]*len(exp)
PMLD     = [None]*len(exp)
PMOC     = [None]*len(exp)
GMLD     = [None]*len(exp)
GMOC     = [None]*len(exp)
bso_pac  = [None]*len(exp)
bso_glb  = [None]*len(exp)

POTRHO_glb = [None]*len(exp)
POTRHO_pac = [None]*len(exp)

bso_pac_interp       = [None]*len(exp)
bso_pac_interp_rmean = [None]*len(exp)
bso_pac_rmean        = [None]*len(exp)

#---> Get the Data
for i in range(len(exp)):
    fn = os.path.join(datadir,filename[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]    = file.variables['YT_OCEAN'][:]
    PMLD[i]   = file.variables['PMLD'][:]
    GMLD[i]   = file.variables['MLD'][:]
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Opening %s" % fn)
    file = nc.Dataset(fn)
    LAT[i]   = file.variables['GRIDLAT_T'][:]
    #LAT[i]   = file.variables['YU_OCEAN'][:]
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    PMOC[i]  = np.squeeze(file.variables['PMOC'][:])
    file.close()

#for i in range(len(exp)):
#    fn = os.path.join(datadir,filename3[i])
#    print("Opening %s" % fn)
#    file = nc.Dataset(fn)
#    LAT[i]   = file.variables['YT_OCEAN'][:]
#    DEPTH[i] = file.variables['ST_OCEAN'][:]
#    POTRHO_glb[i]  = file.variables['POT_RHO_0_ZONALMEAN_GLB'][:]-1000.
#    POTRHO_pac[i]  = file.variables['POT_RHO_0_ZONALMEAN_PAC'][:]-1000.
#    file.close()

#--calcule of base of the shallow overturn

arcname  = ["FAFSTRESS","FAFWATER","FAFHEAT","FAFALL","flux-only"]

ind_pac = [None]*len(LAT[i])
for i in range(len(exp)):
    for j in range(len(LAT[i])):
        pmocj = PMOC[i][:,j]
        for k in range(2,38): #len(pmocj)):
            if LAT[i][j]>=0.0:
                if i == 4: #control
                    if pmocj[k]<=.5 and pmocj[k]>=-1.:
                        ind_pac[j]=np.mean(DEPTH[i][k:k+2])
                        break
                    else:
                        ind_pac[j]=ind_pac[j-1]
                else: #nota que se uso el mismo condicional
                    if pmocj[k]<=.5 and pmocj[k]>=0.: #funciona relativamente bien para todos 
                        ind_pac[j]=np.mean(DEPTH[i][k:k+2])
                        break
                    else:
                        ind_pac[j]=ind_pac[j-1]
            elif LAT[i][j]<0.0:
                if pmocj[k]<=-15 and pmocj[k]>=-18:                
                    ind_pac[j]=np.mean(DEPTH[i][k:k+2])

    bso_pac[i] = ind_pac
    for j in range(len(bso_pac[i])):
        if LAT[i][j]<=.85 and LAT[i][j]>= -.85:
            bso_pac[i][j] = PMLD[i][j]
        elif LAT[i][j]>=30. or LAT[i][j]<= -33.5:
            bso_pac[i][j] = PMLD[i][j]
        else:
            bso_pac[i][j] = bso_pac[i][j]
    ind_pac = [None]*len(LAT[i])

for i in range(len(exp)):
    for j in range(len(bso_pac[i])):
        if bso_pac[i][j]==None:
            bso_pac[i][j]= bso_pac[i][j-1]

#### data    
    #root_grp = Dataset('/home/clima-archive2/rfarneti/RENE/DATA/BSO_PAC_'+arcname[i]+'.nc', 'w', format='NETCDF4')
    root_grp = Dataset('/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA/'+arcname[i]+'.nc', 'w', format='NETCDF4')
    root_grp.description = 'Base_Shallow_Overturn: closed current lines'
    root_grp.createDimension('x',1)
    root_grp.createDimension('y',200)
    x      = root_grp.createVariable('x', 'f4', ('x',))
    y      = root_grp.createVariable('y', 'f4', ('y',))
    field    = root_grp.createVariable('field', 'f8', ('y','x'))
    y[:]     = LAT[i]
    field[:] = bso_pac[i]
    root_grp.close()
####

N=3
for i in range(len(exp)):
    bso_pac_rmean[i] = np.convolve(bso_pac[i],np.ones(N)/N, mode='same') #2,

lat_interp = np.linspace(-90,90,300)
for i in range(len(exp)):
    bso_pac_interp_rmean[i] = np.interp(lat_interp,LAT[i],bso_pac_rmean[i])
###
###

#------------------------PLOTTING
#rc('figure', figsize=(11.69,8.27))
rc('figure', figsize=(8.2,11.69))

##-------------ZONAL MEAN
letter = ["(a)","(b)","(c)","(d)","(e)","(f)","(h)","(g)"]
colors = ['black','blue','red','green','red','gray']
styles = ['solid','solid','solid','solid','dashed','solid']

clevs = [-30,-20,-18,-16,-14,-12,-10,-5,-4,-2.5,-2,-1,0,1,2,2.5,4,5,10,12,14,16,18,20,30]

[LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])

v= [-32,32,0,1000]
#v= [-35,35,0,50]

fig = plt.figure(2)
fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()
subplots_adjust(wspace=None, hspace=.15)

for i in range(len(exp)-1):
    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(3,2,i+1)
    cc = plt.contour(LAT2[i],DEPTH2[i],PMOC[i],levels=clevs,colors='black',linestyles='solid',linewidths=.5)
    plt.clabel(cc,inline=1,inline_spacing=-5,fmt='%1.1f',fontsize=8)
    ax.plot(lat_interp,bso_pac_interp_rmean[i][:],linestyle='solid',color='black',linewidth=2)
    ax.plot(lat_interp,bso_pac_interp_rmean[-1][:],linestyle='solid',color=[.4,.4,.4],linewidth=2)
#    ax.plot(LAT[i],bso_pac[i][:],linestyle='solid',color='black',linewidth=2)
#    ax.plot(LAT[i],bso_pac[-1][:],linestyle='solid',color=[.4,.4,.4],linewidth=2)

    title(exp[i])
    plt.plot(LAT[-1],PMLD[i][:],linestyle='solid',color='red',linewidth=1.5)

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-45,-30,-15,0,15,30,45],["45S","30S","15S",0,"15N","30N","45N"],fontsize=12)
        #plt.xticks([-35,-32,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,32,35],[-35,-32,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,32,35],fontsize=12)
    else:
        #plt.xticks([-35,-32,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,32,35],[-35,-32,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,32,35],fontsize=12)
       plt.xticks([-45,-30,-15,0,15,30,45],[])
    if (i==0 or i==2):
        plt.yticks([0,200,400,600,800,1000],[0,200,400,600,800,1000],fontsize=12)
        #lt.yticks([0,100,200,300,400,500,600,700,800,900,1000],[0,100,200,300,400,500,600,700,800,900,1000],fontsize=12)
        ax.set_ylabel('Depth [m]',fontsize=14)
    else:
        plt.yticks([0,200,400,600,800,1000],[])
    
    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    plt.axis(v)
    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis
    plt.axvline(x=0.0,color='k',linestyle='--',linewidth=2.0) #includes zero line

#plt.savefig('BSO_pacific.png',transparent = True, bbox_inches='tight',dpi=600)
#plt.show()

