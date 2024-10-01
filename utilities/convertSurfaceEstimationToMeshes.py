import trimesh
import numpy as np
from tqdm import tqdm

# Create a simple triangle mesh
def create_triangle():
    vertices = np.array([[0, 0, 0], [0.01, 0, 0], [0, 0.01, 0]])  # 3 vertices
    faces = np.array([[0, 1, 2]])  # One face connecting the vertices
    return trimesh.Trimesh(vertices=vertices, faces=faces)

# Generate triangles at each point location
def create_triangles(points):
    triangles = []
    for p in tqdm(points, desc="Creating triangles", unit="triangle"):
        triangle = create_triangle()
        triangle.apply_translation(p)
        triangles.append(triangle)
    return trimesh.util.concatenate(triangles)

# Function to convert depth map to 3D points (simplified, no intrinsics)
def depth_to_point_cloud_no_intrinsics(depth_map):
    h, w = depth_map.shape
    points = []
    
    # Scale factors for normalizing X and Y positions
    x_scale = w / 2.0  # This will scale the x-coordinates to be centered around 0
    y_scale = h / 2.0  # This will scale the y-coordinates to be centered around 0
    
    for v in range(h):
        for u in range(w):
            Z = depth_map[v, u]
            if Z == 0:  # Skip invalid depth
                continue
            X = (u - w / 2) / x_scale  # Normalize X
            Y = (v - h / 2) / y_scale  # Normalize Y
            points.append([X, Y, Z])   # X, Y, Z is the 3D coordinate
    
    return np.array(points)

# Example usage
# Load depth map (example with random data)
depth_map = np.load(r'c:\Workspace\Dev Workspace\GraphicsProjects\AnimatableAvatars\assets\outputDepth\depthNumpy.npy')  # Replace with your depth map

# Convert depth map to point cloud

print("loaded depth map")
points = depth_to_point_cloud_no_intrinsics(depth_map)
print("converted depth map to point cloud")
# Create spheres at each point
spheres = []
print(len(points))
# Generate spheres and save to OBJ
mesh = create_triangles(points)
mesh.export('output.obj')
print("exported to obj")