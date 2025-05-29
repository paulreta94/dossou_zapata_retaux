import numpy as numpy
import numpy as np

"""Basic navigation functions;
conventions : 
    - [i] : inertial frame
    - [t] : Earth Centered Earth Fixed (ECEF) frame
    - [g] : local geographical frame : North-West-Up
    - [b] : body frame : Forth-Right-Down"""
omega_t_ti = np.array([0,0,np.deg2rad(15.04)/3600]) # [rad/s]
dt = 1/100 # [s]
r_earth = 6378000 # [m]
g = 9.81 # [m/s^2]

def rotation(angle:float, axis:str):
    """angle : float - angle in rad
    axis : str - "x" / "y" / "z" - name of the axis
    Returns the rotation matrix around the mentionned axis"""
    if axis == "x":
        return np.array([[1, 0,              0],
                         [0, np.cos(angle),  np.sin(angle)],
                         [0, -np.sin(angle), np.cos(angle)]])
    elif axis == "y":
        return np.array([[np.cos(angle), 0, -np.sin(angle)],
                         [0,             1, 0],
                         [np.sin(angle), 0, np.cos(angle)]])
    else:
        return np.array([[np.cos(angle),  np.sin(angle), 0],
                         [-np.sin(angle), np.cos(angle), 0],
                         [0,              0,             1]])

def lat_lon_2_tgt(lat:float, lon: float):
    """Returns the matrix enabling to shift from [t] to [g]"""
    return np.array([[-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat)],
                     [np.sin(lon),                -np.cos(lon),               0],
                     [np.cos(lat) * np.cos(lon),  np.cos(lat) * np.sin(lon),  np.sin(lat)]])

def tgt_2_lat_lon(tgt : np.ndarray):
    """Extracts latitude and longitude from Tgt"""
    return (np.arccos(tgt[0,2]), np.arcsin(tgt[1,0]))
    
def k_r_t_2_tbg(k: float, r:float, t:float):
    """Returns matrix enabling to shift from [g] to [b]"""
    return np.array([[np.cos(k) * np.cos(t), 
                      -np.sin(k) * np.cos(t), 
                      np.sin(t)],
                     [-np.sin(k) * np.cos(r) + np.cos(k) * np.sin(t) * np.sin(r),
                      -np.cos(k) * np.cos(r) - np.sin(k) * np.sin(t) * np.sin(r),
                      -np.cos(t) * np.sin(r)],
                     [np.sin(k) * np.sin(r) + np.cos(k) * np.sin(t) * np.cos(r),
                      np.cos(k) * np.sin(r) - np.sin(k) * np.sin(t) * np.cos(r),
                      -np.cos(t) * np.cos(r)]])
    
def compute_curve_matrix(lat: float):
    return np.array([[0,         -1/r_earth,             0],
                     [1/r_earth, 0,                      0],
                     [0,         -1/r_earth*np.tan(lat), 0]])
    
def tbg_2_k_r_t(tbg:np.ndarray):
    """Extracting heading (k), roll(r) and pitch (t) from tbg matrix"""
    return (np.arctan2(-tbg[0,1], tbg[0,0]), 
    # return np.array([-np.arctan2(tbg[0,0], tbg[0,1]), 
            np.arctan2(-tbg[1,2],-tbg[2,2]), 
                    #  np.arctan2(tbg[2,2],tbg[1,2]), 
            np.arccos(np.sqrt(1 - tbg[0,2] ** 2)))

def compute_delta_v_geo(t_g_b:np.ndarray, delta_v_b:np.ndarray):
    return t_g_b @ delta_v_b - np.array([0,0,g]) * dt   

def antisymm(u:np.ndarray):
    return np.array([[0,     -u[2], u[1]],
                     [u[2],  0,     -u[0]],
                     [-u[1], u[0],  0]]) 

def bortz_rot(phi_vector):
    phi_norm = np.linalg.norm(phi_vector)
    return np.eye(3) - np.sin(phi_norm) / phi_norm * antisymm(phi_vector) + (1 - np.cos(phi_norm)) / phi_norm ** 2 * antisymm(phi_vector) @ antisymm(phi_vector)

def compute_delta_theta_g_gi(curve_matrix:np.ndarray, v_geo:np.ndarray, t_g_t:np.ndarray):
    return (curve_matrix @ v_geo + t_g_t @ omega_t_ti) * dt