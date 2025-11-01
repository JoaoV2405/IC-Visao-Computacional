import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import os

def process_bag_file(input_path, output_path):
    """Processa um arquivo .bag e salva a nuvem de pontos filtrada como .ply."""
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        rs.config.enable_device_from_file(config, input_path)
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        cfg = pipeline.start(config)
        profile = cfg.get_stream(rs.stream.depth)
        intrinsics = profile.as_video_stream_profile().get_intrinsics()

        o3d_intrinsic = o3d.camera.PinholeCameraIntrinsic(
            width=intrinsics.width, height=intrinsics.height,
            fx=intrinsics.fx, fy=intrinsics.fy,
            cx=intrinsics.ppx, cy=intrinsics.ppy
        )

        frame = pipeline.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        # depth_color_frame = colorizer.colorize(depth_frames)

        depth_image = np.asarray(depth_frame.get_data(), dtype=np.uint16)

        depth_o3d_image = o3d.geometry.Image(depth_image)
        extrinsic = np.eye(4)

        point_cloud = o3d.geometry.PointCloud.create_from_depth_image(
            depth=depth_o3d_image, intrinsic=o3d_intrinsic, extrinsic=extrinsic,
            depth_scale=10000.0, depth_trunc=1.5, stride=1,
            project_valid_depth_only=True
        )
        point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

        plane_model, inliers = point_cloud.segment_plane(distance_threshold=0.018,
                                                         ransac_n=3, num_iterations=3000)
        filtered_cloud = point_cloud.select_by_index(inliers, invert=True)
        o3d.visualization.draw_geometries([filtered_cloud])

        o3d.io.write_point_cloud(output_path, filtered_cloud)
        print(f"Arquivo salvo: {output_path}")

    finally:
        pipeline.stop()

# Lista de arquivos .bag
base_path = "C:\\Users\\mhmon\\Downloads\\nuvens\\21_dias\\"
save_path = 'C:\\Users\\mhmon\\ovos-pv\\bandeija\\'
num_files = 14  # Número total de arquivos a processar  

input_file = os.path.join(f"C:\\Users\\mhmon\\Downloads\\foto.bag")
output_file = os.path.join(save_path, f"base.ply")

if os.path.exists(input_file):  # Verifica se o arquivo existe antes de processar
    process_bag_file(input_file, output_file)
