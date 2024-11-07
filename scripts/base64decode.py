import base64
import json
import os
import zlib

# Set the path to the resource folder relative to the script's location
resource_folder = os.path.join(os.path.dirname(__file__), "../resource")

# Iterate through each .bp file in the resource folder
for filename in os.listdir(resource_folder):
    if filename.endswith(".bp"):
        file_path = os.path.join(resource_folder, filename)
        
        # Read the base64-encoded blueprint file
        with open(file_path, "r") as file:
            blueprint_base64 = file.read().strip()
        
        try:
            # Remove the version byte and decode the base64 string
            blueprint_data = base64.b64decode(blueprint_base64[1:])

            # Decompress the zlib-compressed data
            decompressed_data = zlib.decompress(blueprint_data)
            
            # Load the JSON data
            blueprint_json = json.loads(decompressed_data.decode('utf-8'))
            
            # Create a new file name with '-decoded' appended
            decoded_filename = f"{filename[:-3]}-decoded.json"
            decoded_file_path = os.path.join(resource_folder, decoded_filename)
            
            # Save the decoded JSON data
            with open(decoded_file_path, "w", encoding="utf-8") as decoded_file:
                json.dump(blueprint_json, decoded_file, indent=4)
            
            print(f"Decoded {filename} -> {decoded_filename}")
        
        except (base64.binascii.Error, zlib.error, json.JSONDecodeError) as e:
            print(f"Failed to decode {filename}: {e}")


