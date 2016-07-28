Structure from Accidental Motion Kit (SAM Kit)
===================================================

This kit is written based on Ceres Solver. 

Please see [ceres-solver.org](http://ceres-solver.org/) for more
information.

### Building

Note: It is best to build the Ceres Solver in Linux or macOS, to build on Windows is a bit troublesome, using Linux Subsystem on Windows 10 is highly recommended. 

#### Install and Build Ceres Solver
Follow [Installation Instructions](http://ceres-solver.org/building.html) here.

#### Install and Build Python and OpenCV, OpenCV-Python
Follow [Installation Instructions](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/) here.

### Usage

* Save image sequences (not included) in a folder, such as `example`.
* Run following Script in Python (example in 'tracker/example.py'), script will generate a bundler file 'bundle.out' in the image folder.
```
python example.py
```
* Run following command to perform bundle adjustment using Ceres Solver, obtain a PLY file with sparse result.
```
ceres-bin/bin/bundle_adjuster --input=path/to/bundle.out
```
### To-Do

* Currently BA does not terminate at the right place. It is hence set to terminate at 10th iteration with reasonable error.
* Rewrite Examples.
* More test cases to prove that it is robust, as the Kit is written from scratch. It should achieve similar reconstruction result as the version I coded for FYP (Currently no).


### Note

I re-wrote SAM Kit from scratch for following reasons:
* The original one I wrote for FYP is full of hacking. I re-organised the Python Code, made it neat and structured, added some documentation in the code for quick reference, consdering it may be used for further research development
* This SAM kit is modified from Ceres Solver, removing most of the unnecesary parts, building is faster than previous version.

I did not include the multiple sparse matching, as it is not current priority.