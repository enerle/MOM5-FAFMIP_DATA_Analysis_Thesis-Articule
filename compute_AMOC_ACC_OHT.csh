#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

echo "------------------------------------------------------------------"
echo "--- Generating the GMOC, AMOC and ACC time series"
echo "------------------------------------------------------------------"
ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2
use ty_trans_rho_$EXP.nc !3
use ty_trans_rho_gm_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!------------------------------------------------------------
!! --- Generating MOC
!!------------------------------------------------------------
let euler     = ty_trans[d=1,l=61:70@ave]
let gm        = ty_trans_gm[d=2,l=61:70@ave]
let moc       = euler[i=@sum,k=@rsum] +  gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_gm    = gm[i=@sum]
let moc_mean  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_$EXP.nc/clobber moc
save/file=MOC_$EXP.nc/append  moc_gm
save/file=MOC_$EXP.nc/append  moc_mean

!! --- Density space
let euler         = ty_trans_rho[d=3,l=61:70@ave]
let gm            = ty_trans_rho_gm[d=4,l=61:70@ave]
let moc_rho       = euler[i=@sum,k=@rsum] +  gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_rho_gm    = gm[i=@sum]
let moc_rho_mean  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_RHO_$EXP.nc/clobber moc_rho
save/file=MOC_RHO_$EXP.nc/append  moc_rho_gm
save/file=MOC_RHO_$EXP.nc/append  moc_rho_mean

!!------------------------------------------------------------
!! --- Generating timeseries for MOC cells
!!------------------------------------------------------------
let mocts       = ty_trans[d=1,i=@sum,k=@rsum] + ty_trans_gm[d=2,i=@sum] - ty_trans[d=1,i=@sum,k=@sum]
let mocts_mean  = ty_trans[d=1,i=@sum,k=@rsum] - ty_trans[d=1,i=@sum,k=@sum]
let mocts_gm    = ty_trans_gm[d=2,i=@sum] 

save/file=MOC_$EXP.timeseries.nc/clobber mocts
save/file=MOC_$EXP.timeseries.nc/append  mocts_gm
save/file=MOC_$EXP.timeseries.nc/append  mocts_mean

!! --- Density space
let mocrhots       = ty_trans_rho[d=3,i=@sum,k=@rsum] + ty_trans_rho_gm[d=4,i=@sum] - ty_trans_rho[d=3,i=@sum,k=@sum]
let mocrhots_mean  = ty_trans_rho[d=3,i=@sum,k=@rsum] - ty_trans_rho[d=3,i=@sum,k=@sum]
let mocrhots_gm    = ty_trans_rho_gm[d=4,i=@sum]

save/file=MOC_RHO_$EXP.timeseries.nc/clobber mocrhots
save/file=MOC_RHO_$EXP.timeseries.nc/append  mocrhots_gm
save/file=MOC_RHO_$EXP.timeseries.nc/append  mocrhots_mean

!!----Mask
use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]
let tmask_atl  = if (( tmask[d=5] EQ 2 OR tmask[d=5] EQ 4 )) then one else one-11
let tmask_ip   = if (( tmask[d=5] EQ 3 OR tmask[d=5] EQ 5 )) then one else one-11
let tmask_so   = if (( tmask[d=5] EQ 1 )) then one else one-11
let tmask_pac  = if (( tmask[d=5] EQ 3 )) then one else one-11
let tmask_paso = if (( tmask[d=5] EQ 1 OR tmask[d=5] EQ 3 )) then one else one-11

set variable/bad=-10. tmask_atl
set variable/bad=-10. tmask_ip
set variable/bad=-10. tmask_so
set variable/bad=-10. tmask_pac
set variable/bad=-10. tmask_paso

!!------------------------------------------------------------
!! --- Generating AMOC
!!------------------------------------------------------------
let euler      = ty_trans[d=1]*tmask_atl
let gm         = ty_trans_gm[d=2]*tmask_atl
let amoc       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let amoc_gm    = gm[i=@sum]
let amoc_mean  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

