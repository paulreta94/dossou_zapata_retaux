from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
from kalman_filter_v6 import kalman_filter

# Path to .mat file
# Cocher line 1 et 3 pour la boucle
# Cocher line 2 et 4 pour Fécamp

# Donnees de reference
# file_path_ref = r"02-Navigations_parfaites\Nav_reference_boucle_1.mat"
file_path_ref = r"02-Navigations_parfaites\Nav_reference_aller.mat"

# Donnees inertielles
# file_path_INS = r"05-Données_Odometre\Donnees_inertielles_boucle_1.mat"
file_path_INS = r"05-Données_Odometre\Donnees_inertielles_aller.mat"

# Donnees non inertielles
# file_path_odo = r"05-Données_Odometre\Donnees_non_inertielles_odo_boucle_1.mat"
file_path_odo = r"05-Données_Odometre\Donnees_non_inertielles_odo_aller.mat"

# Keys in the REF file: dict_keys(['__header__', '__version__', '__globals__', 'altitude_ins', 'cap_ins',
#  'latitude_ins', 'longitude_ins', 'roulis_ins', 'tangage_ins', 'temps_s', 'vit_ins_n', 'vit_ins_w',
#  'vit_ins_z'])

# Keys in the INS file: dict_keys(['__header__', '__version__', '__globals__', 'inc_angl_x_rad',
#  'inc_angl_y_rad', 'inc_angl_z_rad', 'inc_vit_x_ms', 'inc_vit_y_ms', 'inc_vit_z_ms', 'temps_s'])

# print("Keys in the .mat file:", data_INS.keys())

# print(data_INS['temps_s'])

# ------------------- DATA --------------------------
data_ref = loadmat(file_path_ref)
data_INS = loadmat(file_path_INS)
data_odo = loadmat(file_path_odo)
ref_lat = data_ref["latitude_ins"].flatten()
ref_lon = data_ref["longitude_ins"].flatten()
ref_time = data_ref["temps_s"].flatten()

time = data_INS["temps_s"].flatten()

inc_vit_x = data_INS["inc_vit_x_ms"].flatten()
inc_vit_y = data_INS["inc_vit_y_ms"].flatten()
inc_v_z = data_INS["inc_vit_z_ms"].flatten()

time_INS = data_INS["temps_s"].flatten()
inc_ang_x = data_INS["inc_angl_x_rad"].flatten()
inc_ang_y = data_INS["inc_angl_y_rad"].flatten()
inc_angl_z = data_INS["inc_angl_z_rad"].flatten()
distance_odo = data_odo["Dist_Odo_m"].flatten()
# -------------- Initial position ------------------
lat_init = 49.02621
lon_init = 2.110168
heading = 0

position = np.array([0.0, 0.0, 0.0])
velocity = np.array([0.0, 0.0, 0.0])
orientation = np.eye(3)

# A verifier ?
roll = [0.0]  # Roulis
pitch = [0.0]  # Tangage
yaw = [0.0]  # Cap

trajectory = [position.copy()]

R = 6371000  # Rterre

lat_traj = [lat_init]
lon_traj = [lon_init]


# ---------- MATRICE rotation -----------------------
def compute_rotation_matrix(delta_x, delta_y, delta_z):
    R_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(delta_x), -np.sin(delta_x)],
            [0, np.sin(delta_x), np.cos(delta_x)],
        ]
    )
    R_y = np.array(
        [
            [np.cos(delta_y), 0, np.sin(delta_y)],
            [0, 1, 0],
            [-np.sin(delta_y), 0, np.cos(delta_y)],
        ]
    )
    R_z = np.array(
        [
            [np.cos(delta_z), -np.sin(delta_z), 0],
            [np.sin(delta_z), np.cos(delta_z), 0],
            [0, 0, 1],
        ]
    )
    return R_z @ R_y @ R_x


distance_ins = 0.0
x_error = np.ones((11, 1)) * 0.1
# --------------------- MAIN LOOP NAV ---------------------------
for i in range(1, len(time)):
    dt = time[i] - time[i - 1]  # Time step
    freq_echant = 1 / dt
    heading += inc_angl_z[i]

    # Vitesse --> coord
    vx_global = freq_echant * inc_vit_x[i] * np.cos(heading) - freq_echant * inc_vit_y[
        i
    ] * np.sin(heading)
    vy_global = freq_echant * inc_vit_x[i] * np.sin(heading) + freq_echant * inc_vit_y[
        i
    ] * np.cos(heading)

    # D en METRES
    dx = vx_global * dt * freq_echant
    dy = vy_global * dt * freq_echant

    # latitude/longitude
    dlat = dy / R * (180 / np.pi)
    dlon = dx / (R * np.cos(np.radians(lat_traj[-1]))) * (180 / np.pi)

    # K i R
    roll.append(roll[-1] + inc_ang_x[i] * dt)
    pitch.append(pitch[-1] + inc_ang_y[i] * dt)
    yaw.append(yaw[-1] + inc_angl_z[i] * dt)

    # Update
    x_error = kalman_filter(
        x_curr=x_error,
        l=lat_traj[i - 1],
        d_odo=distance_odo[i - 1],
        d_ins=distance_ins,
    )
    # Filtrage de Kalman
    lat_traj.append(lat_traj[-1] + dlat - x_error[0, 0])
    lon_traj.append(lon_traj[-1] + dlon - x_error[1, 0])
    # lat_traj.append(lat_traj[-1] + dlat)
    # lon_traj.append(lon_traj[-1] + dlon)
    distance_ins = distance_ins + np.sqrt(
        (lat_traj[i] - lat_traj[i - 1]) ** 2 + (lon_traj[i] - lon_traj[i - 1]) ** 2
    )

# Arrays
# pour le KALMAN
lat_traj = np.array(lat_traj)  # LATITUDE
lon_traj = np.array(lon_traj)  # LONGITUDE
roll = np.array(roll)  # ROULIS
pitch = np.array(pitch)  # TANGAGE
yaw = np.array(yaw)  # CAP

# ---------------- Plot -------------------
plt.figure(figsize=(10, 6))
plt.plot(ref_lon, ref_lat, label="Reference Trajectory", color="blue")
plt.plot(lon_traj, lat_traj, label="Hybrid navigation", color="red")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Comparaison")
plt.legend()
plt.grid()

plt.figure(figsize=(12, 8))

# (Roulis)
plt.subplot(3, 1, 1)
plt.plot(time, np.degrees(roll), label="Roulis", color="blue")
plt.ylabel("Degrees")
plt.title("Roll vs Time")
plt.grid()
plt.legend()

# (Tangage)
plt.subplot(3, 1, 2)
plt.plot(time, np.degrees(pitch), label="Tangage", color="green")
plt.ylabel("Degrees")
plt.title("Pitch vs Time")
plt.grid()
plt.legend()

# (Cap)
plt.subplot(3, 1, 3)
plt.plot(time, np.degrees(yaw), label="Cap", color="red")
plt.xlabel("Time (s)")
plt.ylabel("Degrees")
plt.title("Yaw vs Time")
plt.grid()
plt.legend()

plt.tight_layout()

plt.show()
