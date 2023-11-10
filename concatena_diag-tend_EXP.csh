#!/bin/csh

module purge
module load nco
module load cdo
module load ferret

#set RUN = (Blaker_flux-only Blaker_FAFHEAT Blaker_FAFHEAT-plus)
set RUN = (Blaker_FAFSTRESS Blaker_FAFWATER)

set i = 1

while ($i <= 2)
set NAME=${RUN[$i]}.nc
set IDIR=/home/netapp-clima-users1/rnavarro/FMS/archive/${RUN[$i]}/history
 
ncrcat -v temp_tendency           $IDIR/*ocean_tendency.nc  temp_tendency_${NAME}
ncrcat -v temp_advection          $IDIR/*ocean_tendency.nc  temp_advection_${NAME}
ncrcat -v neutral_gm_temp         $IDIR/*ocean_tendency.nc  neutral_gm_temp_${NAME}
ncrcat -v neutral_diffusion_temp  $IDIR/*ocean_tendency.nc  neutral_diffusion_temp_${NAME}
ncrcat -v temp_submeso            $IDIR/*ocean_tendency.nc  temp_submeso_${NAME}
ncrcat -v temp_vdiffuse_diff_cbt  $IDIR/*ocean_tendency.nc  temp_vdiffuse_diff_cbt_${NAME}

ncrename -v temp_tendency,opottemptend             temp_tendency_${NAME}           opottemptend_${NAME}
ncrename -v temp_advection,opottemprmadvect        temp_advection_${NAME}          opottemprmadvect_${NAME}
ncrename -v neutral_gm_temp,opottemppadvect        neutral_gm_temp_${NAME}         opottemppadvect_${NAME}
ncrename -v neutral_diffusion_temp,opottemppmdiff  neutral_diffusion_temp_${NAME}  opottemppmdiff_${NAME}
ncrename -v temp_submeso,opottemppsmadvect         temp_submeso_${NAME}            opottemppsmadvect_${NAME}
ncrename -v temp_vdiffuse_diff_cbt,opottempdiff    temp_vdiffuse_diff_cbt_${NAME}  opottempdiff_${NAME}

cdo merge opottemp*_${NAME} MOM_opottemp-diag_${NAME} 

##SALINITY

ncrcat -v salt_tendency           $IDIR/*ocean_tendency.nc  salt_tendency_${NAME}
ncrcat -v salt_advection          $IDIR/*ocean_tendency.nc  salt_advection_${NAME}
ncrcat -v neutral_gm_salt         $IDIR/*ocean_tendency.nc  neutral_gm_salt_${NAME}
ncrcat -v neutral_diffusion_salt  $IDIR/*ocean_tendency.nc  neutral_diffusion_salt_${NAME}
ncrcat -v salt_submeso            $IDIR/*ocean_tendency.nc  salt_submeso_${NAME}
ncrcat -v salt_vdiffuse_diff_cbt  $IDIR/*ocean_tendency.nc  salt_vdiffuse_diff_cbt_${NAME}

ncrename -v salt_tendency,osalttend             salt_tendency_${NAME}           osalttend_${NAME}
ncrename -v salt_advection,osaltrmadvect        salt_advection_${NAME}          osaltrmadvect_${NAME}
ncrename -v neutral_gm_salt,osaltppadvect       neutral_gm_salt_${NAME}         osaltppadvect_${NAME}
ncrename -v neutral_diffusion_salt,osaltpmdiff  neutral_diffusion_salt_${NAME}  osaltpmdiff_${NAME}
ncrename -v salt_submeso,osaltpsmadvect         salt_submeso_${NAME}            osaltpsmadvect_${NAME}
ncrename -v salt_vdiffuse_diff_cbt,osaltdiff    salt_vdiffuse_diff_cbt_${NAME}  osaltdiff_${NAME}

cdo merge osalt*_${NAME} MOM_osalt-diag_${NAME}

#cdo remapbil,r128x64 -sellonlatbox,0,360,-88.59375,88.59375 MOM_${NAME} regrided_${NAME}
#ncap2 -s 'lon=lon+1.40625' regrided_${NAME}                             MOM_regrided_${NAME}

@ i = $i + 1

end

mv MOM_*.nc ../FAFMIP_data
