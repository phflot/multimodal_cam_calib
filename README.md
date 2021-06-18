# Multimodal, Multi Camera Calibration

Example python routines for multimodal camera calibration and image acquisition of our paper *"Multimodal Data Acquisition at SARS-CoV-2 Drive 
Through Screening Centers: Setup Description and Experiences in Saarland, Germany."* and classes to read the hdf5 data 
from our recordings. The project website can be found [here](https://www.snnu.uni-saarland.de/covid19/). We use a 4x13 circular calibration board with 1.5cm circle diameter which is printed and glued 
onto a metal plate with the same pattern cutout. After heating, the pattern is visible in RGB, NIR and thermal cameras: 

![Fig1](img/fig1.jpg)

## Download

Download the repository via
```
$ git clone https://github.com/phflot/multimodal_cam_calib
```

## Documentation and Usage

This code consists of a python class to extract the circular calibration pattern in all cameras on synchronized 
recordings downsampled to 10hz and stores the results in an hdf5 file. The precomputed centers can then be used for
multicamera calibration which is based on opencv's calibration functions. We use the calibration in the paper to project points from the stereo RGB cameras and from the Kinect into the thermal image.  

## Citation

Details on the dataset from our study can be found [here](https://www.snnu.uni-saarland.de/covid19/).

If you use this code in your work, please cite
  
> Flotho, P., Bhamborae, M., Grun, T., Trenado, C., Thinnes, D., Limbach, D., & Strauss, D. J. (2021). Multimodal Data Acquisition at SARS-CoV-2 Drive Through Screening Centers: Setup Description and Experiences in Saarland, Germany. J Biophotonics.

BibTeX entry
```
@article{flotea2021b,
    author = {Flotho, P. and Bhamborae, M.J. and Grün, T. and Trenado, C. and Thinnes, D. and Limbach, D. and Strauss, D. J.},
    title = {Multimodal Data Acquisition at SARS-CoV-2 Drive Through Screening Centers: Setup Description and Experiences in Saarland, Germany},
    year = {2021},
  journal = {J Biophotonics},
  pages = {e202000512},
  doi = {https://doi.org/10.1002/jbio.202000512}
}
```