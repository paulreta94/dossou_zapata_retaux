"""
Description
-----------

Package de fonctions afin de tracer et sortir toutes les figures nécessaires à
la compréhension du TP

Fonctions Disponibles :
   
   - Tracé de la navigation partant de Pontoise ou de Fecamp
   - Calculs des erreurs de position
   - Tracé des erreurs de position
   - Tracé des vitesses géographiques
   - Calculs des erreurs de vitesse
   - Tracé des erreurs de vitesse
   - Tracé des attitudes et cap
   - Calculs des erreurs d'attitudes et cap
   - Tracé des erreurs de d'attitudes et cap
   

Auteurs : Cédric LAURENT, Loïc DAVAIN
Créé le 10 juillet 2024

--------------------------------
"""
#Import des librairies nécessaires au tracé des figures
import plotly.graph_objects as go
import numpy as np
import base64
import webbrowser
from plotly.subplots import make_subplots

#%% POSITION

def trace_figure_nav_pontoise(x,y,x_ref,y_ref):

    r"""Ce script trace dans une fenêtre html le tracé calculé et la référence sur le 
        trajet de Pontoise

    Parameters
    ----------
    x : np.ndarray
        vecteur de la longitude de la nav calculée [deg] (dim (1,N))
    y : np.ndarray
        vecteur de la latitude de la nav calculée [deg] (dim (1,N))
    x_ref : np.ndarray
        vecteur de la longitude de la nav de référence [deg] (dim (1,N))
    y_ref : np.ndarray
        vecteur de la latitude de la nav de référence [deg] (dim (1,N))

    Returns
    -------
    Trace_nav_2D_pontoise.html : figure html
        Tracé de la navigation

    """
    #Ouverture du png de la carte en mode lecture
    with open(r"01-Cartes\map_ilems.PNG", "rb") as png:
        #Encodage en base 64 de la carte au fur et à mesure de sa lecture
        b64 = base64.b64encode(png.read())

    # Chargement de l'image
    img = go.layout.Image(
        source=f"data:image/png;base64,{b64.decode()}",
        xref="x",
        yref="y",
        #Coordonnées du coin supérieur gauche de la carte
        x=1.728479,
        y=49.224106555952380,
        #Différence entre Gmax et Gmin de la carte
        sizex=0.5771341310408928,
        #Différence en Latmax et Latmin de la carte
        sizey=0.2442005559523821,
        sizing="stretch",
        opacity=1,
        layer="below"
    )

    # Données de la nav parfaite pour le tracé de celle-ci
    xref = x_ref[0,:]
    yref = y_ref[0,:]
    # Données de la nav calculée pour le tracé de celle-ci
    x = x[0,:]
    y = y[0,:]

    # x_gnss = x_gps[0,:]
    # y_gnss = y_gps[0,:]  
    # Création de la figure
    fig = go.Figure()

    # Ajout de l'image
    fig.add_layout_image(img)

    # Ajout du tracé de la nav de référence
    fig.add_trace(go.Scatter(x=xref, y=yref, mode='lines', name='Référence'))
    # Ajout du tracé de la nav calculée
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='INS'))
    # fig.add_trace(go.Scatter(x=x_gnss, y=y_gnss, mode='lines', name='GPS'))
    # Configuration des axes de la figure pour correspondre à ceux de l'image
    fig.update_xaxes(range=[1.728479, 2.305613131040893])
    fig.update_yaxes(range=[48.979906, 49.224106555952380])

    # Mise à jour de la disposition pour inclure la légende
    fig.update_layout(
        #titre de la figure
        title="Tracé navigation Référence/INS",
        #titre de l'axe x
        xaxis_title="Longitude [deg]",
        #titre de l'axe y
        yaxis_title="Latitude [deg]",
        #titre de la légende
        legend_title="Légende",
        legend=dict(
            x=1,  # Position X de la légende
            y=1   # Position Y de la légende
        ),
        showlegend=True,
    )

    # Enregistrement de la figure en HTML
    fig.write_html("Trace_nav_2D_pontoise.html")
    # Ouvrir la figure dans le navigateur
    webbrowser.open("Trace_nav_2D_pontoise.html")

