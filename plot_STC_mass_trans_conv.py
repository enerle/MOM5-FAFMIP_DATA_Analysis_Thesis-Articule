import sys
import os
import numpy as np
from scipy import stats
import cmocean
import matplotlib.pyplot as plt
from pylab import *
import netCDF4 as nc

#---------------------- LOAD ALL DATA
#datadir  = '/home/clima-archive2/rfarneti/RENE/DATA/'
datadir = '/home/netapp-clima-users/rnavarro/ANALYSIS/BLAKER/DATA'

exp       = ["faf-stress","faf-water","faf-heat","control"]
filename1 = ["STC_FAFSTRESS.nc","STC_FAFWATER.nc","STC_FAFHEAT.nc","STC_flux-only.nc"]

time             = [None]*len(exp)

conv             = [None]*len(exp)
trans9n          = [None]*len(exp)
trans9s          = [None]*len(exp)

conv_int         = [None]*len(exp)
trans9n_int      = [None]*len(exp)
trans9s_int      = [None]*len(exp)

conv_wbc         = [None]*len(exp)
trans9n_wbc      = [None]*len(exp)
trans9s_wbc      = [None]*len(exp)

conv_mean        = [None]*len(exp)
trans9n_mean     = [None]*len(exp)
trans9s_mean     = [None]*len(exp)

conv_int_mean    = [None]*len(exp)
trans9n_int_mean = [None]*len(exp)
trans9s_int_mean = [None]*len(exp)

conv_wbc_mean    = [None]*len(exp)
trans9n_wbc_mean = [None]*len(exp)
trans9s_wbc_mean = [None]*len(exp)

#---> Get the ACC
for i in range(len(exp)):  
    fn = os.path.join(datadir,filename1[i]) 
    print("Working on ", fn)
    file = nc.Dataset(fn)
    time[i]    = file.variables['TIME'][:]/365 -2188.0

    conv[i]        = np.squeeze(file.variables['CONV'][:])
    trans9n[i]     = abs(np.squeeze(file.variables['TRANS9N'][:]))
    trans9s[i]     = abs(np.squeeze(file.variables['TRANS9S'][:]))

    conv_int[i]    = np.squeeze(file.variables['CONV_INT'][:])
    trans9n_int[i] = abs(np.squeeze(file.variables['TRANS9N_INT'][:]))
    trans9s_int[i] = abs(np.squeeze(file.variables['TRANS9S_INT'][:]))

    conv_wbc[i]    = conv[i]    - conv_int[i]
    trans9n_wbc[i] = trans9n[i] - trans9n_int[i]
    trans9s_wbc[i] = trans9s[i] - trans9s_int[i]

    file.close()

for i in range(len(exp)):
    conv_mean[i]        = np.mean(conv[i][61:70])
    trans9n_mean[i]     = np.mean(trans9n[i][61:70])
    trans9s_mean[i]     = np.mean(trans9s[i][61:70])

    conv_int_mean[i]    = np.mean(conv_int[i][61:70])
    trans9n_int_mean[i] = np.mean(trans9n_int[i][61:70])
    trans9s_int_mean[i] = np.mean(trans9s_int[i][61:70])

    conv_wbc_mean[i]    = np.mean(conv_wbc[i][61:70])
    trans9n_wbc_mean[i] = np.mean(trans9n_wbc[i][61:70])
    trans9s_wbc_mean[i] = np.mean(trans9s_wbc[i][61:70])

##------------------------PLOTTING
#rc('text', usetex=True)
#rc('figure', figsize=(8.27,8))
rc('figure', figsize=(8,14))

colors = ['black','blue','red','gray']
styles = ['solid','solid','solid','solid']

