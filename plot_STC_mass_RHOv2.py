import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA/'

exp       = ["Stress","Water","Heat","All","flux-only"]
filename1 = ["STC_RHOLEVELS_FAFSTRESS.nc","STC_RHOLEVELS_FAFWATER.nc","STC_RHOLEVELS_FAFHEAT.nc","STC_RHOLEVELS_FAFALL.nc","STC_RHOLEVELS_flux-only.nc"]
filename2 = ["STC_RHO_v2_FAFSTRESS_v2.nc","STC_RHO_v2_FAFWATER_v2.nc","STC_RHO_v2_FAFHEAT_v2.nc","STC_RHO_v2_FAFALL_v2.nc","STC_RHO_v2_flux-only_v2.nc"]
filename3 = ["SST_SSS_9S9N_timeseries_FAFSTRESS.nc","SST_SSS_9S9N_timeseries_FAFWATER.nc","SST_SSS_9S9N_timeseries_FAFHEAT.nc","SST_SSS_9S9N_timeseries_FAFALL.nc","SST_SSS_9S9N_timeseries_flux-only.nc"]

trans9n_rholev          = [None]*len(exp)
trans9s_rholev          = [None]*len(exp)
trans9n_int_rholev      = [None]*len(exp)
trans9s_int_rholev      = [None]*len(exp)
trans9n_rholev_mean     = [None]*len(exp)
trans9s_rholev_mean     = [None]*len(exp)
trans9n_int_rholev_mean = [None]*len(exp)
trans9s_int_rholev_mean = [None]*len(exp)
convrho                 = [None]*len(exp)
convrho_int             = [None]*len(exp)
sst                     = [None]*len(exp)
time                    = [None]*len(exp)

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    trans9n_rholev[i]     = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9N'][:])
    trans9s_rholev[i]     = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9S'][:])
    trans9n_int_rholev[i] = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9N_INT'][:])
    trans9s_int_rholev[i] = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9S_INT'][:])
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Working on ", fn)
    file = nc.Dataset(fn)
    convrho[i] = np.squeeze(file.variables['CONVRHO'][:])
    convrho_int[i] = np.squeeze(file.variables['CONVRHO_INT'][:])
    trans9n_rholev_mean[i]     = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9N_MEAN'][:])
    trans9s_rholev_mean[i]     = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9S_MEAN'][:])
    trans9n_int_rholev_mean[i] = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9N_INT_MEAN'][:])
    trans9s_int_rholev_mean[i] = np.squeeze(file.variables['RHOLEVEL_TRANSRHO9S_INT_MEAN'][:])
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename3[i])
    print("Working on ", fn)
    file = nc.Dataset(fn)
    sst[i] = np.squeeze(file.variables['SSTT'][:])
    file.close()

##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(11.69,8.27))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

