#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL)
#set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)

set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!

use ty_trans_$EXP.nc !1
use ty_trans_gm_$EXP.nc !2
use ty_trans_rho_$EXP.nc !3
use ty_trans_rho_gm_$EXP.nc !4

set region/z=0:5500/y=90S:90N/
set mem/size=9999

!!----Mask
use "/home/netapp-clima-users1/rnavarro/ANALYSIS/regionmask_v6.nc" !5
let one=tmask[d=5]/tmask[d=5]
let tmask_pac  = if (( tmask[d=5] EQ 3 )) then one else one-11
set variable/bad=-10. tmask_pac

!!!--- Density space
let tytransrho_tot      = ty_trans_rho[d=3]+ty_trans_rho_gm[d=4]
let tytransrho_tot_mask = tytransrho_tot*tmask_pac

let tytransrho_tot_mask_sum       = tytransrho_tot_mask[x=@sum]
let tytransrho_tot_mask_int_north = tytransrho_tot_mask[x=145e:70w@sum]
let tytransrho_tot_mask_int_south = tytransrho_tot_mask[x=165e:70w@sum]

let tytransrho_tot_mask_neg     = if(tytransrho_tot_mask_sum LT 0) then tytransrho_tot_mask_sum else 0.
let tytransrho_tot_mask_pos     = if(tytransrho_tot_mask_sum GT 0) then tytransrho_tot_mask_sum else 0.
let tytransrho_tot_mask_int_neg = if(tytransrho_tot_mask_int_north LT 0) then tytransrho_tot_mask_int_north else 0.
let tytransrho_tot_mask_int_pos = if(tytransrho_tot_mask_int_south GT 0) then tytransrho_tot_mask_int_south else 0.

let TRANSRHO9N     = tytransrho_tot_mask_neg[y=9N]
let TRANSRHO9S     = tytransrho_tot_mask_pos[y=9S]
let TRANSRHO9N_INT = tytransrho_tot_mask_int_neg[y=9N]
let TRANSRHO9S_INT = tytransrho_tot_mask_int_pos[y=9S]

let RHOLEVEL_TRANSRHO9N     = TRANSRHO9N[z=1033:1038@loc:0]
let RHOLEVEL_TRANSRHO9S     = TRANSRHO9S[z=1033:1038@loc:0]
let RHOLEVEL_TRANSRHO9N_INT = TRANSRHO9N_INT[z=1033:1038@loc:0]
let RHOLEVEL_TRANSRHO9S_INT = TRANSRHO9S_INT[z=1033:1038@loc:0]

let RHOLEVEL_TRANSRHO9N_mean     = RHOLEVEL_TRANSRHO9N[l=61:70@ave]
let RHOLEVEL_TRANSRHO9S_mean     = RHOLEVEL_TRANSRHO9S[l=61:70@ave]
let RHOLEVEL_TRANSRHO9N_INT_mean = RHOLEVEL_TRANSRHO9N_INT[l=61:70@ave]
let RHOLEVEL_TRANSRHO9S_INT_mean = RHOLEVEL_TRANSRHO9S_INT[l=61:70@ave]

let transrho9n_above_rholevel     = if(Z LT RHOLEVEL_TRANSRHO9N_mean) then TRANSRHO9N else 0.
let transrho9s_above_rholevel     = if(Z LT RHOLEVEL_TRANSRHO9S_mean) then TRANSRHO9S else 0.
let transrho9n_int_above_rholevel = if(Z LT RHOLEVEL_TRANSRHO9N_INT_mean) then TRANSRHO9N_INT else 0.
let transrho9s_int_above_rholevel = if(Z LT RHOLEVEL_TRANSRHO9S_INT_mean) then TRANSRHO9S_INT else 0.

let CONVRHO     = transrho9s_above_rholevel     - transrho9n_above_rholevel
let CONVRHO_INT = transrho9s_int_above_rholevel - transrho9n_int_above_rholevel

save/file=STC_RHO_v2_${EXP}_v2.nc/clobber CONVRHO[k=@sum],CONVRHO_INT[k=@sum]
!!save/file=STC_RHO_v2_${EXP}_v2.nc/append  transrho9n_above_rholevel[k=@sum],transrho9s_above_rholevel[k=@sum]
!!save/file=STC_RHO_v2_${EXP}_v2.nc/append  transrho9n_int_above_rholevel[k=@sum],transrho9s_int_above_rholevel[k=@sum]
save/file=STC_RHO_v2_${EXP}_v2.nc/append  RHOLEVEL_TRANSRHO9N_mean,RHOLEVEL_TRANSRHO9S_mean,RHOLEVEL_TRANSRHO9N_INT_mean,RHOLEVEL_TRANSRHO9S_INT_mean

save/file=STC_RHOLEVELS_${EXP}.nc/clobber RHOLEVEL_TRANSRHO9N,RHOLEVEL_TRANSRHO9S,RHOLEVEL_TRANSRHO9N_INT,RHOLEVEL_TRANSRHO9S_INT

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
