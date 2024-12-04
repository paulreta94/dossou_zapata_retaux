import numpy as np
import scipy
import plotly
import matplotlib
import tqdm


# ------------------ Boucle ACCELERO -------------------------
global omega


def compute_t_g_b(K, R, T):
    return np.array(
        [
            [np.cos(K) * np.cos(T), -np.sin(K) * np.cos(T), np.sin(T)],
            [
                -np.sin(K) * np.cos(R) + np.cos(K) * np.sin(T) * np.sin(R),
                -np.cos(K) * np.cos(R) - np.sin(K) * np.sin(T) * np.sin(R),
                -np.cos(T) * np.sin(R),
            ],
            [
                np.sin(K) * np.sin(R) + np.cos(K) * np.sin(T) * np.cos(R),
                np.cos(K) * np.sin(R) - np.sin(K) * np.sin(T) * np.cos(R),
                -np.cos(T) * np.cos(R),
            ],
        ]
    ).T


def compute_t_g_t(L: float, G: float):
    """Returns the matrix enabling to shift from geo to terrestrial referential"""
    return np.array(
        [
            [-np.sin(L) * np.cos(G), -np.sin(L) * np.sin(G), np.cos(L)],
            [np.sin(G), -np.cos(G), 0],
            [np.cos(L) * np.cos(G), np.cos(L) * np.sin(G), np.sin(L)],
        ]
    )


# Creation des matrices de rotation
def compute_t_t_i(omega, t, L, G, K, T, R):
    return np.array(
        [
            [np.cos(omega * t), np.sin(omega * t), 0],
            [-np.sin(omega * t), np.cos(omega * t), 0],
            [0, 0, 1],
        ]
    )


# Compensation Coriolis et acc.centripète
# def coriolis_matrix(T_p_t, ro_p, omega):
#     matA = ro_p + 2 * T_p_t * np.array([[0], [0], [omega]])
#     coriolisA = antisymmetric_matrix(matA)
#     return coriolisA


g_geo_vector = np.array([[0], [0], [9.81]])  # unit : [m/s^2]
omega_inertial_vector = np.array([[0], [0], [15 * np.pi / 180 / 3600]])


def compute_omega_b_b_g(t_b_g, t_g_t, omega_b_b_i, rho_g_x, rho_g_y):
    """Returns, in the body referential, the rotation vector of body relative to the terrestrial one"""
    return (
        omega_b_b_i
        - t_b_g @ t_g_t * omega_inertial_vector
        - t_b_g * np.array([rho_g_x, rho_g_y, 0])
    )


def compute_omega_g_g_t(v_gx: float, v_gy: float, z: float, lat: float):
    """Returns the vector of the angular speeds in the geographical referential"""
    Rt = 6378000.0  # Rayon terrestre en mètres
    return np.array([[0], [v_gx / (Rt + z)], [-v_gy / ((Rt + z) * np.cos(lat))]])


def antisymmetric(u: np.ndarray):
    """Returns the corresponding antisymmetrical matrix"""
    u_x, u_y, u_z = u[0, 0], u[1, 0], u[2, 0]
    return np.array([[0, -u_x, u_y], [u_z, 0, -u_x], [-u_y, u_x, 0]])


def extract_h_r_p(t_b_g):

    T = np.arcsin(t_b_g[0, 2])
    R = np.arcsin(-t_b_g[1, 2] / np.cos(T))
    K = np.arccos(t_b_g[0, 0] / np.cos(T))
    return K, R, T


def extract_lat_lon(t_g_t: np.ndarray, time_instant: float):
    # TODO : faire un moyennage sur toutes les valeurs de la matrice
    try:
        lat = np.arccos(t_g_t[0, 2])
    except ValueError:
        print(f"Warning : could not extract latitude at step number {time_instant}")
        lat = -1
    try:
        lon = np.arcsin(t_g_t[1, 0])
    except ValueError:
        print(f"Warning : could not extract latitude at step {time_instant}")
        lon = -1
    return lat, lon
