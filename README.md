Structure from Accidental Motion Kit (SAM Kit)
===================================================

Strucutre from Accidental Motion Kit is a 3D reconstruction software kit. It is capable of reconsturcting 3D sparse structure of an object from a sequence of images with limited camera translation and rotation. The reconstruction model is based on Fisher Yu and David Gallup's work in 2014, 3D Reconstruction from Accidental Motion.

Please see [CVPR 2014 3D Reconstruction from Accidental Motion](http://www.yf.io/p/tiny) for more information about the theories behind the SAM Kit.

This kit uses Ceres Solver for Bundle Adjustment.

Please see [ceres-solver.org](http://ceres-solver.org/) for more
information.

### Building

Note: It is best to build the Ceres Solver in Linux or macOS, to build on Windows is a bit troublesome, using Linux Subsystem on Windows 10 is highly recommended. 

#### Install and Build Ceres Solver
Follow [Installation Instructions](http://ceres-solver.org/building.html) here.

#### Install and Build Python and OpenCV, OpenCV-Python
Follow [Installation Instructions](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/) here.

### Usage

* Save image sequences (not included) in a folder, such as `example/images`.
* Run following Script in Python (see `example/example.py`), script will generate a bundler file `bundle.out`, and an optical flow tracking result `optical_flow.jpg` in the output folder (`example/output`).
```
python example.py
```
* Bundle adjustment will be automatically performed once the featurue tracking is completed. BA result (`final.ply`) can be found in the output folder  (`example/output`). `init.ply` is the initial guess data.

### To-Do

* More Examples.
* More test cases to prove that it is robust, as the Kit is written from scratch. It should achieve similar reconstruction result as the version I coded for FYP.

### Note

I re-wrote SAM Kit from scratch for following reasons:
* The original one I wrote for FYP is full of hacking. I re-organised the Python Code, made it neat and structured, added some documentation in the code for quick reference, consdering it may be used for further research development
* This SAM kit is modified from Ceres Solver, removing most of the unnecesary parts, building is faster than previous version.

I did not include the multiple sparse matching, as it is not current priority.