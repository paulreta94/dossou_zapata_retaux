"""
Description
-----------

Script principal de tracé des figures, celui-ci permet d'importer les fichiers binaires créés et de
ressortir toutes les figures utiles au tracé et à la compréhension de la nav calculée

Pour voir le détail des figures -> trace_figures.py

Auteurs : Cédric LAURENT, Loïc DAVAIN
Créé le 10 juillet 2024

--------------------------------
"""
#import des librairies et des fichiers utiles au bon déroulé du script MAIN
from trace_figures import (trace_figure_nav_pontoise,
                           trace_figure_nav_fecamp,
                           trace_erreurs_position,
                           trace_figure_vitesses,
                           trace_erreurs_vitesse,
                           trace_figure_attitudes,
                           trace_erreurs_attitude,
                           calcul_erreurs_position,
                           calcul_erreurs_vitesse,
                           calcul_erreurs_attitude,
                           trace_increments,
                           trace_positions_gnss,
                           trace_data_vordme,
                           trace_positions_vordme,
)
import scipy
from pathlib import Path
from Lecture_donnees import (
    def_map,
    corres_traj_chemin,
)
import webbrowser

#--------------------------- CHOIX DE L'ESSAI---------------------------------

# Choix de l'essai, choix disponibles : 'aller', 'boucle'
CHOIX_TRAJ = 'boucle'
# CHOIX_TRAJ = 'aller'
# Choix de la sauvegarde des figures, choix disponibles : True ou False (booléen)
SAVE_FIG = False

#-----------------------------------------------------------------------------

print ("Import des fichiers de données en cours...")

# Lecture du fichier binaire de la navigation calculée
contenu_nav_calculee = scipy.io.loadmat('Nav_calculee_etudiants_modifiable.mat')

# On remonte au dossier parent du script actuel
rep_tp = Path(__file__).parent
# Le chemin va chercher la navigation parfaite de l'essai choisi
chemin_nav_parfaite = rep_tp / '02-Navigations_parfaites' / f"Nav_reference_{corres_traj_chemin[CHOIX_TRAJ]}.mat"
# On importe les données contenues dans le fichier
contenu_nav_parfaite = scipy.io.loadmat(chemin_nav_parfaite)
# On récupère le nom du fichier
file_name = f"Nav_reference_{corres_traj_chemin[CHOIX_TRAJ]}.mat"

#Déduction de la carte à utiliser en fonction du nom du fichier
map_utile = def_map(file_name)

print("Fin de l'import de données, début de tracé et de calcul des figures.")

#%% Tracé position + erreurs de position
# Tracé des navigations parfaite et calculée en 2D dans une fenêtre HTML
if map_utile == 'Pontoise':
    trace_figure_nav_pontoise(contenu_nav_calculee["Lon_calculee_deg"],
                            contenu_nav_calculee["Lat_calculee_deg"],
                            contenu_nav_parfaite["longitude_ins"],
                            contenu_nav_parfaite["latitude_ins"],
                            contenu_nav_calculee["Lon_gnss"],
                            contenu_nav_calculee["Lat_gnss"])
elif map_utile == 'Fecamp':
    trace_figure_nav_fecamp(contenu_nav_calculee["Lon_calculee_deg"],
                            contenu_nav_calculee["Lat_calculee_deg"],
                            contenu_nav_parfaite["longitude_ins"],
                            contenu_nav_parfaite["latitude_ins"])

# Calcul des erreurs de position de la navigation calculée par rapport à la navigation parfaite
# err_pos_x, err_pos_y, err_pos_z = calcul_erreurs_position(contenu_nav_parfaite["longitude_ins"],
#                                                         contenu_nav_parfaite["latitude_ins"],
#                                                         contenu_nav_parfaite["altitude_ins"],
#                                                         contenu_nav_calculee["Lon_calculee_deg"],
#                                                         contenu_nav_calculee["Lat_calculee_deg"],
#                                                         contenu_nav_calculee["Alt_calculee_m"])

# Tracé des erreurs de position calculées précédemment
# fig1 = trace_erreurs_position(contenu_nav_calculee["temps_s"],err_pos_x,err_pos_y,err_pos_z)
# Afficher la figure dans une fenêtre à part


#%% Tracé vitesses + erreurs de vitesse
# Tracé des vitesses géographiques du porteur en fonction du temps
# fig2 = trace_figure_vitesses(contenu_nav_calculee["temps_s"],
#                             contenu_nav_calculee["Vn_calculee_ms"],
#                             contenu_nav_calculee["Vw_calculee_ms"],
#                             contenu_nav_calculee["Vz_calculee_ms"])
# Afficher la figure dans une fenêtre à part