def trace_figure_nav_fecamp(x,y,x_ref,y_ref):

    r"""Ce script trace dans une fenêtre html le tracé calculé et la référence sur le
        trajet de Fecamp

    Parameters
    ----------
    x : np.ndarray
        vecteur de la longitude de la nav calculée [deg] (dim (1,N))
    y : np.ndarray
        vecteur de la latitude de la nav calculée [deg] (dim (1,N))
    x_ref : np.ndarray
        vecteur de la longitude de la nav de référence [deg] (dim (1,N))
    y_ref : np.ndarray
        vecteur de la latitude de la nav de référence [deg] (dim (1,N))

    Returns
    -------
    Trace_nav_2D_fecamp.html : figure html
        Tracé de la navigation

    """

    #Ouverture du png de la carte en mode lecture
    with open(r"01-Cartes\map_fecamp.PNG", "rb") as png:
        #Encodage en base 64 de la carte au fur et à mesure de sa lecture
        b64 = base64.b64encode(png.read())

    # Chargement de l'image
    img = go.layout.Image(
        source=f"data:image/png;base64,{b64.decode()}",
        xref="x",
        yref="y",
        #Coordonnées du coin supérieur gauche de la carte
        x=0.317211,
        y=49.787612490196075,
        #Différence entre Gmax et Gmin de la carte
        sizex=1.9932976035555563,
        #Différence en Latmax et Latmin de la carte
        sizey=0.819765490196076,
        sizing="stretch",
        opacity=1,
        layer="below"
    )

    # Données de la nav parfaite pour le tracé de celle-ci
    xref = x_ref[0,:]
    yref = y_ref[0,:]
    # Données de la nav calculée pour le tracé de celle-ci
    x = x[0,:]
    y = y[0,:]
    # Création de la figure
    fig = go.Figure()

    # Ajout de l'image
    fig.add_layout_image(img)

    # Ajout du tracé de la nav de référence
    fig.add_trace(go.Scatter(x=xref, y=yref, mode='lines', name='Référence'))
    # Ajout du tracé de la nav calculée
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='INS'))
    # Configuration des axes de la figure pour correspondre à ceux de l'image
    fig.update_xaxes(range=[0.317211, 2.310508603555556])
    fig.update_yaxes(range=[48.967847, 49.787612490196075])

    # Mise à jour de la disposition pour inclure la légende
    fig.update_layout(
        #titre de la figure
        title="Tracé navigation Référence/INS",
        #titre de l'axe x
        xaxis_title="Longitude [deg]",
        #titre de l'axe y
        yaxis_title="Latitude [deg]",
        #titre de la légende
        legend_title="Légende",
        legend=dict(
            x=1,  # Position X de la légende
            y=1   # Position Y de la légende
        ),
        showlegend=True,
    )

    # Enregistrement de la figure en HTML
    fig.write_html("Trace_nav_2D_fecamp.html")
    # Ouvrir la figure dans le navigateur
    webbrowser.open("Trace_nav_2D_fecamp.html")


def calcul_erreurs_position(ref_x, ref_y, ref_z, cal_x, cal_y, cal_z):

    r"""Ce script calcule les erreurs de position sur chaque axe de la navigation

    Parameters
    ----------
    ref_x : np.ndarray
        vecteur de la longitude de la nav de référence [deg] (dim (1,N))
    ref_y : np.ndarray
        vecteur de la latitude de la nav de référence [deg] (dim (1,N))
    ref_z : np.ndarray
        vecteur de l'altitude de la nav de référence [deg] (dim (1,N))
    cal_x : np.ndarray
        vecteur de la longitude de la nav calculée [deg] (dim (1,N))
    cal_y : np.ndarray
        vecteur de la latitude de la nav calculée [deg] (dim (1,N))
    cal_z : np.ndarray
        vecteur de l'altitude de la nav calculée [deg] (dim (1,N))
        
    Returns
    -------
    err_x : np.ndarray
        vecteur de l'erreur de position selon l'axe x [g] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de position selon l'axe y [g] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de position selon l'axe z [g] (dim (1,N))

    """

    #Constante rayon terrestre
    Rt = 6378000.0
    #Calcul de l'erreur de position en longitude
    err_x = (ref_x - cal_x)*(np.pi/180)*Rt*np.cos(np.radians(ref_y))
    #Calcul de l'erreur de position en latitude
    err_y = (ref_y - cal_y)*(np.pi/180)*Rt
    #Calcul de l'erreur de position en altitude
    err_z = ref_z - cal_z
    #Renvoie des 3 erreurs calculées
    return err_x, err_y, err_z

