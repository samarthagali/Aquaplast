from ultralytics import YOLO
import pandas as pd
from PIL import Image
import numpy as np
import os
import torch
import warnings


#predict bounding boxes for image
def predict(model,img,img_id):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    values={} 
    values['IMG_ID']=img_id
    img=Image.open(img)
   
    result=model(img,device=device,conf=0.05,iou=0.35,verbose=False)
    boxes=result[0].boxes
    #find number of bounding boxes
    count=len(boxes)
    if count>0:
        values['PRED_LAB']='YES'
    else:
        values['PRED_LAB']='NO'
    values['PRED_CT']=len(boxes)
    return values

#cols for dataframe
cols=['IMG_ID','PRED_LAB','PRED_CT']

#fill values in dataframe and write to csv
def write_to_csv(pred_dir,weight_path,filename):
    df=pd.DataFrame(columns=cols)
    print(pred_dir,type(pred_dir))
    imgs=os.listdir(pred_dir)
    #iterate through predict directory
    for img_path in imgs:
        try:
            img=pred_dir+"/"+img_path
            row=predict(weight_path,img,img_path)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = df.append(row, ignore_index=True)
        except:
            print("error in retrieving predictions for "+img_path)
    try:
        os.makedirs("results")
    except FileExistsError:
        pass
    df.to_csv(filename)
    # print("written predictions to "+filename)
