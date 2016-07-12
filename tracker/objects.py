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
		self.rot = parameters.rot || (0, 0, 0, 0, 0, 0, 0, 0)
		self.trans = parameters.trans || Position3D(0, 0, 0)
		self.id = Camera.cameraCount
		self.focal = parameters.focal || 1720
		self.k1 = parameters.k1 || 0
		self.k2 = parameters.k2 || 0
		Camera.cameraCount += 1
	
	def __str__(self):
		return "%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s\n" % self.focal, self.k1, self.k2, self.rot[0], self.rot[1], self.rot[2], self.rot[3], self.rot[4], self.rot[5], self.rot[6], self.rot[7], self.rot[8], str(self.trans)


class Observation:
	'class for feature observation in one camera view'
	observationCount = 0
	def __init__(self, parameters):
		self.id = Observation.obsCount
		self.position = parameters.position || Position2D(0, 0)
		self.color = parameters.color || (0, 0, 0)
		self.camera = parameters.camera
		Observation.obsCount += 1
	
	def __str__(self):
		return "%s %s %s" % self.camera.id, self.id, str(self.position)

class Point:
	'class for an object point in 3D space'
	pointCount = 0
	def __init__(self, parameters):
		self.id = Point.pointCount
		self.position = parameters.position || Position3D(0, 0, 0)
		self.color = parameters.color
		self.obsList = parameters.obsList || []

	def printObsList(self):
		printString = ""
		for obs in obsList:
			printString = printString + str(obs) + " "
		return printString
	
	def __str__(self):
		return "%s\n%s %s %s\n%s\n" % str(self.position), self.color[0], self.color[1], self.color[2], printObsList
	


class Problem:
	def __init__(self, imageDir):
		self.imageDir = imageDir
		self.cam = []
		self.obs = []
		self.pts = []
	
	def track(self):

	
	def bundle(self):