def trace_erreurs_position(t, err_x, err_y, err_z):
    r"""Ce script trace les erreurs de position sur chaque axe de la navigation avec Plotly.

    Parameters
    ----------
    t : np.ndarray
        vecteur temps du système [s] (dim (1,N))
    err_x : np.ndarray
        vecteur de l'erreur de position selon l'axe x [m] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de position selon l'axe y [m] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de position selon l'axe z [m] (dim (1,N))
        
    Returns
    -------
    Erreurs de position : figure 
        Tracé des erreurs avec 3 subplots pour chaque axe via Plotly.
    """
    # Création d'une figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                       subplot_titles=("Ect Err Position X [m]", 
                                       "Ect Err Position Y [m]", 
                                       "Ect Err Position Z [m]"))

    # Ajout de la première courbe (Erreur position X)
    fig.add_trace(go.Scatter(x=t[0, :], y=err_x[0, :],
                            mode='lines', name='Ect Err Position X [m]',
                            line=dict(color='black')), row=1, col=1)

    # Ajout de la deuxième courbe (Erreur position Y)
    fig.add_trace(go.Scatter(x=t[0, :], y=err_y[0, :],
                            mode='lines', name='Ect Err Position Y [m]',
                            line=dict(color='blue')), row=2, col=1)

    # Ajout de la troisième courbe (Erreur position Z)
    fig.add_trace(go.Scatter(x=t[0, :], y=err_z[0, :],
                            mode='lines', name='Ect Err Position Z [m]',
                            line=dict(color='red')), row=3, col=1)

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_yaxes(title_text="Ect Err Position X [m]", row=1, col=1)
    fig.update_yaxes(title_text="Ect Err Position Y [m]", row=2, col=1)
    fig.update_yaxes(title_text="Ect Err Position Z [m]", row=3, col=1)
    
    # Mise à jour du layout général
    fig.update_layout(height=800, title_text="Erreurs de position")
    
    # Affichage de la figure
    return fig
    
#%% VITESSES
def trace_figure_vitesses(t, vn, vw, vz):
    r"""Ce script trace les vitesses géographiques nord, ouest et z de la navigation calculée avec Plotly.

    Parameters
    ----------
    t : np.ndarray
        vecteur temps du système [s] (dim (1,N))
    vn : np.ndarray
        vecteur de la vitesse géographique nord [m/s] (dim (1,N))
    vw : np.ndarray
        vecteur de la vitesse géographique ouest [m/s] (dim (1,N))
    vz : np.ndarray
        vecteur de la vitesse géographique z [m/s] (dim (1,N))
        
    Returns
    -------
    Vitesses Géographiques : figure 
        Tracé des vitesses avec 3 subplots pour chaque axe via Plotly.
    """

    # Création de la figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Vit Nord [m/s]", 
                                        "Vit Ouest [m/s]", 
                                        "Vit Z Up [m/s]"))

    # Ajout de la courbe de la vitesse nord
    fig.add_trace(go.Scatter(x=t[0, :], y=vn[0, :],
                             mode='lines', name='Vit Nord [m/s]',
                             line=dict(color='blue')), row=1, col=1)

    # Ajout de la courbe de la vitesse ouest
    fig.add_trace(go.Scatter(x=t[0, :], y=vw[0, :],
                             mode='lines', name='Vit Ouest [m/s]',
                             line=dict(color='green')), row=2, col=1)

    # Ajout de la courbe de la vitesse z
    fig.add_trace(go.Scatter(x=t[0, :], y=vz[0, :],
                             mode='lines', name='Vit Z Up [m/s]',
                             line=dict(color='red')), row=3, col=1)

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_yaxes(title_text="Vit Nord [m/s]", row=1, col=1)
    fig.update_yaxes(title_text="Vit Ouest [m/s]", row=2, col=1)
    fig.update_yaxes(title_text="Vit Z Up [m/s]", row=3, col=1)

    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="Vitesses Géographiques",
                      title_x=0.5)
    return fig

