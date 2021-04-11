__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
## calibration with detected patterns from extract_pattern_synchronized.py

from src.util.calibration_util import *
import h5py


thermal_width = 640
thermal_height = 480


kinect_width = 512
kinect_height = 424


left_width = 1398
left_height = 1023


right_width = 1280
right_height = 1024


if __name__ == '__main__':
    input_file = '../detections/calibration_detections_200512.h5'

    with h5py.File(input_file, 'r') as f:
        right_points = f['right_points'][:].astype(np.float32)
        left_points = f['left_points'][:].astype(np.float32)
        thermal_points = f['thermal_points'][:].astype(np.float32)
        kinect_points = f['kinect_points'][:].astype(np.float32)

    object_points = get_object_points()

    stride = 10
    idx_left = np.squeeze(np.array(np.where(left_points[:, 0, 0, 0] != -1)))[0:-1:stride]
    idx_right = np.squeeze(np.array(np.where(right_points[:, 0, 0, 0] != -1)))[0:-1:stride]
    idx_thermal = np.squeeze(np.array(np.where(thermal_points[:, 0, 0, 0] != -1)))[0:-1:stride]
    idx_kinect = np.squeeze(np.array(np.where(kinect_points[:, 0, 0, 0] != -1)))[0:-1:stride]
    idx_left_thermal = np.squeeze(np.array(np.where(
        (left_points[:, 0, 0, 0] != -1) & (thermal_points[:, 0, 0, 0] != -1))))[0:-1:stride]
    idx_left_right = np.squeeze(np.array(np.where(
        (left_points[:, 0, 0, 0] != -1) & (right_points[:, 0, 0, 0] != -1))))[0:-1:stride]
    idx_kinect_thermal = np.squeeze(np.array(np.where(
        (kinect_points[:, 0, 0, 0] != -1) & (thermal_points[:, 0, 0, 0] != -1))))[0:-1:stride]

    left_calib = calibrate_single_cam(left_points, object_points, idx_left, (left_width, left_height))
    right_calib = calibrate_single_cam(right_points, object_points, idx_right, (right_width, right_height))
    thermal_calib = calibrate_single_cam(thermal_points, object_points, idx_thermal, (thermal_width, thermal_height))
    kinect_calib = calibrate_single_cam(kinect_points, object_points, idx_kinect, (kinect_width, kinect_height))

    stereo_calib = calibrate_stereo_cam(left_points, right_points, object_points, idx_left_right, left_calib, right_calib)
    left_thermal_calib = calibrate_stereo_cam(left_points, thermal_points,
                                              object_points, idx_left_thermal, left_calib, thermal_calib)
    kinect_thermal_calib = calibrate_stereo_cam(kinect_points, thermal_points, object_points, idx_kinect_thermal,
                                                kinect_calib, thermal_calib)

    print("done calibration!")
