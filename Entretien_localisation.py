"""Main navigation module"""

import numpy as np
from Gerer_donnees import NavInput, NavOutput
from tqdm import tqdm #type:ignore
from functions import *
from kalman_filter_v7 import *


def calcul_nav(data_in: NavInput, donnees_NI_dispo: bool):
    r"""Script qui permet d'itérer sur le temps et de calculer chaque paramètre
    de la navigation

    Parameters
    ----------
    data_in : class structtype
        structure rassemblant toutes les données de la navigation qui seront utilisée et/ou calculées

    Returns
    -------
    data_out : class structtype
        structure rassemblant toutes les données calculées de la navigation
    On passe en nav à partir de 777 secondes

    """

    # Définition des variables locales de la fonction à l'aide des données
    # initialisées de la navigation
    temps = data_in.temps_s
    Lon = data_in.Lon_calculee_deg * np.pi / 180
    Lat = data_in.Lat_calculee_deg * np.pi / 180
    Alt = data_in.Alt_calculee_m
    Vn = data_in.Vn_calculee_ms
    Vw = data_in.Vw_calculee_ms
    Vz = data_in.Vz_calculee_ms
    Cap = data_in.Cap_calcule_rad
    Rou = data_in.Roulis_calcule_rad
    Tan = data_in.Tangage_calcule_rad
    Bx = data_in.Bacc_x_estime
    By = data_in.Bacc_y_estime
    Bz = data_in.Bacc_z_estime
    Dx = data_in.Dgyr_x_estime
    Dy = data_in.Dgyr_y_estime
    Dz = data_in.Dgyr_z_estime
    Sigma_Lon = data_in.Sigma_Lon_calculee_deg * np.pi / 180
    Sigma_Lat = data_in.Sigma_Lat_calculee_deg * np.pi / 180
    Sigma_Alt = data_in.Sigma_Alt_calculee_m
    Sigma_Vn = data_in.Sigma_Vn_calculee_ms
    Sigma_Vw = data_in.Sigma_Vw_calculee_ms
    Sigma_Vz = data_in.Sigma_Vz_calculee_ms
    Sigma_C = data_in.Sigma_Cap_calcule_rad
    Sigma_R = data_in.Sigma_Roulis_calcule_rad
    Sigma_T = data_in.Sigma_Tangage_calcule_rad
    Sigma_Bx = data_in.Sigma_Bacc_x_estime
    Sigma_By = data_in.Sigma_Bacc_y_estime
    Sigma_Bz = data_in.Sigma_Bacc_z_estime
    Sigma_Dx = data_in.Sigma_Dgyr_x_estime
    Sigma_Dy = data_in.Sigma_Dgyr_y_estime
    Sigma_Dz = data_in.Sigma_Dgyr_z_estime
    ivx = data_in.inc_vit_x_ms
    ivy = data_in.inc_vit_y_ms
    ivz = data_in.inc_vit_z_ms
    iax = data_in.inc_angl_x_rad
    iay = data_in.inc_angl_y_rad
    iaz = data_in.inc_angl_z_rad
    Vxm = data_in.Vx_m
    Vym = data_in.Vy_m
    Vzm = data_in.Vz_m
    lat_gnss = data_in.lat_gnss
    lon_gnss = data_in.lon_gnss
    # Constantes utiles aux calculs
    g = 9.81  # attraction terrestre
    dt = 0.01  # pas de temps
    Rt = 6378000.0  # Rayon terrestre en mètres
    omega_t_ti = np.array([0,0,np.deg2rad(15.04)/3600])
    # Initialisation de la navigation
    Rou[0, 0] = data_in.Rou_initial_rad  # Initialisation de la valeur de roulis
    Tan[0, 0] = data_in.Tan_initial_rad  # Initialisation de la valeur de tangage
    Cap[0, 0] = data_in.Cap_initial_rad  # Initialisation de la valeur de cap
    Lon[0, 0] = data_in.Lon_initiale_rad  # Initialisation de la valeur de longitude
    Lat[0, 0] = data_in.Lat_initiale_rad  # Initialisation de la valeur de latitude
    # Alt[0, 0] = data_in.Alt_initiale_m  # Initialisation de la valeur d'altitude
    t_g_b = k_r_t_2_tbg(Cap[0, 0], Rou[0, 0], Tan[0, 0]).T # /!\ transposing t_b_g matrix
    v_geo_vector = np.zeros((3, 1)).flatten()
    # omega_g_g_t = np.zeros((3, 1))
    t_g_t = lat_lon_2_tgt(Lat[0,0], Lon[0,0])
    for t in tqdm(
        range(1, np.shape(temps)[1]),
        desc="Processing",
    ):
        # Speed integration
        v_geo_vector = v_geo_vector + compute_delta_v_geo(t_g_b=t_g_b, 
                                                  delta_v_b=np.array([ivx[0, t], ivy[0, t], ivz[0, t]])) # formule d'euler donc t-1
        # Attitude integration
        curve_matrix = compute_curve_matrix(Lat[0, t]) # Latitude pas encore dispo
        delta_theta_g_gi = compute_delta_theta_g_gi(curve_matrix, v_geo_vector, t_g_t) # bizarre : curve_matrix est ancienne mais v_geo_vector est actualisee
        t_g_b = bortz_rot(delta_theta_g_gi) @ t_g_b @ bortz_rot(-np.array([iax[0,t], iay[0,t], iaz[0,t]])) # je ne sais pas me prononcer sur le synchronisme
        
        # Position integration
        t_g_t = bortz_rot(curve_matrix @ v_geo_vector * dt) @ t_g_t 
        
        # Attitude and position extraction
        Lat[0,t], Lon[0,t] = tgt_2_lat_lon(t_g_t)
        Cap[0,t], Rou[0,t], Tan[0,t] = tbg_2_k_r_t(tbg = t_g_b.T)
    # --------------------------------------------------------------------------------

    # Création d'une nouvelle structure pour les données en sortie
    data_out = NavOutput(
        # Attribution des éléments locaux aux éléments globaux dans la structure
        # Cette structure peut être complétée selon vos besoins, n'oubliez pas de mettre
        # à jour la définition de cette classe dans le fichier "Gerer_donnees.py"
        temps_s=temps,
        Lon_calculee_deg=Lon * 180 / np.pi,
        Lat_calculee_deg=Lat * 180 / np.pi,
        Alt_calculee_m=Alt,
        Vn_calculee_ms=Vn,
        Vw_calculee_ms=Vw,
        Vz_calculee_ms=Vz,
        Cap_calcule_rad=Cap,
        Roulis_calcule_rad=Rou,
        Tangage_calcule_rad=Tan,
        Bacc_x_estime=Bx,
        Bacc_y_estime=By,
        Bacc_z_estime=Bz,
        Dgyr_x_estime=Dx,
        Dgyr_y_estime=Dy,
        Dgyr_z_estime=Dz,
        Sigma_Lon_calculee_deg=Sigma_Lon * 180 / np.pi,
        Sigma_Lat_calculee_deg=Sigma_Lat * 180 / np.pi,
        Sigma_Alt_calculee_m=Sigma_Alt,
        Sigma_Vn_calculee_ms=Sigma_Vn,
        Sigma_Vw_calculee_ms=Sigma_Vw,
        Sigma_Vz_calculee_ms=Sigma_Vz,
        Sigma_Cap_calcule_rad=Sigma_C,
        Sigma_Roulis_calcule_rad=Sigma_R,
        Sigma_Tangage_calcule_rad=Sigma_T,
        Sigma_Bacc_x_estime=Sigma_Bx,
        Sigma_Bacc_y_estime=Sigma_By,
        Sigma_Bacc_z_estime=Sigma_Bz,
        Sigma_Dgyr_x_estime=Sigma_Dx,
        Sigma_Dgyr_y_estime=Sigma_Dy,
        Sigma_Dgyr_z_estime=Sigma_Dz,
        Inc_Vit_Xm=ivx,
        Inc_Vit_Ym=ivy,
        Inc_Vit_Zm=ivz,
        Inc_Ang_Xm=iax,
        Inc_Ang_Ym=iay,
        Inc_Ang_Zm=iaz,
        Lat_gnss=data_in.lat_gnss,
        Lon_gnss=data_in.lon_gnss,
        Alt_gnss=data_in.alt_gnss,
        nb_sat_gnss=data_in.nsat_gnss,
        val_gnss=data_in.val_gnss,
        dist_odo=temps,
        vor_bvs=data_in.vor_bvs,
        dme_bvs=data_in.dme_bvs,
        vor_dvl=data_in.vor_dvl,
        dme_dvl=data_in.dme_dvl,
        vor_pon=data_in.vor_pon,
        dme_pon=data_in.dme_pon,
        vor_rou=data_in.vor_rou,
        dme_rou=data_in.dme_rou,
    )
    # Renvoie de la nouvelle structure
    return data_out
