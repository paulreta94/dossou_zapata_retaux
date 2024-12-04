"""
Description
-----------

Fichier fonctionnel qui permet de créer une classe vide en ayant des champs
prédéfinis mis à 0 et une classe de sortie permettant de sortir les 
données intéressantes de la fonction de calcul

Classes Disponibles :
   
   - class NavInput
   - class NavOutput
   
Auteurs : Cédric LAURENT, Loïc DAVAIN
Créé le 10 juillet 2024

--------------------------------
"""


from dataclasses import dataclass
import numpy as np
from dataclasses import asdict

@dataclass
class NavInput:

    temps_s: np.ndarray = None
    """Temps du système, de dimension (1, N)"""
    Lon_calculee_deg: np.ndarray = None
    """Longitude calculée, de dimension (1, N)"""
    Lat_calculee_deg: np.ndarray = None
    """Latitude calculée, de dimension (1, N)"""
    Alt_calculee_m: np.ndarray = None
    """Altitude calculée, de dimension (1, N)"""

    # Déclaration des vitesses géographiques du porteur
    Vn_calculee_ms: np.ndarray = None
    """Vitesse Nord calculée, de dimension (1, N)"""
    Vw_calculee_ms: np.ndarray = None
    """Vitesse Ouest calculée, de dimension (1, N)"""
    Vz_calculee_ms: np.ndarray = None
    """Vitesse z calculée, de dimension (1, N)"""

    # Déclaration des attitudes et du cap du porteur
    Cap_calcule_rad: np.ndarray = None
    """Cap calculé, de dimension (1, N)"""
    Roulis_calcule_rad: np.ndarray = None
    """Roulis calculé, de dimension (1, N)"""
    Tangage_calcule_rad: np.ndarray = None
    """Tangage calculé, de dimension (1, N)"""

    # Déclaration de l'estimation du biais sur chaque axe
    Bacc_x_estime: np.ndarray = None
    """Biais accéléro sur l'axe X calculé, de dimension (1, N)"""
    Bacc_y_estime: np.ndarray = None
    """Biais accéléro sur l'axe Y calculé, de dimension (1, N)"""
    Bacc_z_estime: np.ndarray = None
    """Biais accéléro sur l'axe Z calculé, de dimension (1, N)"""

    # Déclaration de l'estimation des dérives sur chaque axe
    Dgyr_x_estime: np.ndarray = None
    """Dérive gyro sur l'axe X calculée, de dimension (1, N)"""    
    Dgyr_y_estime: np.ndarray = None
    """Dérive gyro sur l'axe Y calculée, de dimension (1, N)"""
    Dgyr_z_estime: np.ndarray = None
    """Dérive gyro sur l'axe Z calculée, de dimension (1, N)"""

    # Déclaration des variances de localisation du porteur
    Sigma_Lon_calculee_deg: np.ndarray = None
    """Variance longitude calculée, de dimension (1, N)"""
    Sigma_Lat_calculee_deg: np.ndarray = None
    """Variance latitude calculée, de dimension (1, N)"""
    Sigma_Alt_calculee_m: np.ndarray = None
    """Variance altitude calculée, de dimension (1, N)"""

    # Déclaration des variances des vitesses géographiques du porteur
    Sigma_Vn_calculee_ms: np.ndarray = None
    """Variance vitesse nord calculée, de dimension (1, N)"""
    Sigma_Vw_calculee_ms: np.ndarray = None
    """Variance vitesse ouest calculée, de dimension (1, N)"""
    Sigma_Vz_calculee_ms: np.ndarray = None
    """Variance vitesse z calculée, de dimension (1, N)"""

    # Déclaration des variances des attitudes et du cap du porteur
    Sigma_Cap_calcule_rad: np.ndarray = None
    """Variance cap calculée, de dimension (1, N)"""
    Sigma_Roulis_calcule_rad: np.ndarray = None
    """Variance roulis calculée, de dimension (1, N)"""
    Sigma_Tangage_calcule_rad: np.ndarray = None
    """Variance tangage calculée, de dimension (1, N)"""

    # Déclaration des variances des biais estimés sur chaque axe
    Sigma_Bacc_x_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe X calculée, de dimension (1, N)"""
    Sigma_Bacc_y_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe Y calculée, de dimension (1, N)"""
    Sigma_Bacc_z_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe Z calculée, de dimension (1, N)"""

    # Déclaration des variances des dérives estimées sur chaque axe
    Sigma_Dgyr_x_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe X calculée, de dimension (1, N)"""
    Sigma_Dgyr_y_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe Y calculée, de dimension (1, N)"""
    Sigma_Dgyr_z_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe Z calculée, de dimension (1, N)"""

    # Déclaration des vitesses sur chaque axe dans le repère de mesure
    Vx_m: np.ndarray = None
    """Vitesse sur l'axe X calculée dans [m], de dimension (1, N)"""
    Vy_m: np.ndarray = None
    """Vitesse sur l'axe Y calculée dans [m], de dimension (1, N)"""
    Vz_m: np.ndarray = None
    """Vitesse sur l'axe Z calculée dans [m], de dimension (1, N)"""

    # Déclaration des paramètres initiaux
    Cap_initial_rad: float = 0
    """Cap initial en radians, float"""
    Lon_initiale_rad: float = 0
    """Longitude initiale en radians, float"""
    Lat_initiale_rad: float = 0
    """Latitude initiale en radians, float"""
    Alt_initiale_m: float = 0
    """Altitude initiale en degrés, float"""

    # Déclaration des incréments d'angle et de vitesse
    inc_vit_x_ms: np.ndarray = None
    """Incréments en vitesse sur l'axe X calculés, de dimension (1, N)"""
    inc_vit_y_ms: np.ndarray = None
    """Incréments en vitesse sur l'axe Y calculés, de dimension (1, N)"""
    inc_vit_z_ms: np.ndarray = None
    """Incréments en vitesse sur l'axe Z calculés, de dimension (1, N)"""
    inc_angl_x_rad: np.ndarray = None
    """Incréments en angle sur l'axe X calculés, de dimension (1, N)"""
    inc_angl_y_rad: np.ndarray = None
    """Incréments en angle sur l'axe Y calculés, de dimension (1, N)"""
    inc_angl_z_rad: np.ndarray = None
    """Incréments en angle sur l'axe X=Z calculés, de dimension (1, N)"""

