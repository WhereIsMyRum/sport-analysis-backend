import utils.utils as utils
import moviepy.editor as moviepy
from math import ceil
 
path = 'tennis-video-bucket-1/user_1/f33c957413544e03e54bce5df4673f77/video.mp4'
print(utils.getBucketUserFolderAndFileFromPath(path))