from PIL import Image
import csv
import glob
import os

def extract_datetime(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Extract the geotag data
    exif_data = image._getexif()
    if exif_data is not None and 36867 in exif_data:
        image_data = exif_data[36867]
        return image_data
    
    return None

def write_to_csv(image_paths,os, csv_file):
    os_list=["linux","windows"]
    if os in os_list:
        if os=="linux":
            delimit="/"
        else:
            delimit="\\"
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["IMG_ID", "Date", "Time"])
            
            for image_path in image_paths:
                date_time = extract_datetime(image_path)
                image_name = image_path.split(delimit)[-1]
                
                if date_time is not None:
                    img_date,img_time = date_time.split(" ")
                    img_date = img_date.replace(':','-')
                    writer.writerow([image_name, img_date,img_time])
                    
                    # print(f"Timestamp data extracted for {image_path} and written to CSV.")
                else:
                    print(f"No Timestamp data found for {image_path}.")
    else:
        print("os not recognized")
def find_jpeg_files(folder_path):
    jpeg_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                jpeg_files.append(os.path.join(root, file))
    return jpeg_files

if __name__=="__main__":

    folder_path =input("Enter the folder path:")
    jpg_paths = find_jpeg_files(folder_path)
    output_csv_file = input("Enter output filename(without extenstion):") + ".csv"

    #Generate Timestamp CSV 
    write_to_csv(jpg_paths, output_csv_file)

    # for path,output_csv in zip(image_paths,output_csv_files):
    #     write_to_csv(path, output_csv)
    print("Done Extracting TimeStamp Data")