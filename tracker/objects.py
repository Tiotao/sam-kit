import os
import numpy as np
import cv2

class Position2D:
	def __init__(self, position):
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]
	def __str__(self):
		return "%s %s %s" % self.x, self.y, self.z


class Position3D:
	def __init__(self, position):
		self.u = position[u]
		self.v = position[v]
	def __str__(self):
		return "%s %s" % self.u, self.v


class Camera:
	'class for camera'
	cameraCount = 0
	def __init__(self, parameters):
		self.rot = parameters.rot or (0, 0, 0, 0, 0, 0, 0, 0)
		self.trans = parameters.trans or Position3D(0, 0, 0)
		self.id = Camera.cameraCount
		self.focal = parameters.focal or 1720
		self.k1 = parameters.k1 or 0
		self.k2 = parameters.k2 or 0
		Camera.cameraCount += 1
	
	def __str__(self):
		return "%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s\n" % self.focal, self.k1, self.k2, self.rot[0], self.rot[1], self.rot[2], self.rot[3], self.rot[4], self.rot[5], self.rot[6], self.rot[7], self.rot[8], str(self.trans)


class Observation:
	'class for feature observation in one camera view'
	observationCount = 0
	def __init__(self, parameters):
		self.id = Observation.obsCount
		self.position = parameters.position or Position2D(0, 0)
		self.color = parameters.color or (0, 0, 0)
		self.camera = parameters.camera
		Observation.obsCount += 1
	
	def __str__(self):
		return "%s %s %s" % self.camera.id, self.id, str(self.position)

class Point:
	'class for an object point in 3D space'
	pointCount = 0
	def __init__(self, parameters):
		self.id = Point.pointCount
		self.position = parameters.position or Position3D(0, 0, 0)
		self.color = parameters.color
		self.obsList = parameters.obsList or []

	def printObsList(self):
		printString = ""
		for obs in obsList:
			printString = printString + str(obs) + " "
		return printString
	
	def __str__(self):
		return "%s\n%s %s %s\n%s\n" % str(self.position), self.color[0], self.color[1], self.color[2], printObsList
	

class Tracker:
	def __init__(self, imageDir):
		self.featureParams = dict(  maxCorners = 5000,
									qualityLevel = 0.02,
									minDistance = 40,
									blockSize = 20,
									mask = None,
									useHarrisDetector=True)
		self.lucasPramas = dict(	winSize  = (20,20),
                 					maxLevel = 8,
                  					criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.3))
		self.imageDir = imageDir
		self.imagePaths = None
		self.corners = None
		self.referenceImageGray = None

	def getCorners(self):
		# get absolute path of the first image
		self.imagePaths = [os.path.join(self.imageDir,fn) for fn in next(os.walk(self.imageDir))[2]]
		referenceImagePath = self.imagePaths[0]

		# find corner in the first image
		referenceImage = cv2.imread(referenceImagePath)
		referenceImageGray = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)
		self.referenceImageGray = referenceImageGray
		self.corners = cv2.goodFeaturesToTrack(referenceImageGray, **self.featureParams)
	
	def trackCorners(self):
		trackImagePaths = self.imagePaths[1:]
		referenceCorners = self.corners
		# track corners on each image
		for imagePath in trackImagePaths:
			# load tracking image
			currentImage = cv2.imread(imagePath)
			currentImageGray = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)
			# calculate optical flow
			trackedCorners, status, err = cv2.calcOpticalFlowPyrLK(referenceImageGray, currentImageGray, referenceCorners, None, **self.lucasPramas)
			goodTrackedCorners = trackedCorners[status==1]
			# goodReferenceCorners = referenceCorners[status==1]
			referenceCorners = goodTrackedCorners.reshape(-1, 1, 2)
		self.corners = referenceCorners


class Problem:
	def __init__(self, imageDir):
		self.imageDir = imageDir
		self.cam = []
		self.obs = []
		self.pts = []
	
	def track(self):
		cornerFilter = dict( edge = True,
							 homography = True)
		tracker = Tracker(self.imageDir)
		tracker.getCorners()
		# tracker.trackCorners()
		# tracker.filterCorners(cornerFilter, )
		
		

	
	# def bundle(self):