def calcul_erreurs_vitesse(ref_x, ref_y, ref_z, cal_x, cal_y, cal_z):

    r"""Ce script calcule les erreurs de vitesse sur chaque axe de la navigation

    Parameters
    ----------
    ref_x : np.ndarray
        vecteur de la vitesse géographique nord de la nav de référence [m/s] (dim (1,N))
    ref_y : np.ndarray
        vecteur de la vitesse géographique ouest de la nav de référence [m/s] (dim (1,N))
    ref_z : np.ndarray
        vecteur de la vitesse géographique z de la nav de référence [m/s] (dim (1,N))
    cal_x : np.ndarray
        vecteur de la vitesse géographique nord de la nav calculée [m/s] (dim (1,N))
    cal_y : np.ndarray
        vecteur de la vitesse géographique ouest de la nav calculée [m/s] (dim (1,N))
    cal_z : np.ndarray
        vecteur de la vitesse géographique z de la nav calculée [m/s] (dim (1,N))
        
    Returns
    -------
    err_x : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe x [m/s] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe y [m/s] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe z [m/s] (dim (1,N))

    """

    #Calcul de l'erreur de vitesse en x (nord)
    err_x = ref_x - cal_x
    #Calcul de l'erreur de vitesse en y (ouest)
    err_y = ref_y - cal_y
    #Calcul de l'erreur de vitesse en z
    err_z = ref_z - cal_z

    #Renvoie des 3 erreurs calculées
    return err_x, err_y, err_z


def trace_erreurs_vitesse(t, err_x, err_y, err_z):
    r"""Ce script trace les erreurs de vitesse sur chaque axe de la navigation avec Plotly.

    Parameters
    ----------
    t : np.ndarray
        vecteur temps du système [s] (dim (1,N))
    err_x : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe x [m/s] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe y [m/s] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de vitesse selon l'axe z [m/s] (dim (1,N))
        
    Returns
    -------
    Erreurs de vitesse : figure 
        Tracé des erreurs avec 3 subplots pour chaque axe via Plotly.
    """

    # Création de la figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Ect Err Vitesse X [m/s]", 
                                        "Ect Err Vitesse Y [m/s]", 
                                        "Ect Err Vitesse Z [m/s]"))

    # Ajout de la courbe d'erreur selon l'axe x
    fig.add_trace(go.Scatter(x=t[0, :], y=err_x[0, :],
                             mode='lines', name='Ect Err Vitesse X [m/s]',
                             line=dict(color='black')), row=1, col=1)

    # Ajout de la courbe d'erreur selon l'axe y
    fig.add_trace(go.Scatter(x=t[0, :], y=err_y[0, :],
                             mode='lines', name='Ect Err Vitesse Y [m/s]',
                             line=dict(color='blue')), row=2, col=1)

    # Ajout de la courbe d'erreur selon l'axe z
    fig.add_trace(go.Scatter(x=t[0, :], y=err_z[0, :],
                             mode='lines', name='Ect Err Vitesse Z [m/s]',
                             line=dict(color='red')), row=3, col=1)

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_yaxes(title_text="Ect Err Vitesse X [m/s]", row=1, col=1)
    fig.update_yaxes(title_text="Ect Err Vitesse Y [m/s]", row=2, col=1)
    fig.update_yaxes(title_text="Ect Err Vitesse Z [m/s]", row=3, col=1)

    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="Erreurs de vitesse",
                      title_x=0.5)
    return fig

#%% ATTITUDES

def trace_figure_attitudes(t, cap, rou, tan):
    r"""Ce script trace les attitudes et le cap du porteur de la navigation calculée avec Plotly.

    Parameters
    ----------
    t : np.ndarray
        vecteur temps du système [s] (dim (1,N))
    cap : np.ndarray
        vecteur du cap [rad] (dim (1,N))
    rou : np.ndarray
        vecteur du roulis [rad] (dim (1,N))
    tan : np.ndarray
        vecteur du tangage [rad] (dim (1,N))
        
    Returns
    -------
    Attitudes du Porteur : figure 
        Tracé des attitudes avec 3 subplots pour chaque axe via Plotly.
    """

    # Conversion des angles en degrés
    cap_deg = cap * 180 / np.pi
    rou_deg = rou * 180 / np.pi
    tan_deg = tan * 180 / np.pi

    # Création de la figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Cap [deg]", 
                                        "Roulis [deg]", 
                                        "Tangage [deg]"))

    # Ajout de la courbe du cap en degrés
    fig.add_trace(go.Scatter(x=t[0, :], y=cap_deg[0, :],
                             mode='lines', name='Cap [deg]',
                             line=dict(color='blue')), row=1, col=1)

    # Ajout de la courbe du roulis en degrés
    fig.add_trace(go.Scatter(x=t[0, :], y=rou_deg[0, :],
                             mode='lines', name='Roulis [deg]',
                             line=dict(color='green')), row=2, col=1)

    # Ajout de la courbe du tangage en degrés
    fig.add_trace(go.Scatter(x=t[0, :], y=tan_deg[0, :],
                             mode='lines', name='Tangage [deg]',
                             line=dict(color='red')), row=3, col=1)

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_yaxes(title_text="Cap [deg]", row=1, col=1)
    fig.update_yaxes(title_text="Roulis [deg]", row=2, col=1)
    fig.update_yaxes(title_text="Tangage [deg]", row=3, col=1)

    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="Attitudes du Porteur",
                      title_x=0.5)
    return fig

