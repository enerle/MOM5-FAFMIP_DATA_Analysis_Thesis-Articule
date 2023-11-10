#!/bin/csh

#module purge
#module load nco
#module load cdo
module load ferret

set echo on

#cd DATA
cd /home/clima-archive2/rfarneti/RENE/DATA
set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)

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

let tytrans_tot      = ty_trans[d=1]+ty_trans_gm[d=2]
let tytrans_tot_mask = tytrans_tot*tmask_pac
 
let tytrans_tot_mask_sum       = tytrans_tot_mask[x=@sum]
let tytrans_tot_mask_int_north = tytrans_tot_mask[x=145e:70w@sum]
let tytrans_tot_mask_int_south = tytrans_tot_mask[x=165e:70w@sum]

let tytrans_tot_mask_neg     = if(tytrans_tot_mask_sum LT 0) then tytrans_tot_mask_sum else 0.
let tytrans_tot_mask_pos     = if(tytrans_tot_mask_sum GT 0) then tytrans_tot_mask_sum else 0.
let tytrans_tot_mask_int_neg = if(tytrans_tot_mask_int_north LT 0) then tytrans_tot_mask_int_north else 0.
let tytrans_tot_mask_int_pos = if(tytrans_tot_mask_int_south GT 0) then tytrans_tot_mask_int_south else 0.

let/title="Total STC transport (Sv) at 9N depth coordinate"    TRANS9N     = tytrans_tot_mask_neg[y=9N,z=0:1000@sum]
let/title="Total STC transport (Sv) at 9S depth coordinate"    TRANS9S     = tytrans_tot_mask_pos[y=9S,z=0:1000@sum]
let/title="Interior STC transport (Sv) at 9N depth coordinate" TRANS9N_int = tytrans_tot_mask_int_neg[y=9N,z=0:1000@sum]
let/title="Interior STC transport (Sv) at 9S depth coordinate" TRANS9S_int = tytrans_tot_mask_int_pos[y=9S,z=0:1000@sum]

let/title="Convergence of Total STC transport (Sv) (9S-9N) in depth coordinate"    CONV =     TRANS9S - TRANS9N
let/title="Convergence of Interior STC transport (Sv) (9S-9N) in depth coordinate" CONV_int = TRANS9S_int - TRANS9N_int

save/file=STC_${EXP}.nc/clobber CONV,CONV_int,TRANS9N,TRANS9S,TRANS9N_int,TRANS9S_int

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

let/title="Total STC transport (Sv) at 9N density coordinate"    TRANSRHO9N     = tytransrho_tot_mask_neg[y=9N,z=1028:1036@sum]
let/title="Total STC transport (Sv) at 9S density coordinate"    TRANSRHO9S     = tytransrho_tot_mask_pos[y=9S,z=1028:1036@sum]
let/title="Interior STC transport (Sv) at 9N density coordinate" TRANSRHO9N_int = tytransrho_tot_mask_int_neg[y=9N,z=1028:1036@sum]
let/title="Interior STC transport (Sv) at 9S density coordinate" TRANSRHO9S_int = tytransrho_tot_mask_int_pos[y=9S,z=1028:1036@sum]

let/title="Convergence of Total STC transport (Sv) (9S-9N) in density coordinate"    CONVRHO =     TRANSRHO9S     - TRANSRHO9N
let/title="Convergence of Interior STC transport (Sv) (9S-9N) in density coordinate" CONVRHO_int = TRANSRHO9S_int - TRANSRHO9N_int

save/file=STC_RHO_${EXP}.nc/clobber CONVRHO,CONVRHO_int,TRANSRHO9N,TRANSRHO9S,TRANSRHO9N_int,TRANSRHO9S_int 

!!--- Sea surface temperature and salinity timeseries
use SST_SSS_${EXP}.nc !6
let SSTt = sst[d=6,x=180w:90w@ave,y=9s:9n@ave]
let SSSt = sss[d=6,x=180w:90w@ave,y=9s:9n@ave]

save/clobber/file=SST_SSS_9S9N_timeseries_${EXP}.nc SSTt,SSSt

exit
!

/bin/rm -f ferret.jnl*
@ i = $i + 1
end
