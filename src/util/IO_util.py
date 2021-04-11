__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
import numpy as np
import cv2


def imagesc(img, window_name="Imagesc", color_map=cv2.COLORMAP_HOT):
    cv2.imshow(window_name, normalize_color(img, color_map))


def normalize_color(img, color_map=cv2.COLORMAP_HOT, normalize=True):
    img_8b = np.empty(img.shape, np.uint8)
    if normalize:
        cv2.normalize(img, img_8b, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    else:
        img_8b = (255 * img).astype(np.uint8)
    img_8b = cv2.applyColorMap(img_8b, color_map)
    return img_8b


def draw_landmarks(frame, landmarks):
    frame_rgb = normalize_color(frame)
    for (x, y) in landmarks:
        cv2.circle(frame_rgb, (int(np.round(x)), int(np.round(y))), 2, (0, 0, 0), -1)

    return frame_rgb


def imgaussfilt(img, sigma):
    if np.isscalar(sigma):
        width = 2 * (np.ceil(6 * sigma) // 2) + 1
        height = width
    else:
        width = 2 * (np.ceil(6 * sigma[0]) // 2) + 1
        height = 2 * (np.ceil(6 * sigma[1]) // 2) + 1
    width = int(width)
    height = int(height)
    return cv2.GaussianBlur(img, (width, height), sigmaX=sigma, sigmaY=sigma)


def map_temp(data, cam="A655"):
    if cam == "A655":
        return (0.1 * data) - 273.15
    elif cam == "A65":
        return (0.04 * data) - 273.15
    else:
        print("camera not implemented!")
