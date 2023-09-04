import pandas as pd
import glob
import os
import platform
from ultralytics import YOLO
from src import getGeotag
from src import get_predict
from src import getDatetime
from src import gen_heatmap
from src import getStats
from src import getWeather

def pipeline(dirs):
    ops=platform.system().lower()
    parent="data/"
    print(os.getcwd())
    model=YOLO("models/train4.onnx",task="detect")
    # preds="prediction_"+dirs+".csv"
    preds = "prediction_" + dirs + ".csv"
    geotag="geotag_"+dirs+".csv"
    datetime="datetime_"+dirs+".csv"
    dirs=parent+dirs+"/"
    imgs=glob.glob(dirs+"*.jpg")
    print(len(imgs))
    get_predict.write_to_csv(dirs,model,preds)
    getGeotag.write_to_csv(imgs,ops,geotag)
    getDatetime.write_to_csv(imgs,ops,datetime)
    predict_df=pd.read_csv(preds)
    geotag_df=pd.read_csv(geotag)
    datetime_df=pd.read_csv(datetime)
    merged_df=predict_df.merge(geotag_df, on ="IMG_ID",how='outer')
    merged_df=merged_df.merge(datetime_df,on="IMG_ID",how='outer')
    drops="Unnamed: 0"
    merged_df.drop([drops],axis=1,inplace=True)
    merged_csv="merged_"+preds
    merged_df.to_csv('merged'+preds)
    merged_df=pd.read_csv("merged"+preds)
    gen_heatmap.gen_heatmap(merged_df)
    getWeather.get_data(geotag)
    getStats.getPlasticlevel('merged'+preds)
    if os.path.exists(preds):
        os.remove(preds)
    if os.path.exists(geotag):
        os.remove(geotag)
    if os.path.exists(datetime):
        os.remove(datetime)
    print("written results to "+"merged"+preds)