let amoc_41n = amoc_mean[y=41n,k=@max]
let amoc_26n = amoc_mean[y=26n,k=@max]
let amoc_30s = amoc_mean[y=30s,k=@max]
let aabw50   =  mocts_mean[y=50s,z=1036:1038@min]
let aabw60   =  mocts_mean[y=60s,z=1036:1038@min]
let aabw     =  mocts_mean[y=50s:30s@min,z=2500:5500@min]

save/file=MOC_$EXP.nc/append amoc[l=61:70@ave]
save/file=MOC_$EXP.nc/append amoc_gm[l=61:70@ave]
save/file=MOC_$EXP.nc/append amoc_mean[l=61:70@ave]
save/file=MOC_$EXP.nc/append amoc_41n
save/file=MOC_$EXP.nc/append amoc_26n
save/file=MOC_$EXP.nc/append amoc_30s
save/file=MOC_$EXP.nc/append aabw50
save/file=MOC_$EXP.nc/append aabw60
save/file=MOC_$EXP.nc/append aabw

!! --- Density space
let euler         = ty_trans_rho[d=3,l=61:70@ave]*tmask_atl
let gm            = ty_trans_rho_gm[d=4,l=61:70@ave]*tmask_atl
let amoc_rho       = euler[i=@sum,k=@rsum] +  gm[i=@sum] - euler[i=@sum,k=@sum]
let amoc_rho_gm    = gm[i=@sum]
let amoc_rho_mean  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_RHO_$EXP.nc/append  amoc_rho
save/file=MOC_RHO_$EXP.nc/append  amoc_rho_gm
save/file=MOC_RHO_$EXP.nc/append  amoc_rho_mean

