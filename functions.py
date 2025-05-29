import numpy as numpy
import numpy as np

"""Basic navigation functions;
conventions : 
    - [i] : inertial frame
    - [t] : Earth Centered Earth Fixed (ECEF) frame
    - [g] : local geographical frame : North-West-Up
    - [b] : body frame : Forth-Right-Down"""

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
    "Returns the matrix enabling to shift from [t] to [g]"
    return np.array([[-np.sin(lat) * np.cos(lon), -np.sin(lat) * np.sin(lon), np.cos(lat)],
                     [np.sin(lon),                -np.cos(lon),               0],
                     [np.cos(lat) * np.cos(lon),  np.cos(lat) * np.sin(lon),  np.sin(lat)]])
    
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
    
def compute_curve_matrix(lat: float, r_earth: float):
    return np.array([[0,         -1/r_earth,             0],
                     [1/r_earth, 0,                      0],
                     [0,         -1/r_earth*np.tan(lat), 0]])
    
def tbg_2_k_r_t(tbg:np.ndarray):
    """Extracting heading (k), roll(r) and pitch (t) from tbg matrix"""
    return np.array([np.arctan2(-tbg[0,1], tbg[0,0]), 
    # return np.array([-np.arctan2(tbg[0,0], tbg[0,1]), 
                     np.arctan2(-tbg[1,2],-tbg[2,2]), 
                    #  np.arctan2(tbg[2,2],tbg[1,2]), 
                     np.arccos(np.sqrt(1 - tbg[0,2] ** 2))])
    

def angle2dcm(yaw, pitch, roll, input_units="rad", rotation_sequence="321"):
    """
    Returns a transformation matrix (aka direction cosine matrix or DCM) which
    transforms from navigation to body frame.  Other names commonly used,
    besides DCM, are `Cbody2nav` or `Rbody2nav`.  The rotation sequence
    specifies the order of rotations when going from navigation-frame to
    body-frame.  The default is '321' (i.e Yaw -> Pitch -> Roll).
    Parameters
    ----------
    yaw   : yaw angle, units of input_units.
    pitch : pitch angle, units of input_units.
    roll  : roll angle , units of input_units.
    input_units: units for input angles {'rad', 'deg'}, optional.
    rotationSequence: assumed rotation sequence {'321', others can be
                                                implemented in the future}.
    Returns
    -------
    Rnav2body: 3x3 transformation matrix (numpy matrix data type).  This can be
               used to convert from navigation-frame (e.g NED) to body frame.

    Notes
    -----
    Since Rnav2body is a proper transformation matrix, the inverse
    transformation is simply the transpose.  Hence, to go from body->nav,
    simply use: Rbody2nav = Rnav2body.T
    Examples:
    ---------
    >>> import numpy as np
    >>> from nav import angle2dcm
    >>> g_ned = np.matrix([[0, 0, 9.8]]).T # gravity vector in NED frame
    >>> yaw, pitch, roll = np.deg2rad([90, 15, 0]) # vehicle orientation
    >>> g_body = Rnav2body * g_ned
    >>> g_body
    matrix([[-2.53642664],
            [ 0.        ],
            [ 9.4660731 ]])

    >>> g_ned_check = Rnav2body.T * g_body
    >>> np.linalg.norm(g_ned_check - g_ned) < 1e-10 # should match g_ned
    True
    Reference
    ---------
    [1] Equation 2.4, Aided Navigation: GPS with High Rate Sensors, Jay A. Farrel 2008
    [2] eul2Cbn.m function (note, this function gives body->nav) at:
    http://www.gnssapplications.org/downloads/chapter7/Chapter7_GNSS_INS_Functions.tar.gz
    """
    # Apply necessary unit transformations.
    if input_units == "rad":
        pass
    elif input_units == "deg":
        yaw, pitch, roll = np.radians([yaw, pitch, roll])

    # Build transformation matrix Rnav2body.
    s_r, c_r = sin(roll), cos(roll)
    s_p, c_p = sin(pitch), cos(pitch)
    s_y, c_y = sin(yaw), cos(yaw)

    if rotation_sequence == "321":
        # This is equivalent to Rnav2body = R(roll) * R(pitch) * R(yaw)
        # where R() is the single axis rotation matrix.  We implement
        # the expanded form for improved efficiency.
        Rnav2body = np.matrix(
            [
                [c_y * c_p, s_y * c_p, -s_p],
                [-s_y * c_r + c_y * s_p * s_r, c_y * c_r + s_y * s_p * s_r, c_p * s_r],
                [s_y * s_r + c_y * s_p * c_r, -c_y * s_r + s_y * s_p * c_r, c_p * c_r],
            ]
        )

    else:
        # No other rotation sequence is currently implemented
        print("WARNING (angle2dcm): requested rotation_sequence is unavailable.")
        print("                     NaN returned.")
        Rnav2body = np.nan

    return Rnav2body
