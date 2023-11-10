#
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

datadir = '/home/clima-archive2/rfarneti/RENE/DATA'

exp      = ["Stress","Water","Heat","All","CTL"]
filename = ["pot_rho_2_zonalmean_FAFSTRESS.nc","pot_rho_2_zonalmean_FAFWATER.nc","pot_rho_2_zonalmean_FAFHEAT.nc","pot_rho_2_zonalmean_FAFALL.nc","pot_rho_2_zonalmean_flux-only.nc"]

LAT    = [None]*len(exp)
DEPTH  = [None]*len(exp)
LAT2   = [None]*len(exp)
DEPTH2 = [None]*len(exp)
POTRHO = [None]*len(exp)

for i in range(len(filename)):
    fn = os.path.join(datadir,filename[i])
    file = nc.Dataset(fn)
    print("--Working on %s" % fn)
    LAT[i] = file.variables['YT_OCEAN'][:]
    DEPTH[i] = file.variables['ST_OCEAN'][:]
    POTRHO[i] = file.variables['POT_RHO_2_ZONALMEAN_GLB'][:,:]-1000
    file.close()

#------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

#colors = ['black','blue','red','green','gray']
colors = ['black','black','black','black','gray']

#clevs = np.arange(-1,1,.1)
clevs = np.arange(34.5,37.5,.5)
#clevs = np.arange(22.,28.,.5)

v= [-90,90,0,4000]

fig = plt.figure(1)
fig.subplots_adjust(top=0.95,bottom=0.12,hspace=0.25,wspace=0.12)

for i in range(len(exp)-1):

    [LAT2[i],DEPTH2[i]] = np.meshgrid(LAT[i],DEPTH[i])
    ax = fig.add_subplot(3,2,i+1)

    cc = plt.contour(LAT[-1],DEPTH[-1],POTRHO[-1],\
            levels=clevs,colors=colors[-1],linestyles='solid',linewidths=1)

    plt.clabel(cc,inline=False, inline_spacing=0,fmt='%1.2f', fontsize=10)

    cc = plt.contour(LAT2[i],DEPTH2[i],POTRHO[i],\
            levels=clevs,colors=colors[i],linestyles='solid',linewidths=1)
   
    plt.axis(v)
    
    plt.title('%s' % (exp[i]), fontsize=16, color='k')

    ##-----------for beauty
    if (i>=2):
        plt.xticks([-90,-60,-30,0,30,60,90],['90S','60S','30S','0','30N','60N','90N'],fontsize=12)
    else:
        plt.xticks([-90,-60,-30,0,30,60,90],[])
    if (i==0 or i==2 or i==4):
        plt.yticks([0,1000,2000,3000,4000,5000],[0,1000,2000,3000,4000,5000],fontsize=12)
        ax.set_ylabel('Depth (m)',fontsize=14)
    else:
        plt.yticks([0,1000,2000,3000,4000,5000],[])

    ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)
    ##-----------

    ax.set_ylim(ax.get_ylim()[::-1]) #reverse the y-axis

#plt.show()
plt.savefig('potrho2_zonalmean.png',transparent = True, bbox_inches='tight',dpi=600)