fig = plt.figure(1)
fig.subplots_adjust(hspace=0.25,wspace=0.12)
fig.tight_layout()
subplots_adjust(wspace=None, hspace=.3)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],conv[i]-conv[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Total convergence",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis([0,70,-4,4])
#ax.axis([0,70,50,57])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9n[i]-trans9n[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Total mass transport across 9$^o$N",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.axis([0,70,-4,4])
#ax.axis([0,70,20,25])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9s[i]-trans9s[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("Total mass transport across 9$^o$S",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.set_xlabel("Time (years)",fontsize=16)
#ax.legend(loc=3,ncol=2, fontsize=16)
ax.axis([0,70,-4,4])
#ax.axis([0,70,30,35])

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
plt.savefig('STC-conv-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

##INTERIOR
v = [0,70,-2.5,2.5]

fig = plt.figure(2)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],conv_int[i]-conv_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Equatorial mass convergence",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9n_int[i]-trans9n_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Northern hemisphere equatorward mass transport (across $9^o$N)",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9s_int[i]-trans9s_int[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("Southern hemisphere equatorward mass transport (across $9^o$S)",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
#ax.legend(loc=2,ncol=2, fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
#plt.savefig('STC-conv-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

##WESTERN BOUNDARY CURRENT CONTRIBUTION
v = [0,70,-4,4]

fig = plt.figure(3)

ax = fig.add_subplot(3,1,1)
for i in range(len(exp)-1):
    ax.plot(time[i],conv_wbc[i]-conv_wbc[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Equatorial mass convergence",fontsize=16)
ax.set_ylabel("Sv",fontsize=16)
ax.legend(loc=1,ncol=2, fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,2)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9n_wbc[i]-trans9n_wbc[-1],color=colors[i],linestyle=styles[i],linewidth=2.0, label = exp[i])

###
ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.xticks([0,10,20,30,40,50,60,70],[])

plt.title("Northern hemisphere equatorward mass transport (across $9^o$N)",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

ax = fig.add_subplot(3,1,3)
for i in range(len(exp)-1):
    ax.plot(time[i],trans9s_wbc[i]-trans9s_wbc[-1],color=colors[i],linestyle=styles[i],linewidth=2.0,label=exp[i])
###

ax.spines['top'].set_linewidth(2);  ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2); ax.spines['right'].set_linewidth(2)
ax.xaxis.set_tick_params(width=2);  ax.yaxis.set_tick_params(width=2)

plt.title("Southern hemisphere equatorward mass transport (across $9^o$S)",fontsize=16)
ax.set_ylabel("[Sv]",fontsize=16)
ax.set_xlabel("Time [years]",fontsize=16)
#ax.legend(loc=2,ncol=2, fontsize=16)
ax.axis(v)

plt.axhline(y=0.0,color='k',linestyle='--',linewidth=2) #includes zero line
plt.yticks(fontsize=16); plt.xticks(fontsize=16)
###

#plt.show()
#plt.savefig('STC-conv_wbc-timeseries.png',transparent = True, bbox_inches='tight',dpi=600)

print("--Total--")
print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & %.2f " %(conv_mean[-1]) + " & %.2f " %(conv_mean[0]-conv_mean[-1]) + " & %.2f " %(conv_mean[1]-conv_mean[-1]) + " & %.2f " %(conv_mean[2]-conv_mean[-1]) + " & %.2f " %(conv_mean[3]-conv_mean[-1]))
print("\centering $Trans. 9N$" + " & %.2f " %(trans9n_mean[-1]) + " & %.2f " %(trans9n_mean[0]-trans9n_mean[-1]) + " & %.2f " %(trans9n_mean[1]-trans9n_mean[-1]) + " & %.2f " %(trans9n_mean[2]-trans9n_mean[-1]) + " & %.2f " %(trans9n_mean[3]-trans9n_mean[-1]))
print("\centering $Trans. 9S$" + " & %.2f " %(trans9s_mean[-1]) + " & %.2f " %(trans9s_mean[0]-trans9s_mean[-1]) + " & %.2f " %(trans9s_mean[1]-trans9s_mean[-1]) + " & %.2f " %(trans9s_mean[2]-trans9s_mean[-1]) + " & %.2f " %(trans9s_mean[3]-trans9s_mean[-1]))

print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & " + " & %.0f " %(((conv_mean[0]/conv_mean[-1])-1)*100.) + " & %.0f " %(((conv_mean[1]/conv_mean[-1])-1)*100.) + " & %.0f " %(((conv_mean[2]/conv_mean[-1])-1)*100.) + " & %.0f " %(((conv_mean[3]/conv_mean[-1])-1)*100.))
print("\centering $Trans. 9N$" + " & " + " & %.0f " %(((trans9n_mean[0]/trans9n_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_mean[1]/trans9n_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_mean[2]/trans9n_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_mean[3]/trans9n_mean[-1])-1)*100.))
print("\centering $Trans. 9S$" + " & " + " & %.0f " %(((trans9s_mean[0]/trans9s_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_mean[1]/trans9s_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_mean[2]/trans9s_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_mean[3]/trans9s_mean[-1])-1)*100.))


print("--Interior--")
print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & %.2f " %(conv_int_mean[-1]) + " & %.2f " %(conv_int_mean[0]-conv_int_mean[-1]) + " & %.2f " %(conv_int_mean[1]-conv_int_mean[-1]) + " & %.2f " %(conv_int_mean[2]-conv_int_mean[-1]) + " & %.2f " %(conv_int_mean[3]-conv_int_mean[-1]))
print("\centering $Trans. 9N$" + " & %.2f " %(trans9n_int_mean[-1]) + " & %.2f " %(trans9n_int_mean[0]-trans9n_int_mean[-1]) + " & %.2f " %(trans9n_int_mean[1]-trans9n_int_mean[-1]) + " & %.2f " %(trans9n_int_mean[2]-trans9n_int_mean[-1]) + " & %.2f " %(trans9n_int_mean[3]-trans9n_int_mean[-1]))
print("\centering $Trans. 9S$" + " & %.2f " %(trans9s_int_mean[-1]) + " & %.2f " %(trans9s_int_mean[0]-trans9s_int_mean[-1]) + " & %.2f " %(trans9s_int_mean[1]-trans9s_int_mean[-1]) + " & %.2f " %(trans9s_int_mean[2]-trans9s_int_mean[-1]) + " & %.2f " %(trans9s_int_mean[3]-trans9s_int_mean[-1]))

print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & " + " & %.0f " %(((conv_int_mean[0]/conv_int_mean[-1])-1)*100.) + " & %.0f " %(((conv_int_mean[1]/conv_int_mean[-1])-1)*100.) + " & %.0f " %(((conv_int_mean[2]/conv_int_mean[-1])-1)*100.) + " & %.0f " %(((conv_int_mean[3]/conv_int_mean[-1])-1)*100.))
print("\centering $Trans. 9N$" + " & " + " & %.0f " %(((trans9n_int_mean[0]/trans9n_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_int_mean[1]/trans9n_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_int_mean[2]/trans9n_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_int_mean[3]/trans9n_int_mean[-1])-1)*100.))
print("\centering $Trans. 9S$" + " & " + " & %.0f " %(((trans9s_int_mean[0]/trans9s_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_int_mean[1]/trans9s_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_int_mean[2]/trans9s_int_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_int_mean[3]/trans9s_int_mean[-1])-1)*100.))


print("--Western boundary current--")
print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & %.2f " %(conv_wbc_mean[-1]) + " & %.2f " %(conv_wbc_mean[0]-conv_wbc_mean[-1]) + " & %.2f " %(conv_wbc_mean[1]-conv_wbc_mean[-1]) + " & %.2f " %(conv_wbc_mean[2]-conv_wbc_mean[-1]) + " & %.2f " %(conv_wbc_mean[3]-conv_wbc_mean[-1]))
print("\centering $Trans. 9N$" + " & %.2f " %(trans9n_wbc_mean[-1]) + " & %.2f " %(trans9n_wbc_mean[0]-trans9n_wbc_mean[-1]) + " & %.2f " %(trans9n_wbc_mean[1]-trans9n_wbc_mean[-1]) + " & %.2f " %(trans9n_wbc_mean[2]-trans9n_wbc_mean[-1]) + " & %.2f " %(trans9n_wbc_mean[3]-trans9n_wbc_mean[-1]))
print("\centering $Trans. 9S$" + " & %.2f " %(trans9s_wbc_mean[-1]) + " & %.2f " %(trans9s_wbc_mean[0]-trans9s_wbc_mean[-1]) + " & %.2f " %(trans9s_wbc_mean[1]-trans9s_wbc_mean[-1]) + " & %.2f " %(trans9s_wbc_mean[2]-trans9s_wbc_mean[-1]) + " & %.2f " %(trans9s_wbc_mean[3]-trans9s_wbc_mean[-1]))

print("& var & ctl & stress & water & heat & all ")
print("\centering $Conv.$" + " & " + " & %.0f " %(((conv_wbc_mean[0]/conv_wbc_mean[-1])-1)*100.) + " & %.0f " %(((conv_wbc_mean[1]/conv_wbc_mean[-1])-1)*100.) + " & %.0f " %(((conv_wbc_mean[2]/conv_wbc_mean[-1])-1)*100.) + " & %.0f " %(((conv_wbc_mean[3]/conv_wbc_mean[-1])-1)*100.))
print("\centering $Trans. 9N$" + " & " + " & %.0f " %(((trans9n_wbc_mean[0]/trans9n_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_wbc_mean[1]/trans9n_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_wbc_mean[2]/trans9n_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9n_wbc_mean[3]/trans9n_wbc_mean[-1])-1)*100.))
print("\centering $Trans. 9S$" + " & " + " & %.0f " %(((trans9s_wbc_mean[0]/trans9s_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_wbc_mean[1]/trans9s_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_wbc_mean[2]/trans9s_wbc_mean[-1])-1)*100.) + " & %.0f " %(((trans9s_wbc_mean[3]/trans9s_wbc_mean[-1])-1)*100.))

