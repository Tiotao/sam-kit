import os
import numpy as np
import cv2
import itertools
import config
from logger import logger



class Position3D:
	def __init__(self, position):
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]
	def __str__(self):
		return "%s %s %s" % (self.x, self.y, self.z)


class Position2D:
	def __init__(self, position):
		self.u = position[0]
		self.v = position[1]
	def __str__(self):
		return "%s %s" % (self.u, self.v)


class Camera:
	"""Class for camera"""
	_camera_count = 0
	def __init__(self, parameters):
		self.rot = parameters['rot']
		self.trans = parameters['trans']
		self.id = Camera._camera_count
		self.focal = parameters['focal']
		self.k1 = parameters['k1']
		self.k2 = parameters['k2']
		Camera._camera_count += 1
	
	def __str__(self):
		return "%s %s %s\n%s %s %s\n%s %s %s\n%s %s %s\n%s\n" % (self.focal, self.k1, self.k2, self.rot[0], self.rot[1], self.rot[2], self.rot[3], self.rot[4], self.rot[5], self.rot[6], self.rot[7], self.rot[8], str(self.trans))


class Observation:
	"""Class for feature observation in one camera view"""
	
	_obs_count = 0
	def __init__(self, parameters):
		self.id = Observation._obs_count
		self.position = parameters['position']
		self.camera = parameters['camera']
		Observation._obs_count += 1
	
	def __str__(self):
		return "%s %s %s" % (self.camera.id, self.id, str(self.position))

class Point:
	"""Class for an object point in 3D space"""
	_point_count = 0
	def __init__(self, parameters):
		self.id = Point._point_count
		self.position = parameters['position']
		self.color = parameters['color' ]
		self.obs_list = parameters['obsList']
		Point._point_count += 1

	def print_obs_list(self):
		print_string = ""
		for obs in self.obs_list:
			print_string = print_string + str(obs) + " "
		return print_string
	
	def __str__(self):
		return "%s\n%s %s %s\n%s\n" % (str(self.position), self.color[0], self.color[1], self.color[2], self.print_obs_list())
	

