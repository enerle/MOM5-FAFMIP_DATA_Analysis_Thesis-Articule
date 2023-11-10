import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir  = '/home/netapp-clima-users1/rnavarro/ANALYSIS/BLAKER/DATA'
datadir  = '/home/clima-archive2/rfarneti/RENE/DATA/'

exp       = ["Stress","Water","Heat","All","control"]
filename1 = ["STC_FAFSTRESS.nc","STC_FAFWATER.nc","STC_FAFHEAT.nc","STC_FAFALL.nc","STC_flux-only.nc"]
filename2 = ["STC_RHO_FAFSTRESS.nc","STC_RHO_FAFWATER.nc","STC_RHO_FAFHEAT.nc","STC_RHO_FAFALL.nc","STC_RHO_flux-only.nc"]
filename3 = ["SST_SSS_9S9N_timeseries_FAFSTRESS.nc","SST_SSS_9S9N_timeseries_FAFWATER.nc","SST_SSS_9S9N_timeseries_FAFHEAT.nc","SST_SSS_9S9N_timeseries_FAFALL.nc","SST_SSS_9S9N_timeseries_flux-only.nc","SST_SSS_9S9N_timeseries_FAFHEAT_FAFSTRESS.nc"]

conv        = [None]*len(exp)
conv_int    = [None]*len(exp)
convrho     = [None]*len(exp)
convrho_int = [None]*len(exp)
sst         = [None]*len(exp)
time        = [None]*len(exp)
time2       = [None]*len(exp)

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    conv[i] = np.squeeze(file.variables['CONV'][:])
    conv_int[i] = np.squeeze(file.variables['CONV_INT'][:])
    file.close()

for i in range(len(exp)):
    fn = os.path.join(datadir,filename2[i])
    print("Working on ", fn)
    file = nc.Dataset(fn)
    convrho[i] = np.squeeze(file.variables['CONVRHO'][:])
    convrho_int[i] = np.squeeze(file.variables['CONVRHO_INT'][:])
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
    ax.plot(time[i],conv[i]-conv[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Total convergence",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.axis([0,70,-4,4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],conv_int[i]-conv_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("Interior convergence",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis([0,70,-4,4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
#plt.savefig('STC-conv-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(2)

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
ax.axis([0,70,-4,4])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
#plt.savefig('STC-convrho-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

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

ctot = stats.pearsonr(conv[-1][:],sst[-1][:])
cint = stats.pearsonr(conv_int[-1][:],sst[-1][:])
crhotot = stats.pearsonr(convrho[-1][:],sst[-1][:])
crhoint = stats.pearsonr(convrho_int[-1][:],sst[-1][:])

#################
##--Only controls
#################

fig = plt.figure(3)

ax1 = fig.add_subplot(2,1,1)
ax1.plot(time[-1],conv[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx() 
ax2.plot(time[-1],sst[-1],color='red',linestyle='solid',linewidth=2.0)

ax1.set_ylabel("[Sv]",color='black',fontsize=16)
ax1.axis([0,70,52,55])
ax1.tick_params(axis='y',labelcolor='black',labelsize=16)

ax2.set_ylabel("[$C^o$]",color='red',fontsize=16)
ax2.axis([0,70,27,27.5])
ax2.tick_params(axis='y',labelcolor='red',labelsize=16)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])
plt.title("Total convergence and mean tropical SST (Corr = %.2f " %ctot[0] + "p-value = %.2f )" %ctot[1],fontsize=16)

ax1 = fig.add_subplot(2,1,2)
ax1.plot(time[-1],conv_int[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx()
ax2.plot(time[-1],sst[-1],color='red',linestyle='solid',linewidth=2.0)

ax1.set_ylabel("[Sv]",color='black',fontsize=16)
ax1.axis([0,70,12,14])
ax1.tick_params(axis='y',labelcolor='black',labelsize=16)

ax2.set_ylabel("[$C^o$]",color='red',fontsize=16)
ax2.axis([0,70,27,27.5])
ax2.tick_params(axis='y',labelcolor='red',labelsize=16)

ax1.spines['top'].set_linewidth(2);  ax1.spines['bottom'].set_linewidth(2)
ax1.spines['left'].set_linewidth(2); ax1.spines['right'].set_linewidth(2)
ax1.xaxis.set_tick_params(width=2);  ax1.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[0,10,20,30,40,50,60,70])
plt.title("Interior convergence and mean tropical SST (Corr = %.2f " %cint[0] + "p-value = %.2f )" %cint[1],fontsize=16)

ax1.set_xlabel("Time [years]",fontsize=16)
ax1.tick_params(axis='x',labelcolor='black',labelsize=16)
plt.xticks(fontsize=16)

#plt.show()
#plt.savefig('STC-conv-timeseries_CTL.png',transparent = True, bbox_inches='tight',dpi=600)

fig = plt.figure(4)

ax1 = fig.add_subplot(2,1,1)
ax1.plot(time[-1],convrho[-1],color='black',linestyle='solid',linewidth=2.0)
ax2 = ax1.twinx()
ax2.plot(time[-1],sst[-1],color='red',linestyle='solid',linewidth=2.0)

ax1.set_ylabel("[Sv]",color='black',fontsize=16)
ax1.axis([0,70,41,45])
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
ax1.axis([0,70,9,12])
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

plt.show()
#plt.savefig('STC-convrho-timeseries_CTL.png',transparent = True, bbox_inches='tight',dpi=600)
