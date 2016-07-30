import cv2

FEATURE_PARAMS 		= dict( maxCorners        = 5000,
							qualityLevel      = 0.03,
		 					minDistance       = 40,
							blockSize         = 20,
							mask              = None,
							useHarrisDetector = True)

LOCAS_PARAMS 		= dict( winSize  = (25,25),
                 			maxLevel = 8,
            				criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.3))

HOMOGRAPHY_PARAMS 	= dict(	ransacThreshold = 0.05)

CAMERA_PARAMS		= dict( imageWidth  = 3264,
							imageHeight = 2448,
							focal       = 2720.0,
							k1          = 0,
							k2          = 0,
							rot         = (1, 0, 0, 0, 1, 0, 0, 0, 1),
							estDistance = 700)

CORNER_FILTER		= dict( edge       = False,
							homography = True)

CERES_PARAMS        = dict( solverPath    = '../ceres-bin/bin/bundle_adjuster',
							maxIterations = 100)
