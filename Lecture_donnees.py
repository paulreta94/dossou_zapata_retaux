"""
Description
-----------

Ce fichier possède deux dictionnaires qui permettent de choisir un chemin
vers un fichier à l'aide des choix disponibles. Une fonction est aussi
disponible et permet de sélectionner la map correspondante à l'essai choisi

Fonctions Disponibles :
   
   - def_map

Dictionnaires Disponibles :
   
   - corres_tp_chemin : Permet de sélectionner l'hybridation choisie
   - corres_traj_chemin : Permet de sélectionner le trajet voulu
   
Liste Disponible :
    
    - to_keep : liste des champs à garder dans la structure NavOutput
    
Auteurs : Cédric LAURENT, Loïc DAVAIN
Créé le 10 juillet 2024

--------------------------------
"""
#Dictionnaire permettant de choisir l'hybridation choisie
corres_tp_chemin = {
    'zupt': "03-Données_zupt",
    'gps': "04-Données_GPS",
    'odo': "05-Données_Odometre",
    'vordme': "06-Données_VORDME",
}

#Dictionnaire permettant de choisir l'essai voulu
corres_traj_chemin = {
    'aller': "aller",
    'boucle': "boucle_1",
    'soutenance': "boucle_2"
}

#Liste contenant les champs à garder pour le fichier à destination du prof (NE PAS MODIFIER)
to_keep = [
    "temps_s",
    "Lon_calculee_deg",
    "Lat_calculee_deg",
    "Alt_calculee_m",
    "Vn_calculee_ms",
    "Vw_calculee_ms",
    "Vz_calculee_ms",
    "Cap_calcule_rad",
    "Roulis_calcule_rad",
    "Tangage_calcule_rad",
    "Bacc_x_estime",
    "Bacc_y_estime",
    "Bacc_z_estime",
    "Dgyr_x_estime",
    "Dgyr_y_estime",
    "Dgyr_z_estime",
    "Sigma_Lon_calculee_deg",
    "Sigma_Lat_calculee_deg",
    "Sigma_Alt_calculee_m",
    "Sigma_Vn_calculee_ms",
    "Sigma_Vw_calculee_ms",
    "Sigma_Vz_calculee_ms",
    "Sigma_Cap_calcule_rad",
    "Sigma_Roulis_calcule_rad",
    "Sigma_Tangage_calcule_rad",
    "Sigma_Bacc_x_estime",
    "Sigma_Bacc_y_estime",
    "Sigma_Bacc_z_estime",
    "Sigma_Dgyr_x_estime",
    "Sigma_Dgyr_y_estime",
    "Sigma_Dgyr_z_estime"]

def def_map(name):

    r"""Script qui permet de définir la carte qu'il faudra afficher lors du tracé de la nav

    Parameters
    ----------
    name : str
        nom du fichier de référence sélectionné

    Returns
    -------
    map_a_utiliser : str
        Variable prenant le nom voulu pour afficher la carte correspondante

    """

    #Test sur le nom du fichier de la navigation de référence choisie
    if name == 'Nav_reference_boucle_1.mat':
        #Si la navigation est une boucle alors on affiche la carte de Pontoise
        map_a_utiliser = 'Pontoise'
    else:
        #Si la navigation est un autre test alors on affiche la carte entre Cergy et Fécamp
        map_a_utiliser= 'Fecamp'
    return map_a_utiliser
