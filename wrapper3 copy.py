#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

import open3d as o3d
from sympy import python

def get_depth_at_pixel(depth_frame, pixel_x, pixel_y):
	"""
	Get the depth value at the desired image point

	Parameters:
	-----------
	depth_frame 	 : rs.frame()
						   The depth frame containing the depth information of the image coordinate
	pixel_x 	  	 	 : double
						   The x value of the image coordinate
	pixel_y 	  	 	 : double
							The y value of the image coordinate

	Return:
	----------
	depth value at the desired pixel

	"""
	return depth_frame.as_depth_frame().get_distance(round(pixel_x), round(pixel_y))

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)


    # Start streaming from file
    cfg = pipeline.start(config)
    profile = cfg.get_stream(rs.stream.depth) # Fetch stream profile for depth stream
    
    # Downcast to video_stream_profile and fetch intrinsics
    intrinsics = profile.as_video_stream_profile().get_intrinsics() 
    
    # Convert to PinholeCameraIntrisic Object
    o3d_intrinsic = o3d.camera.PinholeCameraIntrinsic(
    width=intrinsics.width,
    height=intrinsics.height,
    fx=intrinsics.fx,
    fy=intrinsics.fy,
    cx=intrinsics.ppx,
    cy=intrinsics.ppy
)
    # Create opencv window to render image in
    # cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer()

    # Get frameset of depth
    frame = pipeline.wait_for_frames()

    # Get depth frame
    depth_frames = frame.get_depth_frame()

    # Colorize depth frame to jet colormap
    depth_color_frame = colorizer.colorize(depth_frames)

    # Convert depth_frame to numpy array to render image in opencv
    depth_image = np.asarray(depth_frames.get_data(), dtype=np.uint32)
    
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    
    # IMAGE_WIDTH = 640
    # IMAGE_HEIGHT = 480

    framesize = IMAGE_WIDTH * IMAGE_HEIGHT
    
    teste = []

    # Loop para obter o valor de profundide de cada pixel
    for y in range(IMAGE_HEIGHT):
        for x in range(IMAGE_WIDTH):
            valor = get_depth_at_pixel(depth_frame=depth_frames, pixel_x=x, pixel_y=y)
            
            # Checagem para limitar a profundidae a 3 metros
            if valor > 3:
                 valor = 3
                 teste.append(valor)
            else:
                teste.append(valor)

    # array16 = depth_image.astype(np.uint16)
    
    # reshape = np.reshape(array16, (IMAGE_HEIGHT, IMAGE_WIDTH))
    
    
    array = np.asanyarray(teste, dtype=np.double)
    # Conversão do valor de profundidade de metros para milímetros
    array *= 10000
    
    array16 = array.astype(np.uint16)

    reshape = np.reshape(array16, (IMAGE_HEIGHT, IMAGE_WIDTH))
    
    
    depth_o3d_image = o3d.geometry.Image(reshape)
    
    extrinsic = np.eye(4)

    point_cloud = o3d.geometry.PointCloud.create_from_depth_image(
    depth=depth_o3d_image,
    intrinsic=o3d_intrinsic,
    extrinsic=extrinsic,
    depth_scale=10000.0,
    depth_trunc=1.5,
    stride=1,
    project_valid_depth_only=True
)
    point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    o3d.visualization.draw_geometries([point_cloud])

    
    plane_model, inliers = point_cloud.segment_plane(distance_threshold=0.018,
                                         ransac_n=3,
                                         num_iterations=3000)
    #quanto maior o distance_threshold mais plano é removido

    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    inlier_cloud = point_cloud.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
    # outlier_cloud.paint_uniform_color([0, 1.0, 0])  # Outliers em verde
    o3d.io.write_point_cloud("C:/Users/mhmon/ovos-pv/sem_pano/14.ply", outlier_cloud)


    o3d.visualization.draw_geometries([outlier_cloud])
# Visualizar a nuvem de pontos
    # o3d.visualization.draw_geometries([point_cloud])
    
finally:
    pass