!!------------------------------------------------------------
!! --- Generating MOC Pacific branch
!!------------------------------------------------------------
let euler         = ty_trans[d=1]*tmask_pac
let gm            = ty_trans_gm[d=2]*tmask_pac
let moc_pac       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_gm_pac    = gm[i=@sum]
let moc_mean_pac  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_$EXP.nc/append moc_pac[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_gm_pac[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_mean_pac[l=61:70@ave]

!! --- Density space
let euler             = ty_trans_rho[d=3]*tmask_pac
let gm                = ty_trans_rho_gm[d=4]*tmask_pac
let moc_rho_pac       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_rho_gm_pac    = gm[i=@sum]
let moc_rho_mean_pac  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_RHO_$EXP.nc/append  moc_rho_pac[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_gm_pac[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_mean_pac[l=61:70@ave]

!!------------------------------------------------------------
!! --- Generating MOC Southern Ocean branch
!!------------------------------------------------------------
let euler         = ty_trans[d=1]*tmask_so
let gm            = ty_trans_gm[d=2]*tmask_so
let moc_soc       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_gm_soc    = gm[i=@sum]
let moc_mean_soc  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_$EXP.nc/append moc_soc[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_gm_soc[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_mean_soc[l=61:70@ave]

!! --- Density space
let euler             = ty_trans_rho[d=3]*tmask_so
let gm                = ty_trans_rho_gm[d=4]*tmask_so
let moc_rho_soc       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_rho_gm_soc    = gm[i=@sum]
let moc_rho_mean_soc  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_RHO_$EXP.nc/append  moc_rho_soc[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_gm_soc[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_mean_soc[l=61:70@ave]

!!------------------------------------------------------------
!! --- Generating MOC Pacific and Southern Ocean branches
!!------------------------------------------------------------
let euler         = ty_trans[d=1]*tmask_paso
let gm            = ty_trans_gm[d=2]*tmask_paso
let moc_paso       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_gm_paso    = gm[i=@sum]
let moc_mean_paso  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_$EXP.nc/append moc_paso[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_gm_paso[l=61:70@ave]
save/file=MOC_$EXP.nc/append moc_mean_paso[l=61:70@ave]

!! --- Density space
let euler             = ty_trans_rho[d=3]*tmask_paso
let gm                = ty_trans_rho_gm[d=4]*tmask_paso
let moc_rho_paso       = euler[i=@sum,k=@rsum] + gm[i=@sum] - euler[i=@sum,k=@sum]
let moc_rho_gm_paso    = gm[i=@sum]
let moc_rho_mean_paso  = euler[i=@sum,k=@rsum] - euler[i=@sum,k=@sum]

save/file=MOC_RHO_$EXP.nc/append  moc_rho_paso[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_gm_paso[l=61:70@ave]
save/file=MOC_RHO_$EXP.nc/append  moc_rho_mean_paso[l=61:70@ave]

!!------------------------------------------------------------
!! --- Generating time serie of ACC
!!------------------------------------------------------------
use tx_trans_$EXP.nc !6
let acc = tx_trans[d=6,x=73w,y=80s:50s@sum,z=@sum]
save/file=ACC_$EXP.nc/clobber acc

!!------------------------------------------------------------
!! --- Heat transport
!!------------------------------------------------------------
use temp_yflux_adv_int_z_$EXP.nc !7
use temp_yflux_gm_int_z_$EXP.nc !8
use temp_yflux_ndiffuse_int_z_$EXP.nc !9

let gladv    = temp_yflux_adv_int_z[d=7,l=61:70@ave]
let atadv    = temp_yflux_adv_int_z[d=7,l=61:70@ave]*tmask_atl
let ipadv    = temp_yflux_adv_int_z[d=7,l=61:70@ave]*tmask_ip
let soadv    = temp_yflux_adv_int_z[d=7,l=61:70@ave]*tmask_so
let pacadv   = temp_yflux_adv_int_z[d=7,l=61:70@ave]*tmask_pac
let GLOHT_M  = gladv[i=@sum]
let ATOHT_M  = atadv[i=@sum]
let IPOHT_M  = ipadv[i=@sum]
let SOOHT_M  = soadv[i=@sum]
let PACOHT_M = pacadv[i=@sum]

let ggm        = TEMP_YFLUX_GM_INT_Z[d=8,l=61:70@ave]
let agm        = TEMP_YFLUX_GM_INT_Z[d=8,l=61:70@ave]*tmask_atl
let ipgm       = TEMP_YFLUX_GM_INT_Z[d=8,l=61:70@ave]*tmask_ip
let sogm       = TEMP_YFLUX_GM_INT_Z[d=8,l=61:70@ave]*tmask_so
let pacgm      = TEMP_YFLUX_GM_INT_Z[d=8,l=61:70@ave]*tmask_pac
let GLOHT_GM   = ggm[i=@sum]
let ATOHT_GM   = agm[i=@sum]
let IPOHT_GM   = ipgm[i=@sum]
let SOOHT_GM   = sogm[i=@sum]
let PACOHT_GM  = pacgm[i=@sum]

let gdif      = temp_yflux_ndiffuse_int_z[d=9,l=61:70@ave]
let adif      = temp_yflux_ndiffuse_int_z[d=9,l=61:70@ave]*tmask_atl
let ipdif     = temp_yflux_ndiffuse_int_z[d=9,l=61:70@ave]*tmask_ip
let sodif     = temp_yflux_ndiffuse_int_z[d=9,l=61:70@ave]*tmask_so
let pacdif    = temp_yflux_ndiffuse_int_z[d=9,l=61:70@ave]*tmask_pac
let GLOHT_D   = gdif[i=@sum]
let ATOHT_D   = adif[i=@sum]
let IPOHT_D   = ipdif[i=@sum]
let SOOHT_D   = sodif[i=@sum]
let PACOHT_D  = pacdif[i=@sum]

let GLOHT  = GLOHT_M  + GLOHT_GM  + GLOHT_D
let ATOHT  = ATOHT_M  + ATOHT_GM  + ATOHT_D
let IPOHT  = IPOHT_M  + IPOHT_GM  + IPOHT_D
let SOOHT  = SOOHT_M  + SOOHT_GM  + SOOHT_D
let PACOHT = PACOHT_M + PACOHT_GM + PACOHT_D
save/file=OHT_$EXP.nc/clobber GLOHT,ATOHT,IPOHT,SOOHT,PACOHT

exit
!
/bin/rm -f ferret.jnl*
@ i = $i + 1

end
