import trimesh
import numpy as np
from tqdm import tqdm
import argparse

def estimate_obj_size(mesh):
    # Rough estimate: each vertex is about 40 bytes, each face about 15 bytes
    estimated_size = (len(mesh.vertices) * 40 + len(mesh.faces) * 15) / (1024 * 1024)
    return estimated_size

# Load the OBJ file
parser = argparse.ArgumentParser(description='Simplify a 3D mesh file.')
parser.add_argument('input_file', help='Path to the input OBJ file')
parser.add_argument('output_file', help='Path for the output simplified OBJ file')
parser.add_argument('--max_size', type=float, default=100, help='Maximum target size in MB (default: 100)')
args = parser.parse_args()

# Use the command-line arguments
input_file = args.input_file
output_file = args.output_file
max_size = args.max_size

print(f"Loading mesh from {input_file}")
mesh = trimesh.load_mesh(input_file)

print("Original mesh:", mesh)
original_size = estimate_obj_size(mesh)
print(f"Estimated original size: {original_size:.2f} MB")

# Simplify the mesh
target_faces = len(mesh.faces)
estimated_size = original_size

while estimated_size > max_size:
    target_faces = int(target_faces * 0.9)  # Reduce by 10%
    simplified_mesh = mesh.simplify_quadric_decimation(target_faces)
    estimated_size = estimate_obj_size(simplified_mesh)
    print(f"Reduced to {len(simplified_mesh.faces)} faces. Estimated size: {estimated_size:.2f} MB")
    mesh = simplified_mesh  # Update mesh for next iteration if needed

print("Final simplified mesh:", mesh)

# Export the final result
mesh.export(output_file)
print(f"Exported final simplified mesh to {output_file}")