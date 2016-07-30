import sys
# append objects directory in system path
sys.path.append('../main')
from objects import Problem

# create a problem object with (image_directory, output_directory)
# image directory contains image sequences, output directory contains output files
p = Problem('images', 'output')
# feature tracking
p.track()
# bundle adjustment
p.bundle()