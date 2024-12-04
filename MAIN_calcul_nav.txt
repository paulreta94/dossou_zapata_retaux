"""
Description
-----------

Script principal de calcul de la navigation, celui-ci permet dans une boucle de calculer tous
les paramètres de la navigation et de les écrire dans des fichiers binaires.

Pour voir le détail des calculs -> Entretien_localisation.py

Auteurs : Cédric LAURENT, Loïc DAVAIN
Créé le 10 juillet 2024

--------------------------------
"""

# import des librairies et des fichiers utiles au bon déroulé du script MAIN
from pathlib import Path
import numpy as np
from Lecture_donnees import (
    corres_tp_chemin,
    corres_traj_chemin,
    to_keep,
)
from Entretien_localisation import calcul_nav
import scipy
from Gerer_donnees import NavInput
from dataclasses import asdict

# --------------- CHOIX DE L'HYBRIDATION ET DE L'ESSAI----------------------------

# Choix de l'hybridation, choix disponibles : 'zupt', 'gps', 'odo', 'vordme'
CHOIX_HYB = "odo"
# Choix de l'essai, choix disponibles : 'aller', 'boucle', 'soutenance'
CHOIX_TRAJ = "boucle"
# CHOIX_TRAJ = 'aller'

# --------------------------------------------------------------------------------

print(
    "Configuration de l'essai, hybridation : ",
    CHOIX_HYB,
    " et trajectoire : ",
    CHOIX_TRAJ,
)
# On remonte au dossier parent du script actuel
rep_tp = Path(__file__).parent

# Le premier chemin est donc les données inertielles d'une concaténation de l'hybridation et de l'essai choisi
Premier_chemin = (
    rep_tp
    / corres_tp_chemin[CHOIX_HYB]
    / f"Donnees_inertielles_{corres_traj_chemin[CHOIX_TRAJ]}.mat"
)

# Définition des variables du premier fichier
contenu_inertiel = scipy.io.loadmat(Premier_chemin)
print(contenu_inertiel.keys())

# On remonte au dossier parent du premier chemin pour rester dans la même hybridation
rep_mat = Premier_chemin.parent

# Création d'une liste des fichiers de données non inertielles en extension mat dans ce dossier
list_chemin = list(
    rep_mat.glob(f"Donnees_non_inertielles_*{corres_traj_chemin[CHOIX_TRAJ]}.mat")
)

# Condition pour définir si la liste contient des données inertielles ou non
if len(list_chemin) == 1:
    # Si effectivement il y a des données inertielles on y applique le chemin et on load les données contenues
    Second_chemin = list_chemin[0]
    contenu_non_inertiel = scipy.io.loadmat(Second_chemin)
    print(contenu_non_inertiel.keys())
else:
    # S'il n'y a rien alors le chemin est vide et rien ne se passe
    Second_chemin = None

# Variable qui définit s'il y a des données non inertielles ou non
donnees_NI_dispo = bool(Second_chemin)

# Création et allocation mémoire
donnees_in = NavInput(temps_s=contenu_inertiel["temps_s"])
donnees_in.alloc_memoire()


# %% Conditions initiales

# Condition initiale du cap
Cap_initial_rad = 41.14 * np.pi / 180

# Position initiale du porteur (NE PAS MODIFIER)
Lon_initiale_rad = 2.110168 * np.pi / 180
Lat_initiale_rad = 49.02621 * np.pi / 180
Alt_initiale_m = 0.0

# Structure qui contient toutes les données initialisées
donnees_in.inc_vit_x_ms = contenu_inertiel["inc_vit_x_ms"]
donnees_in.inc_vit_y_ms = contenu_inertiel["inc_vit_y_ms"]
donnees_in.inc_vit_z_ms = contenu_inertiel["inc_vit_z_ms"]
donnees_in.inc_angl_x_rad = contenu_inertiel["inc_angl_x_rad"]
donnees_in.inc_angl_y_rad = contenu_inertiel["inc_angl_y_rad"]
donnees_in.inc_angl_z_rad = contenu_inertiel["inc_angl_z_rad"]
donnees_in.Cap_initial_rad = Cap_initial_rad
donnees_in.Lon_initiale_rad = Lon_initiale_rad
donnees_in.Lat_initiale_rad = Lat_initiale_rad
donnees_in.Alt_initiale_m = Alt_initiale_m

# Rajouter ici les données non inertielles
# donnees_in.lat_gnss = contenu_non_inertiel["lat_gps_deg"]
# donnees_in.lon_gnss = contenu_non_inertiel["lon_gps_deg"]
# donnees_in.alt_gnss = contenu_non_inertiel["alt_gps_m"]
# donnees_in.nsat_gnss = contenu_non_inertiel["nb_sat"]
# donnees_in.val_gnss = contenu_non_inertiel["val"]
# donnees_in.temps_gnss = contenu_non_inertiel["temps_s"]

# donnees_in.dme_bvs = contenu_non_inertiel["dist_vor_beauvais_nav_m"]
# donnees_in.vor_bvs = contenu_non_inertiel["ang_vor_beauvais_nav_deg"]
# donnees_in.dme_dvl = contenu_non_inertiel["dist_vor_deauville_nav_m"]
# donnees_in.vor_dvl = contenu_non_inertiel["ang_vor_deauville_nav_deg"]
# donnees_in.dme_pon = contenu_non_inertiel["dist_vor_pontoise_nav_m"]
# donnees_in.vor_pon = contenu_non_inertiel["ang_vor_pontoise_nav_deg"]
# donnees_in.dme_rou = contenu_non_inertiel["dist_vor_rouen_nav_m"]
# donnees_in.vor_rou = contenu_non_inertiel["ang_vor_rouen_nav_deg"]

donnees_in.odo = contenu_non_inertiel["Dist_Odo_m"]


# %% boucle itérative sur les données

# Boucle de calcul, sortant la nouvelle structure avec les données calculées
donnees_out = calcul_nav(donnees_in, donnees_NI_dispo)

# %% Écriture des fichiers binaires

print("Écriture des données en cours...")

# Création d'un premier dico de données (NE PAS MODIFIER !)
nav_prof = {}
for k in to_keep:
    nav_prof[k] = getattr(donnees_out, k)

# Ecriture du premier dico dans un fichier binaire
scipy.io.savemat("Nav_calculee_etudiants_pour_prof.mat", nav_prof)

# Création d'un second dico (à modifier pour rajouter des données)
donnees_etudiants = asdict(donnees_out)

# Ecriture du second dico dans un fichier binaire
scipy.io.savemat("Nav_calculee_etudiants_modifiable.mat", donnees_etudiants)

print("Écriture terminée, merci d'avoir patienté.")