#Calcul des erreurs de vitesse entre les vitesses calculées et parfaites
# err_vit_x, err_vit_y, err_vit_z = calcul_erreurs_vitesse(contenu_nav_parfaite["vit_ins_n"],
#                                                         contenu_nav_parfaite["vit_ins_w"],
#                                                         contenu_nav_parfaite["vit_ins_z"],
#                                                         contenu_nav_calculee["Vn_calculee_ms"],
#                                                         contenu_nav_calculee["Vw_calculee_ms"],
#                                                         contenu_nav_calculee["Vz_calculee_ms"])

# Tracé des erreurs de vitesse en fonction du temps
# fig3 = trace_erreurs_vitesse(contenu_nav_calculee["temps_s"],err_vit_x, err_vit_y, err_vit_z)

#%% Tracé attitudes + erreurs d'attitudes
# Tracé des attitudes et du cap du porteur en fonction du temps
# fig4 = trace_figure_attitudes(contenu_nav_calculee["temps_s"],
#                             contenu_nav_calculee["Cap_calcule_rad"],
#                             contenu_nav_calculee["Roulis_calcule_rad"],
#                             contenu_nav_calculee["Tangage_calcule_rad"])

# Calcul des erreurs d'attitudes et de cap entre celles calculées et parfaites
# err_att_cap, err_att_rou, err_att_tan = calcul_erreurs_attitude(contenu_nav_parfaite["cap_ins"],
#                                                                 contenu_nav_parfaite["roulis_ins"],
#                                                                 contenu_nav_parfaite["tangage_ins"],
#                                                                 contenu_nav_calculee["Cap_calcule_rad"],
#                                                                 contenu_nav_calculee["Roulis_calcule_rad"],
#                                                                 contenu_nav_calculee["Tangage_calcule_rad"])

# Tracé des erreurs d'attitudes et de cap en fonction du temps
# fig5 = trace_erreurs_attitude(contenu_nav_calculee["temps_s"],err_att_cap, err_att_rou, err_att_tan)

# fig6 = trace_increments(contenu_nav_calculee["temps_s"],
#                     contenu_nav_calculee["Inc_Vit_Xm"],contenu_nav_calculee["Inc_Vit_Ym"],contenu_nav_calculee["Inc_Vit_Zm"],
#                     contenu_nav_calculee["Inc_Ang_Xm"],contenu_nav_calculee["Inc_Ang_Ym"],contenu_nav_calculee["Inc_Ang_Zm"],)

# fig7 = trace_positions_gnss(contenu_nav_calculee["temps_s"],
#                     contenu_nav_calculee["Lat_gnss"],contenu_nav_calculee["Lon_gnss"],contenu_nav_calculee["Alt_gnss"],
#                     contenu_nav_parfaite["latitude_ins"],contenu_nav_parfaite["longitude_ins"],contenu_nav_parfaite["altitude_ins"])

fig8 = trace_data_vordme(contenu_nav_calculee["temps_s"],
                    contenu_nav_calculee["vor_bvs"],contenu_nav_calculee["dme_bvs"],
                    contenu_nav_calculee["vor_dvl"],contenu_nav_calculee["dme_dvl"],
                    contenu_nav_calculee["vor_pon"],contenu_nav_calculee["dme_pon"],
                    contenu_nav_calculee["vor_rou"],contenu_nav_calculee["dme_rou"])

fig9 = trace_positions_vordme(contenu_nav_calculee["temps_s"],
                    contenu_nav_parfaite["latitude_ins"],contenu_nav_parfaite["longitude_ins"],contenu_nav_parfaite["altitude_ins"],
                    contenu_nav_calculee["vor_bvs"],contenu_nav_calculee["dme_bvs"],
                    contenu_nav_calculee["vor_dvl"],contenu_nav_calculee["dme_dvl"],
                    contenu_nav_calculee["vor_pon"],contenu_nav_calculee["dme_pon"],
                    contenu_nav_calculee["vor_rou"],contenu_nav_calculee["dme_rou"])

print("Fin d'appel des figures, vous pouvez les visualiser maintenant.")

#%% Enregistrement des figures

if SAVE_FIG == True :
    # Enregistrer les figures dans le répertoire
    # Enregistrement des figures en HTML
    # fig1.write_html("Erreurs_de_position.html")
    # fig2.write_html("Vitesses_géographiques.html")
    # fig3.write_html("Erreurs_de_vitesse.html")
    # fig4.write_html("Attitudes.html")
    # fig5.write_html("Erreurs_d_attitudes.html")

    # Ouvrir la figure dans le navigateur
    webbrowser.open("Erreurs_de_position.html")
    webbrowser.open("Vitesses_géographiques.html")
    webbrowser.open("Erreurs_de_vitesse.html")
    webbrowser.open("Attitudes.html")
    webbrowser.open("Erreurs_d_attitudes.html")

else : 
    # Affichage des figures dans le navigateur
    # fig1.show()
    # fig2.show()
    # fig3.show()
    # fig4.show()
    # fig5.show()
    # fig6.show()
    # fig7.show()
    fig8.show()
    fig9.show()
