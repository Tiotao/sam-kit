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
	"""Class for camera"""
	_camera_count = 0
	def __init__(self, parameters):
		self.rot = parameters.rot or (0, 0, 0, 0, 0, 0, 0, 0)
		self.trans = parameters.trans or Position3D(0, 0, 0)
		self.id = Camera._camera_count
		self.focal = parameters.focal or 1720
		self.k1 = parameters.k1 or 0
		self.k2 = parameters.k2 or 0
		Camera._camera_count += 1
	
	def __str__(self):
		return "%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s\n" % self.focal, self.k1, self.k2, self.rot[0], self.rot[1], self.rot[2], self.rot[3], self.rot[4], self.rot[5], self.rot[6], self.rot[7], self.rot[8], str(self.trans)


class Observation:
	"""Class for feature observation in one camera view"""
	
	_obs_count = 0
	def __init__(self, parameters):
		self.id = Observation._obs_count
		self.position = parameters.position or Position2D(0, 0)
		self.color = parameters.color or (0, 0, 0)
		self.camera = parameters.camera
		Observation._obs_count += 1
	
	def __str__(self):
		return "%s %s %s" % self.camera.id, self.id, str(self.position)

class Point:
	"""Class for an object point in 3D space"""
	_point_count = 0
	def __init__(self, parameters):
		self.id = Point._point_count
		self.position = parameters.position or Position3D(0, 0, 0)
		self.color = parameters.color or (0, 0, 0)
		self.obs_list = parameters.obs_list or []
		Point._point_count += 1

	def print_obs_list(self):
		print_string = ""
		for obs in obs_list:
			print_string = print_string + str(obs) + " "
		return print_string
	
	def __str__(self):
		return "%s\n%s %s %s\n%s\n" % str(self.position), self.color[0], self.color[1], self.color[2], print_obs_list()
	

class Tracker:
	def __init__(self, image_dir):
		self.feature_params = dict(  maxCorners = 1000,
									qualityLevel = 0.02,
									minDistance = 40,
									blockSize = 20,
									mask = None,
									useHarrisDetector=True)
		self.lucas_params = dict(	winSize  = (25,25),
                 					maxLevel = 8,
                  					criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.3))
		self.image_dir = image_dir
		self.image_paths = None
		self.corners = None
		self.reference_image_gray = None
		self.corners_optical_flow = None

	def get_corners(self):
		"""Gets Harris corners from reference image"""
		# get absolute path of the first image
		self.image_paths = [os.path.join(self.image_dir,fn) for fn in next(os.walk(self.image_dir))[2]]
		reference_image_path = self.image_paths[0]
		# find corner in the first image
		reference_image = cv2.imread(reference_image_path)
		reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
		self.reference_image_gray = reference_image_gray
		self.corners = cv2.goodFeaturesToTrack(reference_image_gray, **self.feature_params)
		# save corner as the first entry in optical flow array
		self.corners_optical_flow = []
		for corner in self.corners:
			self.corners_optical_flow.append([(corner.ravel()[0], corner.ravel()[1])])
		print self.corners_optical_flow
	
	def draw_optical_flow(self):
		"""Draws tracked optical flow"""
		image = cv2.imread(self.image_paths[0])
		mask = np.zeros_like(image)
		for corner in self.corners_optical_flow:
			corner = np.array(corner, np.int32).reshape((-1,1,2))
			cv2.polylines(mask, [corner], False, (0,255,255))
		image = cv2.add(image, mask)
		cv2.imwrite('optical_flow.jpg', image)
	
	def track_corners(self):
		"""Tracks selected corners in the rest of the images"""
		track_image_corners = self.image_paths[1:]
		reference_corners = self.corners
		optical_flow = self.corners_optical_flow
		reference_image_gray = self.reference_image_gray
		# track corners on each image
		for image_path in track_image_corners:
			# load image to be tracked
			current_image = cv2.imread(image_path)
			current_image_gray = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
			# calculate optical flow on that image
			tracked_corners, status, err = cv2.calcOpticalFlowPyrLK(reference_image_gray, 
																	current_image_gray, 
																	reference_corners, 
																	None, 
																	**self.lucas_params)
			
			# remove corners that are missing in the current image
			good_tracked_corners = tracked_corners[status==1]
			optical_flow = [optical_flow[i] for i, j in enumerate(status) if j == 1]

			# add tracked corner position to optical flow
			for index, corner in enumerate(optical_flow):
				new_position = good_tracked_corners[index].ravel()
				corner.append((new_position[0], new_position[1]))
			# good_reference_corners = reference_corners[status==1]
			reference_corners = good_tracked_corners.reshape(-1, 1, 2)
			reference_image_gray = current_image_gray.copy()

		self.corners = reference_corners
		self.optical_flow = optical_flow
		self.draw_optical_flow()



class Problem:
	def __init__(self, image_dir):
		self.image_dir = image_dir
		self.cam = []
		self.obs = []
		self.pts = []
	
	def track(self):
		"""Tracks Harris corners using KLT Optical Flow"""
		corner_filter = dict(edge = True,
							 homography = True)
		tracker = Tracker(self.image_dir)
		tracker.get_corners()
		tracker.track_corners()
		# tracker.filter_corners(cornerFilter, )
		# tracker.update_problem()
		
		

	
	# def bundle(self):


