#!/bin/csh

#module purge
module load nco
module load cdo
module load ferret

set echo on

cd /home/clima-archive2/rfarneti/RENE/DATA

set RUN = (flux-only FAFHEAT FAFWATER FAFSTRESS FAFALL FAFHEAT_FAFSTRESS)
set i = 1

while ($i <= 6)
set EXP  = $RUN[$i]

ferret <<!
!!------------------------------------------------------------
!! --- Generating SST and SSS
!!------------------------------------------------------------
use temp_$EXP.nc !1
use salt_$EXP.nc !2

let SST = temp[k=1,d=1]
let SSS = salt[k=1,d=2]

save/file=SST_SSS_$EXP.nc/clobber SST,SSS

exit
!

@ i = $i + 1
end
