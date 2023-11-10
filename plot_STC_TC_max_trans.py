import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp       = ["Stress","Water","Heat","All","control"]
filename1 = ["STC_max_trans_FAFSTRESS_v2.nc","STC_max_trans_FAFWATER_v2.nc","STC_max_trans_FAFHEAT_v2.nc","STC_max_trans_FAFALL_v2.nc","STC_max_trans_flux-only_v2.nc"]

time                 = [None]*len(exp)
trans_tc_north          = [None]*len(exp)
trans_tc_south          = [None]*len(exp)
trans_tc_north_mean     = [None]*len(exp)
trans_tc_south_mean     = [None]*len(exp)

trans_stc_north      = [None]*len(exp)
trans_stc_south      = [None]*len(exp)
trans_stc_north_mean = [None]*len(exp)
trans_stc_south_mean = [None]*len(exp)

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i] = file.variables['TIME'][:]/365 -2188.0
    trans_tc_north[i]  = abs(file.variables['TRANS_TC_NORTH'][:])
    trans_tc_south[i]  = abs(file.variables['TRANS_TC_SOUTH'][:])
    trans_stc_north[i] = abs(np.squeeze(file.variables['TRANS_STC_NORTH'][:]))
    trans_stc_south[i] = abs(np.squeeze(file.variables['TRANS_STC_SOUTH'][:]))
    file.close()

for i in range(len(exp)):
    trans_tc_north_mean[i]  = np.mean(trans_tc_north[i][61:70])   
    trans_tc_south_mean[i]  = np.mean(trans_tc_south[i][61:70])
    trans_stc_north_mean[i] = np.mean(trans_stc_north[i][61:70])
    trans_stc_south_mean[i] = np.mean(trans_stc_south[i][61:70])


##------------------------PLOTTING
#rc('text', usetex=True)
rc('figure', figsize=(8,8))

colors = ['black','blue','red','green','gray']
styles = ['solid','solid','solid','solid','solid']

v = [0,70,-5,5]

fig = plt.figure(1)

ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(time[-1],trans_tc_north[i]-trans_tc_north[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("North",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis(v)

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],trans_tc_south[i]-trans_tc_south[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("South",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
#ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis(v)

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('Tropical_cell-maxtrans-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

v = [0,70,-1.5,1.5]

fig = plt.figure(2)

ax = fig.add_subplot(2,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],trans_stc_north[i]-trans_stc_north[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("North",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis(v)

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(2,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],trans_stc_south[i]-trans_stc_south[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("South",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
#ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis(v)

#plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('SubTropical_cell-maxtrans-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

print('-----------------------------------')
print('TRANSIENT CHANGE TABLES (tropical cell)')
print('-----------------------------------')

print("& var & ctl & stress & water & heat & all ")
print("\centering $Max. trans (HN)$" + " & %.2f " %(trans_tc_north_mean[-1]) + " & %.2f " %(trans_tc_north_mean[0]-trans_tc_north_mean[-1]) + " & %.2f " %(trans_tc_north_mean[1]-trans_tc_north_mean[-1]) + " & %.2f " %(trans_tc_north_mean[2]-trans_tc_north_mean[-1]) + " & %.2f " %(trans_tc_north_mean[3]-trans_tc_north_mean[-1]))
print("\centering $Max. trans (HS)$" + " & %.2f " %(trans_tc_south_mean[-1]) + " & %.2f " %(trans_tc_south_mean[0]-trans_tc_south_mean[-1]) + " & %.2f " %(trans_tc_south_mean[1]-trans_tc_south_mean[-1]) + " & %.2f " %(trans_tc_south_mean[2]-trans_tc_south_mean[-1]) + " & %.2f " %(trans_tc_south_mean[3]-trans_tc_south_mean[-1]))

print("& var & ctl & stress & water & heat & all ")
print("\centering $Max. trans (HN)$" + " & " + " & %.2f " %(((trans_tc_north_mean[0]/trans_tc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_tc_north_mean[1]/trans_tc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_tc_north_mean[2]/trans_tc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_tc_north_mean[3]/trans_tc_north_mean[-1])-1)*100.))
print("\centering $Max. trans (HS)$" + " & " + " & %.2f " %(((trans_tc_south_mean[0]/trans_tc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_tc_south_mean[1]/trans_tc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_tc_south_mean[2]/trans_tc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_tc_south_mean[3]/trans_tc_south_mean[-1])-1)*100))

print('-----------------------------------')
print('TRANSIENT CHANGE TABLES (STC)')
print('-----------------------------------')

print("& var & ctl & stress & water & heat & all ")
print("\centering $Max. trans (HN)$" + " & %.2f " %(trans_stc_north_mean[-1]) + " & %.2f " %(trans_stc_north_mean[0]-trans_stc_north_mean[-1]) + " & %.2f " %(trans_stc_north_mean[1]-trans_stc_north_mean[-1]) + " & %.2f " %(trans_stc_north_mean[2]-trans_stc_north_mean[-1]) + " & %.2f " %(trans_stc_north_mean[3]-trans_stc_north_mean[-1]))
print("\centering $Max. trans (HS)$" + " & %.2f " %(trans_stc_south_mean[-1]) + " & %.2f " %(trans_stc_south_mean[0]-trans_stc_south_mean[-1]) + " & %.2f " %(trans_stc_south_mean[1]-trans_stc_south_mean[-1]) + " & %.2f " %(trans_stc_south_mean[2]-trans_stc_south_mean[-1]) + " & %.2f " %(trans_stc_south_mean[3]-trans_stc_south_mean[-1]))

print("& var & ctl & stress & water & heat & all ")
print("\centering $Max. trans (HN)$" + " & " + " & %.2f " %(((trans_stc_north_mean[0]/trans_stc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_stc_north_mean[1]/trans_stc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_stc_north_mean[2]/trans_stc_north_mean[-1])-1)*100.) + " & %.2f " %(((trans_stc_north_mean[3]/trans_stc_north_mean[-1])-1)*100.))
print("\centering $Max. trans (HS)$" + " & " + " & %.2f " %(((trans_stc_south_mean[0]/trans_stc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_stc_south_mean[1]/trans_stc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_stc_south_mean[2]/trans_stc_south_mean[-1])-1)*100) + " & %.2f " %(((trans_stc_south_mean[3]/trans_stc_south_mean[-1])-1)*100))

