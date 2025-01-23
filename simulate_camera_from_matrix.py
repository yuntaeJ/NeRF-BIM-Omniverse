import omni
import json
import math
from pxr import Usd, UsdGeom, Gf

# Load the JSON file
file_path = "F:/Research/Digital_twin/SMARTINSIDE/Site_BIM/Real_cam/col.json"
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract the camera parameters
camera_params = data["frames"]

# Initialize Omniverse Kit
usd_context = omni.usd.get_context()
if not usd_context:
    raise RuntimeError("Failed to get USD context")

# Get or create the stage
stage = usd_context.get_stage()
if not stage:
    usd_context.new_stage()
    stage = usd_context.get_stage()
if not stage:
    raise RuntimeError("Failed to create or get stage")

# Define camera path
camera_path = "/World/Camera"

# Create a new camera if it doesn't exist
camera_prim = stage.GetPrimAtPath(camera_path)
if not camera_prim:
    omni.kit.commands.execute('CreatePrim', prim_type='Camera', prim_path=camera_path)
    camera_prim = stage.GetPrimAtPath(camera_path)

# Get the camera's Xformable interface
camera_xform = UsdGeom.Xformable(camera_prim)

# Function to convert rotation matrix to Euler angles
def rotation_matrix_to_euler_angles(R):
    sy = math.sqrt(R[0][0] * R[0][0] +  R[1][0] * R[1][0])
    singular = sy < 1e-6
    if not singular:
        x = math.atan2(R[2][1], R[2][2])
        y = math.atan2(R[2][0], sy)
        z = math.atan2(R[1][0], R[0][0])
    else:
        x = math.atan2(R[1][2], R[1][1])
        y = math.atan2(R[2][0], sy)
        z = 180
    return Gf.Vec3d(math.degrees(x), math.degrees(y), math.degrees(z))
    
# Normalize angles to be within 0 to 360 degrees
def normalize_angles(angles):
    return Gf.Vec3d(
        angles[0] % 360,
        angles[1] % 360,
        angles[2] % 360
    )

# Retrieve existing translation and rotation operations
translate_op = camera_xform.GetOrderedXformOps()[0]
rotate_op = camera_xform.GetOrderedXformOps()[1]

# Create time codes for keyframes
start_time_code = 0
end_time_code = len(camera_params) - 1
time_codes = range(start_time_code, end_time_code + 1)

# Apply transformations to the camera at each frame and set keyframes
for i, frame in zip(time_codes, camera_params):
    transform_matrix = frame["transform_matrix"]

    # Extract translation and rotation from the transform matrix
    translation = Gf.Vec3d(transform_matrix[0][3], transform_matrix[1][3], transform_matrix[2][3])
    
    # Extract the rotation as a rotation matrix
    rotation_matrix = [
        [transform_matrix[0][0], transform_matrix[0][1], transform_matrix[0][2]],
        [transform_matrix[1][0], transform_matrix[1][1], transform_matrix[1][2]],
        [transform_matrix[2][0], transform_matrix[2][1], transform_matrix[2][2]]
    ]
    euler_angles_deg = rotation_matrix_to_euler_angles(rotation_matrix)

    # Normalize the angles to be within 0 to 360 degrees
    euler_angles_deg = normalize_angles(euler_angles_deg)

    # Adjust the Z rotation angle to align the zero angle with the -Z direction
    euler_angles_deg[2] = (euler_angles_deg[2] + 180) % 360
    
    # Set keyframes for translation
    translate_op.GetAttr().Set(translation, i)


    # Set keyframes for rotation in X-Y-Z order
    rotate_op.GetAttr().Set(euler_angles_deg, i)

# Set stage time and duration
stage.SetStartTimeCode(start_time_code)
stage.SetEndTimeCode(end_time_code)
stage.SetTimeCodesPerSecond(30)  # Set the frames per second, adjust as needed

# Set default prim
stage.GetRootLayer().defaultPrim = camera_prim.GetName()

# Save the stage (optional)
# usd_context.save_as_stage("path/to/save/stage.usda")

print("Animation setup complete. Use the Play button to start the animation.")

# If you need to stop the application, uncomment the following line
# omni.kit.app.get_app().stop()


