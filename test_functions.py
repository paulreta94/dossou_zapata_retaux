import pytest
import numpy as np
from .functions import *

def test_rotation():
    for axis in ["x", "y", "z"]:
        assert(np.allclose(rotation(angle = 0, axis = axis), np.eye(3)) == True)
        
def test_lat_lon_2_tgt():
    """Reminder : tgt = Rot_y(lat - pi / 2) @ Rot_z(lon + pi)"""
    assert(np.allclose(lat_lon_2_tgt(lat = 0, lon = 0), 
                       rotation(angle = -np.pi / 2, axis="y") @ rotation(angle = np.pi, axis="z")))
    
def test_k_r_t_2_tbg():
    """Reminder : tbg = Rot_x(r) @ Rot_y(t) @ Rot_z(k) @ Rot_x(pi)"""
    assert (np.allclose(k_r_t_2_tbg(k = 0, r = 0, t= 0), 
                        rotation(0, "x") @ rotation(0, "y") @ rotation(0, "z") @ rotation(np.pi, "x")) == True)

def test_tbg_2_k_r_t():
    assert (tbg_2_k_r_t(k_r_t_2_tbg(k = 0, r = 0, t = 0)) == (pytest.approx(0),pytest.approx(0),pytest.approx(0)))
    
def test_tgt_2_lat_lon():
    assert (tgt_2_lat_lon(lat_lon_2_tgt(lat=0,lon=0)) == (pytest.approx(0), pytest.approx(0)))

# def test_bort_rot():
#     assert (np.allclose(bortz_rot(np.array([0,0,0])), np.eye(3)) == True)