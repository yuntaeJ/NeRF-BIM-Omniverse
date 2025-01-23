import omni.usd
import os
import json
from pxr import Gf

#Initialize the USD stage
stage = omni.usd.get_context().get_stage()

#Specify the full path where you want to save the notepath file
out_dir = 'PATH/TO/SAVE'
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

json_file_path = os.path.join(out_dir,'checkerboard_position_corners.json')
points_data1 = []
points_data2 = []
points_data3 = []

for i in range (0,40):
	prim_path = f"/World/Checkboard/Corner_{i:02d}"
	prim = stage.GetPrimAtPath(prim_path)
	
	if prim.IsValid():  # Check if the prim is valid
		matrix = omni.usd.get_world_transform_matrix(prim)  # Get the world transform matrix
		translate = matrix.ExtractTranslation()  # Extract translation from the matrix (Vec3d)
		#Convert Vec3d to list of floats for JSON serialization
		position_list = [translate[0], translate[1], translate[2]]
		# Append the data to the points_data list
		points_data1.append({
			"name": f"point_{i:02d}",
			"x": position_list[0],
			"y": position_list[1],
			"z": position_list[2],
		})
	else:
		print(f"No valid prim path: {prim_path}")
		
for i in range (0,40):
	prim_path = f"/World/Checkboard_01/Corner_{i:02d}"
	prim = stage.GetPrimAtPath(prim_path)
	
	if prim.IsValid():  # Check if the prim is valid
		matrix = omni.usd.get_world_transform_matrix(prim)  # Get the world transform matrix
		translate = matrix.ExtractTranslation()  # Extract translation from the matrix (Vec3d)
		#Convert Vec3d to list of floats for JSON serialization
		position_list = [translate[0], translate[1], translate[2]]
		# Append the data to the points_data list
		points_data2.append({
			"name": f"point_{i:02d}",
			"x": position_list[0],
			"y": position_list[1],
			"z": position_list[2],
		})
	else:
		print(f"No valid prim path: {prim_path}")
		
for i in range (0,40):
	prim_path = f"/World/Checkboard_02/Corner_{i:02d}"
	prim = stage.GetPrimAtPath(prim_path)
	
	if prim.IsValid():  # Check if the prim is valid
		matrix = omni.usd.get_world_transform_matrix(prim)  # Get the world transform matrix
		translate = matrix.ExtractTranslation()  # Extract translation from the matrix (Vec3d)
		#Convert Vec3d to list of floats for JSON serialization
		position_list = [translate[0], translate[1], translate[2]]
		# Append the data to the points_data list
		points_data3.append({
			"name": f"point_{i:02d}",
			"x": position_list[0],
			"y": position_list[1],
			"z": position_list[2],
		})
	else:
		print(f"No valid prim path: {prim_path}")
		

# Serialize the points data to json 
json_data = {"checkboard_01": points_data1,
"checkboard_02": points_data2,
"checkboard_03": points_data3}

# Write the JSON data to a file in the specified directory
with open(json_file_path, 'w') as json_file:
	json.dump(json_data, json_file, indent=4)  # Writing with indentation for readability
	
print(f"JSON file with furniture positions has been saved as '{json_file_path}'.")