fig = plt.figure(1)

ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],convrho[i]-convrho[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Total convergence",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
#ax.axis([0,70,-6,6])
ax.axis([0,70,-4,4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],convrho_int[i]-convrho_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("Interior convergence",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
#ax.axis([0,70,-6,6])
ax.axis([0,70,-4,4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('STC-convrho-timeseries_v2_revisited.png',transparent = True, bbox_inches='tight',dpi=600)


#################
## -- correlation analysis
################

##to note this is requiere if no np.squeeze is used
#x1=np.array(conv[-1][:], dtype=np.float); x1=x1.flatten()
#x2=np.array(conv[-1][:], dtype=np.float); x2=x2.flatten()
#print(stats.pearsonr(x1,x2))
#with np.squeeze():
#print(stats.pearsonr(np.array(conv[-1][:]),np.array(conv[-1][:])))
#print(stats.pearsonr(conv[-1][:],conv[-1][:]))

crhotot = stats.pearsonr(convrho[-1][:],sst[-1][:])
crhoint = stats.pearsonr(convrho_int[-1][:],sst[-1][:])

#################
##--Only controls
#################

fig = plt.figure(2)

ax1 = fig.add_subplot(2,1,1)
ax1.plot(time[-1],convrho[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx()
ax2.plot(time[-1],sst[-1],color='red',linestyle='solid',linewidth=2.0)

plt.xticks([0,10,20,30,40,50,60,70],[])
ax1.set_ylabel("[Sv]",color='black',fontsize=16)
ax1.axis([0,70,35,40])
ax1.tick_params(axis='y',labelcolor='black',labelsize=16)

ax2.set_ylabel("[$^oC$]",color='red',fontsize=16)
ax2.axis([0,70,27,27.5])
ax2.tick_params(axis='y',labelcolor='red',labelsize=16)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])
plt.title("Total convergence and mean tropical SST (Corr = %.2f " %crhotot[0] + "p-value = %.2f )" %crhotot[1],fontsize=16)

ax1 = fig.add_subplot(2,1,2)
ax1.plot(time[-1],convrho_int[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx()
ax2.plot(time[-1],sst[-1],color='red',linestyle='solid',linewidth=2.0)

ax1.set_ylabel("[Sv]",color='black',fontsize=16)
ax1.axis([0,70,8,9])
ax1.tick_params(axis='y',labelcolor='black',labelsize=16)

ax2.set_ylabel("[$^oC$]",color='red',fontsize=16)
ax2.axis([0,70,27,27.5])
ax2.tick_params(axis='y',labelcolor='red',labelsize=16)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70])
plt.title("Interior convergence and mean tropical SST (Corr = %.2f " %crhoint[0] + "p-value = %.2f )" %crhoint[1],fontsize=16)

ax1.set_xlabel("Time [years]",fontsize=16)
ax1.tick_params(axis='x',labelcolor='black',labelsize=16)
plt.xticks(fontsize=16)

#plt.show()
plt.savefig('STC-convrho-timeseries_CTL_v2_revisited.png',transparent = True, bbox_inches='tight',dpi=600)

##-profundidad de integracion

fig = plt.figure(3)

ax = fig.add_subplot(2,2,1)
for i in range(len(exp)):
    ax.plot(time[i],trans9n_rholev[i],color=colors[i],linestyle='solid',linewidth=2.0, label = exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])
plt.yticks([1036,1035,1034,1033,1032],[1036,1035,1034,1033,1032])

plt.title("Total transport $9^o$N",fontsize=16)
ax.set_ylabel("$\\rho_{pot}$ [$Kg/m^{3}$]",fontsize=16)
ax.axis([0,70,1036,1032])

plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,2,2)
for i in range(len(exp)):
    ax.plot(time[i],trans9n_int_rholev[i],color=colors[i],linestyle='solid',linewidth=2.0, label = exp[i])
###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])
plt.yticks([1036,1035,1034,1033,1032],[])

plt.title("Interior transport $9^o$N",fontsize=16)
ax.axis([0,70,1036,1032])

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,2,3)
for i in range(len(exp)):
    ax.plot(time[i],trans9s_rholev[i],color=colors[i],linestyle='solid',linewidth=2.0)

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70])
plt.yticks([1036,1035,1034,1033,1032],[1036,1035,1034,1033,1032])

ax.set_ylabel("$\\rho_{pot}$ [$Kg/m^{3}$]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
plt.title("Total transport $9^o$S",fontsize=16)
ax.axis([0,70,1036,1032])

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,2,4)
for i in range(len(exp)):
    ax.plot(time[i],trans9s_int_rholev[i],color=colors[i],linestyle='solid',linewidth=2.0,label = exp[i])

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70])
plt.yticks([1036,1035,1034,1033,1032],[])

ax.set_xlabel("Time [years]",fontsize=16)
plt.title("Interior transport $9^o$S",fontsize=16)
ax.legend(loc=4,ncol=2, fontsize=16)
ax.axis([0,70,1036,1032])

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('STC-trans_rholev.png',transparent = True, bbox_inches='tight',dpi=600)

###table of density levels

print('TRANSIENT CHANGE TABLES (included control values)')

print("& exp & 9N tot & 9S tot & 9N int & 9S int")
print("\centering Stress"  + " & %.2f "  %trans9n_rholev_mean[0] + " & %.2f " %trans9s_rholev_mean[0] + " & %.2f " %trans9n_int_rholev_mean[0] + " & %.2f " %trans9s_int_rholev_mean[0]) 
print("\centering Water"   + " & %.2f "  %trans9n_rholev_mean[1] + " & %.2f " %trans9s_rholev_mean[1] + " & %.2f " %trans9n_int_rholev_mean[1] + " & %.2f " %trans9s_int_rholev_mean[2])        
print("\centering Heat"    +  " & %.2f " %trans9n_rholev_mean[2] + " & %.2f " %trans9s_rholev_mean[2] + " & %.2f " %trans9n_int_rholev_mean[2] + " & %.2f " %trans9s_int_rholev_mean[2])
print("\centering All"     + " & %.2f "  %trans9n_rholev_mean[3] + " & %.2f " %trans9s_rholev_mean[3] + " & %.2f " %trans9n_int_rholev_mean[3] + " & %.2f " %trans9s_int_rholev_mean[3])
print("\centering Control" + " & %.2f "  %trans9n_rholev_mean[-1] + " & %.2f " %trans9s_rholev_mean[-1] + " & %.2f " %trans9n_int_rholev_mean[-1] + " & %.2f " %trans9s_int_rholev_mean[-1])

