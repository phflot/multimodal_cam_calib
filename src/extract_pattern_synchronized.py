__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
## file to extract the pattern and export them for further processing and calibration

from src.util.hdf_video import *
from src.util.IO_util import imgaussfilt
from os.path import join as fullfile
import h5py


def _get_pattern_thermal(thermal_frame):
    frame = thermal_frame
    frame_8b = np.empty(frame.shape, np.uint8)
    cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    if len(frame_8b.shape) == 2:
        cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        frame_8b = cv2.cvtColor(frame_8b, cv2.COLOR_GRAY2RGB)

    status, points = cv2.findCirclesGrid(imgaussfilt(frame_8b, 0),
                                         (4, 13), flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

    frame_8b = cv2.drawChessboardCorners(frame_8b, (4, 13), points, status)

    return points, status, frame_8b


def _get_pattern_right(right_frame):
    frame = cv2.cvtColor(right_frame, cv2.COLOR_BAYER_GB2BGR)
    frame_8b = np.empty(frame.shape, np.uint8)
    cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    if len(frame_8b.shape) == 2:
        cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        frame_8b = cv2.cvtColor(frame_8b, cv2.COLOR_GRAY2RGB)

    status, points = cv2.findCirclesGrid(cv2.GaussianBlur(frame_8b, (3, 3), 0),
                                         (4, 13), flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

    frame_8b = cv2.drawChessboardCorners(frame_8b, (4, 13), points, status)

    return points, status, frame_8b


def _get_pattern_left(left_frame):
    frame = cv2.resize(cv2.cvtColor(left_frame, cv2.COLOR_BAYER_BG2RGB), None, fx=0.34, fy=0.34)
    frame_8b = np.empty(frame.shape, np.uint8)
    cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    if len(frame_8b.shape) == 2:
        cv2.normalize(frame, frame_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        frame_8b = cv2.cvtColor(frame_8b, cv2.COLOR_GRAY2RGB)

    status, points = cv2.findCirclesGrid(imgaussfilt(frame_8b, 0),
                                         (4, 13), flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

    frame_8b = cv2.drawChessboardCorners(frame_8b, (4, 13), points, status)

    return points, status, frame_8b


def _get_pattern_kinect(kinect_frame):
    frame = np.array(kinect_frame).astype(float)
    frame_8b = np.empty(frame.shape, np.uint8)

    tmp = (frame - 900) / np.power(2, 13)
    tmp[tmp < 0.0] = 0.0
    tmp[tmp > 1.0] = 1.0
    frame_8b = np.array(255 * tmp).astype(np.uint8)

    frame_8b = cv2.cvtColor(frame_8b, cv2.COLOR_GRAY2RGB)

    status, points = cv2.findCirclesGrid(frame_8b,
                                         (4, 13), flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

    frame_8b = cv2.drawChessboardCorners(frame_8b, (4, 13), points, status)

    return points, status, frame_8b


if __name__ == '__main__':
    file_path = ''
    stereo_file = ''
    thermal_file = ''
    kinect_file = '.h5'

    # loading the complete recordings
    stereo_recording = StereoRecording(fullfile(file_path, stereo_file))
    stereo_recording.load_data()
    thermal_recording = SingleRecording(fullfile(file_path, thermal_file))
    thermal_recording.load_data()
    kinect_recording = KinectRecording(fullfile(file_path, kinect_file))
    kinect_recording.load_data()

    # finding matching frames for the calibration
    timestamp_baseline = np.min(np.array([
        stereo_recording.timestamps[0],
        thermal_recording.timestamps[0],
        kinect_recording.timestamps[0]]))

    print("baseline: " + str(timestamp_baseline))
    print("kinect time: " + str(kinect_recording.timestamps[0]))
    print("thermal time: " + str(thermal_recording.timestamps[0]))

    # resampling everything to 10hz
    fps = 10
    stereo_time = np.array(stereo_recording.timestamps - timestamp_baseline).astype(float)
    thermal_time = np.array(thermal_recording.timestamps - timestamp_baseline).astype(float)
    kinect_time = np.array(kinect_recording.timestamps - kinect_recording.timestamps[0]).astype(float) - 100
    print("kinect time 2: " + str(kinect_time[0]))
    print("thermal time 2: " + str(thermal_time[0]))

    stereo_time_resampled = np.arange(0, stereo_time[-1], 1000 / fps, float)
    idx_stereo = np.round(np.interp(stereo_time_resampled, stereo_time,
                                    np.arange(0, stereo_time.shape[0]))).astype(int)
    stereo_recording.left = stereo_recording.left[idx_stereo]
    stereo_recording.right = stereo_recording.right[idx_stereo]

    thermal_time_resampled = np.arange(0, thermal_time[-1], 1000 / fps, float)
    idx_thermal = np.round(np.interp(thermal_time_resampled, thermal_time,
                                    np.arange(0, thermal_time.shape[0]))).astype(int)
    thermal_recording.frames = thermal_recording.frames[idx_thermal]

    kinect_time_resampled = np.arange(0, kinect_time[-1], 1000 / fps, float)
    idx_kinect = np.round(np.interp(kinect_time_resampled, kinect_time,
                                    np.arange(0, kinect_time.shape[0]))).astype(int)
    kinect_recording.ir_frames = kinect_recording.ir_frames[idx_kinect]

    n_frames = np.min(np.array([idx_stereo.shape[0], idx_thermal.shape[0], idx_kinect.shape[0]]))
    close = False

    left_points = np.full((n_frames, 52, 1, 2), -1.0, float)
    right_points = np.full((n_frames, 52, 1, 2), -1.0, float)
    thermal_points = np.full((n_frames, 52, 1, 2), -1.0, float)
    kinect_points = np.full((n_frames, 52, 1, 2), -1.0, float)
    for i in range(n_frames):
        points, status, frame_8b_left = _get_pattern_left(stereo_recording.left[i])
        if status:
            left_points[i] = points
        points, status, frame_8b_right = _get_pattern_right(stereo_recording.right[i])
        if status:
            right_points[i] = points
        points, status, frame_8b_thermal = _get_pattern_thermal(thermal_recording.frames[i])
        if status:
            thermal_points[i] = points
        points, status, frame_8b_kinect = _get_pattern_kinect(kinect_recording.ir_frames[i])
        if status:
            kinect_points[i] = points

        cv2.imshow("left", frame_8b_left)
        cv2.imshow("right", frame_8b_right)
        cv2.imshow("thermal", frame_8b_thermal)
        cv2.imshow("kinect", frame_8b_kinect)

        keystroke = cv2.waitKey(1) & 0xFF
        if keystroke == ord(' '):
            while True:
                keystroke = cv2.waitKey() & 0xFF
                if keystroke == 27:
                    close = True
                    break
                if keystroke == ord(' '):
                    break
        if keystroke == 27 or close:
            break

    output_file_name = 'calibration_detections.h5'
    with h5py.File(fullfile(file_path, output_file_name), 'w') as f:
        f.create_dataset('right_points', data=right_points)
        f.create_dataset('left_points', data=left_points)
        f.create_dataset('thermal_points', data=thermal_points)
        f.create_dataset('kinect_points', data=kinect_points)
