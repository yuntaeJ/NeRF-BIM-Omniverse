import omni
from pxr import UsdGeom, Gf, Sdf, Usd
import json
import os
import numpy as np

# Initialize stage
stage = omni.usd.get_context().get_stage()

# Paths for the camera and path
camera_path = "/World/Camera_01"
path_path = "/World/BasisCurves"

# Get the camera and path primitives
camera_prim = stage.GetPrimAtPath(camera_path)
path_prim = stage.GetPrimAtPath(path_path)

# Assuming the path is a BasisCurves
path = UsdGeom.BasisCurves(path_prim)  # Adjust for NurbsCurves if needed

# Get points from the path for keyframes
points_attr = path.GetPointsAttr()
points = points_attr.Get()

# Time settings based on frame numbers
time_start = 1
time_end = 120  # This can be adjusted based on how quickly you want the camera to move

# Get the xformable schema of the camera
xform = UsdGeom.Xformable(camera_prim)

# Set keyframes for the camera's translation at the start and end points
translate_op = None
for op in xform.GetOrderedXformOps():
    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
        translate_op = op
        break

if not translate_op:
    raise RuntimeError("No translate op found on camera, which is needed for the script.")

# Setting points for translation
translate_op.Set(points[0], time_start)
translate_op.Set(points[-1], time_end)

# Extract the transformation matrix at each frame and store in a JSON file
frame_data = []

# Function to extract matrix
def extract_transform_matrix(camera, time):
    xformable = UsdGeom.Xformable(camera)
    world_transform = xformable.ComputeLocalToWorldTransform(time)
    translation = world_transform.ExtractTranslation()
    rotation_matrix = world_transform.ExtractRotationMatrix()
    # Invert the Z-axis rotation
    rotation_matrix[2] = -rotation_matrix[2]
    transform_matrix = np.eye(4)
    transform_matrix[:3, :3] = rotation_matrix
    transform_matrix[:3, 3] = [translation[0], translation[1], translation[2]]
    return transform_matrix.tolist()

# Loop through each frame to extract the matrix
timeline = omni.timeline.get_timeline_interface()
for current_frame in range(time_start, time_end + 1):
    matrix = extract_transform_matrix(camera_prim, current_frame)
    frame_data.append({
        "frame": current_frame,
        "transform_matrix": matrix
    })
    timeline.set_current_time(current_frame)

# Write the data to a JSON file
out_dir = 'F:/Research/Digital_twin/SMARTINSIDE/Site_BIM/BIM_Coords'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

json_file_path = os.path.join(out_dir, 'camera_transforms_bim_beam.json')
with open(json_file_path, 'w') as json_file:
    json.dump(frame_data, json_file, indent=4)

print("Data has been saved to 'camera_transforms_bim_beam.json'")

