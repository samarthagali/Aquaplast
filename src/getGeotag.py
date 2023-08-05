
from PIL import Image
import csv

def extract_geotag(image_path):
    
    image = Image.open(image_path)
    
    # Extract the geotag data
    exif_data = image._getexif()
    if exif_data is not None and 34853 in exif_data:
        geotag_data = exif_data[34853]
        return geotag_data
    
    return None

def convert_to_decimal(degrees, minutes, seconds, direction):
    # print("Converting to Decimals")
    # print(float(degrees), minutes, seconds, direction)
    # Convert degrees/minutes/seconds to decimal format
    decimal_degrees = float(degrees) + float(minutes/60) + float(seconds/3600)
    # print(decimal_degrees)
    
    # Apply the direction (N, S, E, W)
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def create_geotag_url(latitude, longitude):
    # print("Creating Geotag URL")
    # Create a geotag URL
    return f"https://www.google.com/maps?q={latitude},{longitude}"

def write_to_csv(image_paths,os, csv_file):
    # print("Begin!")
    os_list=["linux","windows"]
    if os in os_list:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IMG_ID", "Latitude", "Longitude", "GEO_Tag_URL"])
            if os=="linux":
                delimit="/"
            else:
                delimit="\\"
            
            for image_path in image_paths:
                geotag_data = extract_geotag(image_path)
                image_name = image_path.split(delimit)[-1]
                
                if geotag_data is not None:
                    # print(geotag_data)
                    latitude = convert_to_decimal(geotag_data[2][0],geotag_data[2][1],geotag_data[2][2],geotag_data[1],)
                    longitude = convert_to_decimal(geotag_data[4][0],geotag_data[4][1],geotag_data[4][2],geotag_data[3],)
                    geotag_url = create_geotag_url(latitude, longitude)
                    
                    writer.writerow([image_name, latitude, longitude, geotag_url])
                    
                    # print(f"Geotag data extracted for {image_path} and written to CSV.")
                else:
                    print(f"No geotag data found for {image_path}.")
    else:
        print("os not recognized")