class Tracker:
	def __init__(self, image_dir):
		self.feature_params = config.FEATURE_PARAMS
		self.lucas_params = config.LOCAS_PARAMS
		self.homography_params = config.HOMOGRAPHY_PARAMS
		self.image_dir = image_dir
		self.image_paths = None
		self.corners = None
		self.reference_image_gray = None
		self.corners_optical_flow = None

	def get_corners(self):
		"""Gets Harris corners from reference image"""
		logger.info("Start Identifying Corners")
		# get absolute path of the first image
		self.image_paths = [os.path.join(self.image_dir,fn) for fn in next(os.walk(self.image_dir))[2]]
		reference_image_path = self.image_paths[0]
		logger.info("Reference Image: " + str(reference_image_path))
		# find corner in the first image
		reference_image = cv2.imread(reference_image_path)
		reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
		self.reference_image_gray = reference_image_gray
		self.reference_image = reference_image
		self.corners = cv2.goodFeaturesToTrack(reference_image_gray, **self.feature_params)
		# save corner as the first entry in optical flow array
		self.corners_optical_flow = []
		logger.info("Identified " + str(len(self.corners)) + " corners.")
		for corner in self.corners:
			self.corners_optical_flow.append([(corner.ravel()[0], corner.ravel()[1])])

	
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
		logger.info("Start Corner Tracking")
		track_image_corners = self.image_paths[1:]
		logger.info("Tracking corners in " + str(len(track_image_corners)) + " images.")
		reference_corners = self.corners
		previous_corners = reference_corners
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
																	previous_corners, 
																	None, 
																	**self.lucas_params)
			
			# remove corners that are missing in the current image
			good_tracked_corners = tracked_corners[status==1]
			reference_corners = reference_corners[status.flatten()==1]
			optical_flow = [optical_flow[i] for i, j in enumerate(status) if j == 1]

			# add tracked corner position to optical flow
			for index, corner in enumerate(optical_flow):
				new_position = good_tracked_corners[index].ravel()
				corner.append((new_position[0], new_position[1]))
			# good_reference_corners = reference_corners[status==1]
			previous_corners = good_tracked_corners.reshape(-1, 1, 2)
			reference_image_gray = current_image_gray.copy()
		
		# update corner list and optical flow
		self.corners = reference_corners
		self.corners_optical_flow = optical_flow
		logger.info("Finsihed Corner Tracking")
		logger.info(str(len(self.corners_optical_flow)) + " corners were found with complete optical flow")
		
		

	def filter_corners(self, corner_filter):
		"""Filter invalid corner to improve the accuracy and success rate of bundle adjustment"""
		if corner_filter['homography']:
			self.filter_homography_corners()
		if corner_filter['edge']:
			self.filter_edge_corners()
	
	def filter_homography_corners(self):
		"""Filter invalid corner based on homography test"""
		logger.info("Filter Corners: Homography")
		optical_flow = self.corners_optical_flow
		corners = self.corners
		num_of_corners = len(corners)
		num_of_cameras = len(optical_flow[0])
		logger.info("Starting Corners Number:" + str(num_of_corners))
		reference_corners = np.float32(corners).reshape(-1, 1, 2)
		
		# initialise a cumulative mask to indicate the validity of corners
		cumulative_mask = np.zeros((num_of_corners, 1))
		# examine the flow of each corner, see if it passes homography test in each image.
		for i in xrange(0, num_of_cameras):
			current_corners = np.float32([pt[i] for pt in optical_flow]).reshape(-1, 1, 2)
			M, mask = cv2.findHomography(reference_corners, current_corners, cv2.RANSAC, 5.0)
			cumulative_mask = cumulative_mask + mask
		cumulative_mask = cumulative_mask.flatten().tolist()
		# defines how many passes are required in a valid flow
		min_pass = num_of_cameras * (1.0 - self.homography_params['ransacThreshold'])
		for j in xrange(0, num_of_corners):
			if (cumulative_mask[j] < min_pass):
				cumulative_mask[j] = False
			else:
				cumulative_mask[j] = True
		# remove invalid corners and its optical flow
		itertools.compress(optical_flow, cumulative_mask)
		itertools.compress(corners, cumulative_mask)
		logger.info("Result Corner Number: " + str(len(corners)))
		# update corner list and optical flow
		self.corners_optical_flow = optical_flow
		self.corners = corners
		logger.info("Finished Homography filtering, updating Corners and Optical Flow")

	def update_problem(self, problem):
		"""Update Problem based on tracking results"""
		logger.info("Update Problem")
		camera_params = config.CAMERA_PARAMS
		camera_params['trans'] = Position3D((0, 0, 0))
		image_width = camera_params['imageWidth']
		image_height = camera_params['imageHeight']
		estimated_distance = camera_params['estDistance']
		points = []
		cameras = []
		observations = []
		# initialise cameras
		num_of_cameras = len(self.corners_optical_flow[0])
		for i in xrange(0, num_of_cameras):
			camera = Camera(camera_params)
			cameras.append(camera)
		# initialise corners
		for corner in self.corners:
			raw_position = corner.tolist()[0]
			# normalize opencv position representation (0 -> w, 0 -> h) to bundler position representation (-w/2 -> w/2, h/2 -> -h/2)
			position = Position3D( (int(raw_position[0] - image_width / 2), 
									int(image_height / 2 - raw_position[1]),
									estimated_distance))
			color = tuple(self.reference_image[position.x-1][position.y+1].tolist())
			point_paramaters = dict( position = position,
									 color = color,
									 obsList = [])
			point = Point(point_paramaters)
			points.append(point)
		# add observations
		for corner_id, flow in enumerate(self.corners_optical_flow):
			point = points[corner_id]
			for camera_id, corner_position in enumerate(flow):
				camera = cameras[camera_id]
				position = Position2D((corner_position[0] - image_width / 2, image_height / 2 - corner_position[1]))
				observation = Observation(dict( position = position,
												camera = camera))
				point.obs_list.append(observation)
		
		problem.pts = points
		problem.cam = cameras

		
	def create_bundler_file(self, problem):
		"""Write Problem into a Bundler file"""
		# content = "# Bundle file v0.3\n%s %s\n" % (str(len(problem.cam)), str(len(problem.pts)))
		content = "%s %s\n" % (str(len(problem.cam)), str(len(problem.pts))) # no Bundle File header
		for cam in problem.cam:
			content = content + str(cam)
		for pt in problem.pts:
			content = content + str(pt)
		logger.info("Write Problem into Bundler file: " + self.image_dir + "/bundle.out")
		with open(self.image_dir + '/bundle.out', 'w') as f:
			f.write(content) 


class Problem:
	def __init__(self, image_dir):
		self.image_dir = image_dir
		self.cam = []
		self.pts = []
	
	def track(self):
		"""Tracks Harris corners using KLT Optical Flow"""
		corner_filter = config.CORNER_FILTER
		tracker = Tracker(self.image_dir)
		tracker.get_corners()
		tracker.track_corners()
		tracker.filter_corners(corner_filter)
		tracker.draw_optical_flow()
		tracker.update_problem(self)
		tracker.create_bundler_file(self, version)

	# def bundle(self):


