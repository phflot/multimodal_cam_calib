__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
import cv2
import numpy as np


def calibrate_single_cam(image_points, object_points_single, valid_idx, image_size):
    tmp_points = image_points[valid_idx]
    error, mtx, dist, rvecs, tvecs, _ = \
        cv2.calibrateCameraRO(np.tile(object_points_single, (tmp_points.shape[0], 1, 1)), tmp_points,
                              image_size, None, None, None)
    return SingleCalibrationResult(error, mtx, dist, rvecs, tvecs)


def calibrate_stereo_cam(left_points, right_points, object_points, valid_idx, calib_left, calib_right):
    tmp_left = left_points[valid_idx]
    tmp_right = right_points[valid_idx]
    error, mtx1, dist1, mtx2, dist2, R, T, E, F = \
        cv2.stereoCalibrate(np.tile(object_points, (tmp_left.shape[0], 1, 1)), tmp_left, tmp_right,
                            cameraMatrix1=calib_left.mtx, distCoeffs1=calib_left.dist,
                            cameraMatrix2=calib_right.mtx, distCoeffs2=calib_right.dist, imageSize=(0, 0),
                            R=None, T=None, E=None, F=None, flags=cv2.CALIB_FIX_INTRINSIC)

    return StereoCalibrationResult(error, mtx1, dist1, mtx2, dist2, R, T, E, F)


def get_object_points():
    width = 4
    height = 13
    object_points = np.zeros((52, 3), np.float32)
    offset = 20
    spacing = 40
    for j in range(height):
        for i in range(width):
            idx = j * width + i
            object_points[idx, 0] = j * offset
            object_points[idx, 1] = i * spacing + (j % 2) * offset
    return object_points


class SingleCalibrationResult:
    def __init__(self, error, mtx, dist, rvecs, tvecs):
        self.error = error
        self.mtx = mtx
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs


class StereoCalibrationResult:
    def __init__(self, error, mtx1, dist1, mtx2, dist2, R, T, E, F):
        self.error = error
        self.mtx1 = mtx1
        self.dist1 = dist1
        self.mtx2 = mtx2
        self.dist2 = dist2
        self.R = R
        self.T = T
        self.E = E
        self.F = F


class CalibrationEngine:
    pass