def calcul_erreurs_attitude(ref_x, ref_y, ref_z, cal_x, cal_y, cal_z):

    r"""Ce script calcule les erreurs d'attitude sur chaque axe de la navigation
    
    Attention à bien mettre les paramètres dans le bon ordre ! 
    Sinon la figure des erreurs n'aura pas les bons arguments et les plot seront mélangés
    
    Parameters
    ----------
    ref_x : np.ndarray
        vecteur du cap de la nav de référence [deg] (dim (1,N))
    ref_y : np.ndarray
        vecteur du roulis de la nav de référence [deg] (dim (1,N))
    ref_z : np.ndarray
        vecteur du tangage de la nav de référence [deg] (dim (1,N))
    cal_x : np.ndarray
        vecteur du cap de la nav calculée [rad] (dim (1,N))
    cal_y : np.ndarray
        vecteur du roulis de la nav calculée [rad] (dim (1,N))
    cal_z : np.ndarray
        vecteur du tangage de la nav calculée [rad] (dim (1,N))
        
    Returns
    -------
    err_x : np.ndarray
        vecteur de l'erreur de cap [mrad] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de roulis [mrad] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de tangage [mrad] (dim (1,N))

    """

    #Conversion du cap parfait en radians
    ref_x = ref_x *(np.pi/180)
    #Conversion du roulis parfait en radians
    ref_y = ref_y *(np.pi/180)
    #Conversion du tangage parfait en radians
    ref_z = ref_z *(np.pi/180)

    #Calcul de l'erreur de cap en mrad
    err_x = (np.unwrap(ref_x) - cal_x)*1000
    #Calcul de l'erreur de roulis en mrad
    err_y = (ref_y - cal_y)*1000
    #Calcul de l'erreur de tangage en mrad
    err_z = (ref_z - cal_z)*1000

    #Renvoie des 3 erreurs calculées
    return err_x, err_y, err_z


def trace_erreurs_attitude(t, err_x, err_y, err_z):
    r"""Ce script trace les erreurs d'attitude sur chaque axe de la navigation calculée avec Plotly.

    Parameters
    ----------
    t : np.ndarray
        vecteur temps du système [s] (dim (1,N))
    err_x : np.ndarray
        vecteur de l'erreur de cap [mrad] (dim (1,N))
    err_y : np.ndarray
        vecteur de l'erreur de roulis [mrad] (dim (1,N))
    err_z : np.ndarray
        vecteur de l'erreur de tangage [mrad] (dim (1,N))
        
    Returns
    -------
    Erreurs d'attitudes : figure 
        Tracé des erreurs avec 3 subplots pour chaque axe via Plotly.
    """

    # Création de la figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Erreur Cap [mrad]", 
                                        "Erreur Roulis [mrad]", 
                                        "Erreur Tangage [mrad]"))

    # Ajout de la courbe d'erreur du cap en mrad
    fig.add_trace(go.Scatter(x=t[0, :], y=err_x[0, :],
                             mode='lines', name='Erreur Cap [mrad]',
                             line=dict(color='blue')), row=1, col=1)

    # Ajout de la courbe d'erreur du roulis en mrad
    fig.add_trace(go.Scatter(x=t[0, :], y=err_y[0, :],
                             mode='lines', name='Erreur Roulis [mrad]',
                             line=dict(color='green')), row=2, col=1)

    # Ajout de la courbe d'erreur du tangage en mrad
    fig.add_trace(go.Scatter(x=t[0, :], y=err_z[0, :],
                             mode='lines', name='Erreur Tangage [mrad]',
                             line=dict(color='red')), row=3, col=1)

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_yaxes(title_text="Erreur Cap [mrad]", row=1, col=1)
    fig.update_yaxes(title_text="Erreur Roulis [mrad]", row=2, col=1)
    fig.update_yaxes(title_text="Erreur Tangage [mrad]", row=3, col=1)

    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="Erreurs d'Attitudes",
                      title_x=0.5)
    return fig


