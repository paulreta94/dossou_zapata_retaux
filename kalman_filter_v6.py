import numpy as np
import scipy
from functions import compute_t_g_b


def v_inertielle(vx, vy, vz):
    return np.sqrt(vx**2 + vy**2 + vz**2)


def kalman_filter(
    x_curr: np.ndarray,
    l: float,
    d_odo: float,
    d_ins: float,
    # biases_vector,
    # drifts_vector,
):
    """Implements one step of the kalman filter
    x_curr : x(k-1|k-1)
    l : latitude
    d_odo : distance indicated by odometer
    d_ins : cumulated sum of distances increments
    """
    # Paramètres du système
    dt = 1 / 100
    w = 15 * np.pi / 180  # vitesse de rotation de la Terre [rad/s]
    g = 9.81  # m/s^2
    n = 11  # dimension du vecteur d'etat
    R_T = 6371000
    # vecteur d'état: (dL,dg, dalt,dvn,dve,dvdown,phix,phiy,phiz,delta_d_odo,delta_d_ins)
    Q = np.eye(11) * 0.01
    R = 0.1**2
    P = np.diag([1**2, 1**2, 1**2, 1**2, 1**2, 1**2, 1**2, 1**2, 1**2, 1**2, 1**2])

    # for k in range(num_steps):

    # Matrice tbg (reste inchangé)
    # Étape de prédiction
    F = np.array(
        [
            [1, 0, 0, dt, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, dt, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, dt, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2 * w * np.sin(l) * dt, 0, 0, g * dt, 0, 0, 0],
            [0, 0, 0, -2 * w * np.sin(l) * dt, 1, 0, -g * dt, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [
                w * np.sin(l) / R_T * dt,
                0,
                0,
                0,
                (1 / R_T) * dt,
                0,
                1,
                w * np.sin(l) * dt,
                0,
                0,
                0,
            ],
            [
                0,
                0,
                0,
                -1 / R_T * dt,
                0,
                0,
                -w * np.sin(l) * dt,
                1,
                w * np.cos(l) * dt,
                0,
                0,
            ],
            [
                -w * np.cos(l) / R_T * dt,
                0,
                0,
                0,
                np.tan(l) / R_T * dt,
                0,
                0,
                -w * np.cos(l) * dt,
                1,
                0,
                0,
            ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ]
    )
    # x_pred = F @ x_curr + np.concatenate(
    # np.concatenate(np.concatenate(np.zeros((3, 1)), biases_vector), drifts_vector),
    # np.zeros((2, 1)),
    # )
    x_pred = F @ x_curr
    P_pred = F @ P @ F.T + Q

    # Etape de recalage
    H = np.zeros((1, n))
    H[0, 9] = 1
    H[0, 10] = -1
    z = d_odo - d_ins

    K = P_pred @ H.T @ np.linalg.inv(H @ P_pred @ H.T + R)

    # Mise à jour
    x_est = x_pred + K @ (z - H @ x_pred)
    P_pred = P_pred - K @ H @ P_pred
    return x_est
