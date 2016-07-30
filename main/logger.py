import logging

# create logger
logger = logging.getLogger("ceres solver")
logger.setLevel(logging.DEBUG)
 
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
 
# create formatter
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
 
# add formatter to ch
ch.setFormatter(formatter)
 
# add ch to logger
logger.addHandler(ch)