def trace_increments(t, inc_vit_x, inc_vit_y, inc_vit_z,inc_ang_x,inc_ang_y,inc_ang_z):
    fig = make_subplots(rows=3, cols=2, shared_xaxes=True,
                        subplot_titles=("Increment Vit X [m/s]", 
                                        "Increment Angle X [rad]", 
                                        "Increment Vit Y [m/s]", 
                                        "Increment Angle Y [rad]", 
                                        "Increment Vit Z [m/s]",
                                        "Increment Angle Z [rad]"))

    fig.add_trace(go.Scatter(x=t[0, :], y=inc_vit_x[0, :],
                             mode='lines', name='DV X [m/s]',
                             line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=inc_vit_y[0, :],
                             mode='lines', name='DV X [m/s]',
                             line=dict(color='green')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=inc_vit_z[0, :],
                             mode='lines', name='DV X [m/s]',
                             line=dict(color='red')), row=3, col=1)     

    fig.add_trace(go.Scatter(x=t[0, :], y=inc_ang_x[0, :],
                             mode='lines', name='DA X [rad]',
                             line=dict(color='blue')), row=1, col=2)
    fig.add_trace(go.Scatter(x=t[0, :], y=inc_ang_y[0, :],
                             mode='lines', name='DA X [rad]',
                             line=dict(color='green')), row=2, col=2)
    fig.add_trace(go.Scatter(x=t[0, :], y=inc_ang_z[0, :],
                             mode='lines', name='DA X [rad]',
                             line=dict(color='red')), row=3, col=2)     

    mvx = np.mean(inc_vit_x[0,1000:3000])*100.0
    mvy = np.mean(inc_vit_y[0,1000:3000])*100.0
    mvz = np.mean(inc_vit_z[0,1000:3000])*100.0
    max = np.mean(inc_ang_x[0,1000:3000])*100.0*180.0/3.1415926*3600.0
    may = np.mean(inc_ang_y[0,1000:3000])*100.0*180.0/3.1415926*3600.0
    maz = np.mean(inc_ang_z[0,1000:3000])*100.0*180.0/3.1415926*3600.0
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)
    fig.update_xaxes(title_text="Temps [s]", row=3, col=2)
    fig.update_yaxes(title_text="gamma x ~ "+str(mvx)+" m/s²", row=1, col=1)
    fig.update_yaxes(title_text="gamma y ~ "+str(mvy)+" m/s²", row=2, col=1)
    fig.update_yaxes(title_text="gamma z ~ "+str(mvz)+" m/s²", row=3, col=1)
    fig.update_yaxes(title_text="omega x ~ "+str(max)+" deg/h", row=1, col=2)
    fig.update_yaxes(title_text="omega y ~ "+str(may)+" deg/h", row=2, col=2)
    fig.update_yaxes(title_text="omega z ~ "+str(maz)+" deg/h", row=3, col=2)         

    return fig


def trace_positions_gnss(t, Lg,Gg,Zg,Lr,Gr,Zr):
# Création de la figure avec sous-graphiques (3 lignes, 1 colonne)
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("Lat [deg]", 
                                        "lon [deg]", 
                                        "alt [m]"))

    fig.add_trace(go.Scatter(x=t[0, :], y=Lg[0, :],mode='lines', name='latitude gnss [mrad]',line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=Lr[0, :],mode='lines', name='latitude reference[mrad]',line=dict(color='green')), row=1, col=1)

    fig.add_trace(go.Scatter(x=t[0, :], y=Gg[0, :],mode='lines', name='longitude gnss [mrad]',line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=Gr[0, :],mode='lines', name='longitude reference[mrad]',line=dict(color='green')), row=2, col=1)
 
    fig.add_trace(go.Scatter(x=t[0, :], y=Zg[0, :],mode='lines', name='altitude gnss [mrad]',line=dict(color='blue')), row=3, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=Zr[0, :],mode='lines', name='altitude reference[mrad]',line=dict(color='green')), row=3, col=1)
 

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)


    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="positions",
                      title_x=0.5)
    return fig

