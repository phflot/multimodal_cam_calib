__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
import numpy as np
import cv2
import h5py
from src.util.IO_util import imagesc
from src.util.IO_util import normalize_color


class StereoRecording:
    def __init__(self, hdf_file, n_frames=None):
        self.hdf_file = hdf_file
        with h5py.File(self.hdf_file, 'r') as f:
            self.width_left = f['FRAMES'].attrs['Width_1']
            self.height_left = f['FRAMES'].attrs['Height_1']
            self.width_right = f['FRAMES'].attrs['Width_2']
            self.height_right = f['FRAMES'].attrs['Height_2']
            if n_frames is None:
                self.n_frames = f['FRAMES'].attrs['FrameCount']
            else:
                self.n_frames = n_frames

            self.left = None
            self.right = None
            self.timestamps = None

    def load_data(self):
        with h5py.File(self.hdf_file, 'r') as f:
            tmp_frames = f['FRAMES'][0:self.n_frames]
            self.timestamps = f['Timestamps_ms'][0:self.n_frames]
        self.left, self.right = self.__split_stereo(tmp_frames)

    def get_frames(self, idx):
        with h5py.File(self.hdf_file, 'r') as f:
            tmp_frames = f['FRAMES'][idx]
            timestamps = f['Timestamps_ms'][idx]

        left, right = self.__split_stereo(tmp_frames)
        return left, right, timestamps

    def plot_stereo_frame_pair(self, frame_num):
        cv2.imshow("left", cv2.resize(cv2.cvtColor(self.left[frame_num], cv2.COLOR_BAYER_BG2RGB), None, fx=0.3, fy=0.3))
        cv2.imshow("right", cv2.cvtColor(self.right[frame_num], cv2.COLOR_BAYER_BG2BGR))

    def get_right_left_frame(self, frame_num):
        right_frame = self.right[frame_num]
        left_frame = self.left[frame_num]

        return right_frame, left_frame

    def __split_stereo(self, f):
        size_left = np.int(self.width_left * self.height_left)
        size_right = np.int(self.width_right * self.height_right)

        left_frames = np.reshape(f[:, 0:size_left], (self.n_frames, self.height_left, self.width_left))
        right_frames = np.reshape(f[:, -size_right - 1:-1], (self.n_frames, self.height_right, self.width_right))

        return left_frames, right_frames


class KinectRecording:
    def __init__(self, hdf_file, n_frames=None):
        self.hdf_file = hdf_file
        with h5py.File(self.hdf_file, 'r') as f:
            self.width = np.int(f['FRAMES'].attrs['FrameWidth'] / 2)
            self.height = f['FRAMES'].attrs['FrameHeight']
            if n_frames is None:
                self.n_frames = f['FRAMES'].attrs['FrameCount']
            else:
                self.n_frames = n_frames

            self.ir_frames = None
            self.depth_frames = None
            self.timestamps = None

    def load_data(self):
        with h5py.File(self.hdf_file, 'r') as f:
            tmp = f['FRAMES'][0:self.n_frames]
            self.timestamps = f['Timestamps_ms'][0:self.n_frames]
        self.ir_frames = tmp[:, :, self.width-1::-1]
        self.depth_frames = tmp[:, :, -1:self.width-1:-1]

    def get_frames(self, idx):
        with h5py.File(self.hdf_file, 'r') as f:
            tmp = f['FRAMES'][idx]
            timestamps = f['Timestamps_ms'][idx]
        ir_frames = tmp[:, :, self.width:0:-1]
        depth_frames = tmp[:, :, self.width:0:-1]
        return ir_frames, depth_frames, timestamps

    def plot_kinect_frame(self, frame_num):
        imagesc(self.ir_frames[frame_num], "ir frame 1", cv2.COLORMAP_BONE)
        image_depth = cv2.flip(self.ir_frames[frame_num], 1)
        imagesc(image_depth, "depth frame 1")

    def get_nir_frame(self, frame_num):
        kinect_frame = cv2.flip(self.ir_frames[frame_num], 1)

        return kinect_frame


class SingleRecording:
    # class works for hfr and thermal hdf recordings
    def __init__(self, hdf_file, n_frames=None):
        self.hdf_file = hdf_file
        with h5py.File(self.hdf_file, 'r') as f:
            self.width = f['FRAMES'].attrs['FrameWidth']
            self.height = f['FRAMES'].attrs['FrameHeight']
            if n_frames is None:
                self.n_frames = f['FRAMES'].attrs['FrameCount']
            else:
                self.n_frames = n_frames

        self.frames = h5py.File(self.hdf_file, 'r')['FRAMES']
        self.timestamps = h5py.File(self.hdf_file, 'r')['Timestamps_ms']

    def load_data(self):
        self.frames = self.frames[0:self.n_frames]
        self.timestamps = self.timestamps[0:self.n_frames]

    def get_frames(self, idx):
        with h5py.File(self.hdf_file, 'r') as f:
            frames = f['FRAMES'][idx]
            timestamps = f['Timestamps_ms'][idx]
        return frames, timestamps

    def plot_thermal_frame(self, frame_num):
        test_frame = np.resize(self.frames[frame_num], (480, 640))
        norm_img = normalize_color(test_frame)
        imagesc(norm_img)

    def get_thermal_frame(self, frame_num):
        thermal_frame = np.resize(self.frames[frame_num], (480, 640))

        return thermal_frame
