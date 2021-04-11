__author__ = "Philipp Flotho"
"""
multimodal_cam_calib
Copyright 2021 by Philipp Flotho, All rights reserved.
"""
from setuptools import setup, find_packages

setup(
    name="multimodal_cam_calib",
    version="0.0.1",
    author="Philipp Flotho",
    author_email="Philipp.Flotho@uni-saarland.de",
    description='Example routines for multimodal camera calibration of our paper *"Multimodal Data Acquisition at '
                'SARS-CoV-2 Drive Through Screening Centers: Setup Description and Experiences in Saarland, '
                'Germany."* and classes to read the hdf5 data from our recordings.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/phflot/multimodal_cam_calib',
    install_requires=[
        'opencv',
        'numpy',
        'h5py'],
    packages=find_packages()
)

