# coding=utf-8
"""Transformation matrices for computer graphics"""

"""Modifiaciónes realizadas: Se eliminaron todas las transformaciones extras que se encontraban en el módulo
de esta manera, solo quedan las transformaciones pertinentes al 2D y se agregó la transformación reflexión"""

import numpy as np

__author__ = "Daniel Calderon"
__license__ = "MIT"

def identity():
    return np.identity(4, dtype=np.float32)

def reflectionY():
    return np.array([
        [-1,0,0],
        [0,1,0],
        [0,0,1]], dtype = np.float32)

def reflectionX():
    return np.array([
        [1,0,0],
        [0,-1,0],
        [0,0,1]], dtype = np.float32)

def reflectionOrigin():
    return np.array([
        [-1,0,0],
        [0,-1,0],
        [0,0,1]], dtype = np.float32)

def uniformScale(s):
    return np.array([
        [s,0,0,0],
        [0,s,0,0],
        [0,0,s,0],
        [0,0,0,1]], dtype = np.float32)


def scale(sx, sy, sz):
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]], dtype = np.float32)


def rotation(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,-sin_theta,0,0],
        [sin_theta,cos_theta,0,0],
        [0,0,1,0],
        [0,0,0,1]], dtype = np.float32)


def translate(tx, ty, tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]], dtype = np.float32)


def shearing(xy, yx, xz, zx, yz, zy):
    return np.array([
        [ 1, xy, xz, 0],
        [yx,  1, yz, 0],
        [zx, zy,  1, 0],
        [ 0,  0,  0, 1]], dtype = np.float32)


def matmul(mats):
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out