# Rajoutez ici les données non inertielles de votre projet !!!
    lat_gnss: np.ndarray = None
    lon_gnss: np.ndarray = None
    alt_gnss: np.ndarray = None
    nsat_gnss: np.ndarray = None
    val_gnss: np.ndarray = None
    temps_gnss: np.ndarray = None

    vor_bvs: np.ndarray = None
    dme_bvs: np.ndarray = None
    vor_dvl: np.ndarray = None
    dme_dvl: np.ndarray = None
    vor_pon: np.ndarray = None
    dme_pon: np.ndarray = None
    vor_rou: np.ndarray = None
    dme_rou: np.ndarray = None

    odo: np.ndarray = None

    def alloc_memoire(self):
        for k, v in asdict(self).items():
            if v is not None:
                continue
            setattr(self, k, np.zeros_like(self.temps_s))


@dataclass
class NavOutput:
    
    temps_s: np.ndarray = None
    """Temps du système, de dimension (1, N)"""
    Lon_calculee_deg: np.ndarray = None
    """Longitude calculée, de dimension (1, N)"""
    Lat_calculee_deg: np.ndarray = None
    """Latitude calculée, de dimension (1, N)"""
    Alt_calculee_m: np.ndarray = None
    """Altitude calculée, de dimension (1, N)"""

    # Déclaration des vitesses géographiques du porteur
    Vn_calculee_ms: np.ndarray = None
    """Vitesse Nord calculée, de dimension (1, N)"""
    Vw_calculee_ms: np.ndarray = None
    """Vitesse Ouest calculée, de dimension (1, N)"""
    Vz_calculee_ms: np.ndarray = None
    """Vitesse z calculée, de dimension (1, N)"""

    # Déclaration des attitudes et du cap du porteur
    Cap_calcule_rad: np.ndarray = None
    """Cap calculé, de dimension (1, N)"""
    Roulis_calcule_rad: np.ndarray = None
    """Roulis calculé, de dimension (1, N)"""
    Tangage_calcule_rad: np.ndarray = None
    """Tangage calculé, de dimension (1, N)"""

    # Déclaration de l'estimation du biais sur chaque axe
    Bacc_x_estime: np.ndarray = None
    """Biais accéléro sur l'axe X calculé, de dimension (1, N)"""
    Bacc_y_estime: np.ndarray = None
    """Biais accéléro sur l'axe Y calculé, de dimension (1, N)"""
    Bacc_z_estime: np.ndarray = None
    """Biais accéléro sur l'axe Z calculé, de dimension (1, N)"""

    # Déclaration de l'estimation des dérives sur chaque axe
    Dgyr_x_estime: np.ndarray = None
    """Dérive gyro sur l'axe X calculée, de dimension (1, N)"""    
    Dgyr_y_estime: np.ndarray = None
    """Dérive gyro sur l'axe Y calculée, de dimension (1, N)"""
    Dgyr_z_estime: np.ndarray = None
    """Dérive gyro sur l'axe Z calculée, de dimension (1, N)"""

    # Déclaration des variances de localisation du porteur
    Sigma_Lon_calculee_deg: np.ndarray = None
    """Variance longitude calculée, de dimension (1, N)"""
    Sigma_Lat_calculee_deg: np.ndarray = None
    """Variance latitude calculée, de dimension (1, N)"""
    Sigma_Alt_calculee_m: np.ndarray = None
    """Variance altitude calculée, de dimension (1, N)"""

    # Déclaration des variances des vitesses géographiques du porteur
    Sigma_Vn_calculee_ms: np.ndarray = None
    """Variance vitesse nord calculée, de dimension (1, N)"""
    Sigma_Vw_calculee_ms: np.ndarray = None
    """Variance vitesse ouest calculée, de dimension (1, N)"""
    Sigma_Vz_calculee_ms: np.ndarray = None
    """Variance vitesse z calculée, de dimension (1, N)"""

    # Déclaration des variances des attitudes et du cap du porteur
    Sigma_Cap_calcule_rad: np.ndarray = None
    """Variance cap calculée, de dimension (1, N)"""
    Sigma_Roulis_calcule_rad: np.ndarray = None
    """Variance roulis calculée, de dimension (1, N)"""
    Sigma_Tangage_calcule_rad: np.ndarray = None
    """Variance tangage calculée, de dimension (1, N)"""

    # Déclaration des variances des biais estimés sur chaque axe
    Sigma_Bacc_x_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe X calculée, de dimension (1, N)"""
    Sigma_Bacc_y_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe Y calculée, de dimension (1, N)"""
    Sigma_Bacc_z_estime: np.ndarray = None
    """Variance biais accéléro sur l'axe Z calculée, de dimension (1, N)"""

    # Déclaration des variances des dérives estimées sur chaque axe
    Sigma_Dgyr_x_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe X calculée, de dimension (1, N)"""
    Sigma_Dgyr_y_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe Y calculée, de dimension (1, N)"""
    Sigma_Dgyr_z_estime: np.ndarray = None
    """Variance dérive gyro sur l'axe Z calculée, de dimension (1, N)"""


    # instrumentation LDA pour vérification data inertielles et non inertielles
    Inc_Vit_Xm: np.ndarray = None
    Inc_Vit_Ym: np.ndarray = None    
    Inc_Vit_Zm: np.ndarray = None
    Inc_Ang_Xm: np.ndarray = None
    Inc_Ang_Ym: np.ndarray = None    
    Inc_Ang_Zm: np.ndarray = None
    Lat_gnss: np.ndarray = None
    Lon_gnss: np.ndarray = None
    Alt_gnss: np.ndarray = None
    nb_sat_gnss: np.ndarray = None
    val_gnss: np.ndarray = None
    dist_odo: np.ndarray = None
    vor_rou: np.ndarray = None
    dme_rou: np.ndarray = None
    vor_pon: np.ndarray = None
    dme_pon: np.ndarray = None
    vor_dvl: np.ndarray = None
    dme_dvl: np.ndarray = None
    vor_bvs: np.ndarray = None
    dme_bvs: np.ndarray = None