def trace_data_vordme(t,vor_bvs,dme_bvs,vor_dvl,dme_dvl,vor_pon,dme_pon,vor_rou,dme_rou):
# Création de la figure avec sous-graphiques (2 lignes, 1 colonne)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("VOR [deg]", 
                                        "DME [m]"))
    ilon = 0
    ilat = 1

    fig.add_trace(go.Scatter(x=t[0, :], y=vor_bvs[0, :],mode='lines', name='vor bvs [deg]',line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=vor_dvl[0, :],mode='lines', name='vor dvl [deg]',line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=vor_pon[0, :],mode='lines', name='vor pon [deg]',line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=vor_rou[0, :],mode='lines', name='vor rou [deg]',line=dict(color='black')), row=1, col=1)

    fig.add_trace(go.Scatter(x=t[0, :], y=dme_bvs[0, :],mode='lines', name='dme bvs [m]',line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=dme_dvl[0, :],mode='lines', name='dme dvl [m]',line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=dme_pon[0, :],mode='lines', name='dme pon [m]',line=dict(color='yellow')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=dme_rou[0, :],mode='lines', name='dme rou [m]',line=dict(color='black')), row=2, col=1)
 

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)


    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="vordme",
                      title_x=0.5)
    return fig


def trace_positions_vordme(t, Lr,Gr,Zr,vor_bvs,dme_bvs,vor_dvl,dme_dvl,vor_pon,dme_pon,vor_rou,dme_rou):
# Création de la figure avec sous-graphiques (2 lignes, 1 colonne)
# Attention, il y a plein de bugs ... les unités !!!
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Lat [xx]", 
                                        "lon [xx]"))
    ilon = 0
    ilat = 1
    BVS = np.array([2.114482,49.459839])
    DVL = np.array([0.312722,49.310750])
    PON = np.array([2.035889,49.096083])
    ROU = np.array([1.280639,49.465639])

    L_bvs = BVS[ilat] + dme_bvs*np.cos(vor_bvs*np.pi/180)
    G_bvs = BVS[ilon] + dme_bvs*np.sin(vor_bvs*np.pi/180)

    L_dvl = DVL[ilat] + dme_dvl*np.cos(vor_dvl*np.pi/180)
    G_dvl = DVL[ilon] + dme_dvl*np.sin(vor_dvl*np.pi/180)
    
    L_pon = PON[ilat] + dme_pon*np.cos(vor_pon*np.pi/180)
    G_pon = PON[ilon] + dme_pon*np.sin(vor_pon*np.pi/180)
    
    L_rou = ROU[ilat] + dme_rou*np.cos(vor_rou*np.pi/180)
    G_rou = ROU[ilon] + dme_rou*np.sin(vor_rou*np.pi/180)

    fig.add_trace(go.Scatter(x=t[0, :], y=L_bvs[0, :],mode='lines', name='latitude gnss [xx]',line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=L_dvl[0, :],mode='lines', name='latitude gnss [xx]',line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=L_pon[0, :],mode='lines', name='latitude gnss [xx]',line=dict(color='yellow')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=L_rou[0, :],mode='lines', name='latitude gnss [xx]',line=dict(color='black')), row=1, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=Lr[0, :],mode='lines', name='latitude reference[xx]',line=dict(color='green')), row=1, col=1)

    fig.add_trace(go.Scatter(x=t[0, :], y=G_bvs[0, :],mode='lines', name='longitude gnss [xx]',line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=G_dvl[0, :],mode='lines', name='longitude gnss [xx]',line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=G_pon[0, :],mode='lines', name='longitude gnss [xx]',line=dict(color='yellow')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=G_rou[0, :],mode='lines', name='longitude gnss [xx]',line=dict(color='black')), row=2, col=1)
    fig.add_trace(go.Scatter(x=t[0, :], y=Gr[0, :],mode='lines', name='longitude reference[xx]',line=dict(color='green')), row=2, col=1)
 

    # Mise à jour des titres des axes
    fig.update_xaxes(title_text="Temps [s]", row=3, col=1)

    # Mise à jour du layout général avec un titre
    fig.update_layout(height=800, title_text="positions",
                      title_x=0.5)
    return fig