from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from warnings import filterwarnings
import zipfile

# from sklearn.preprocessing import StandardScaler
# from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.mergeGeotag import pipeline
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=1024*1024*1024
filterwarnings('ignore')

# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/heatmap')
def heatmap():
    return render_template('heatmap_plastic.html')

@app.route('/login')
def login():
    return render_template('l-o-g-i-n.html')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/contact')
def contact():
    return render_template('c-o-n-t-a-c-t.html')

@app.route('/signup')
def signup():
    return render_template('s-i-g-n-u-p.html')

@app.route('/prediction')
def prediction():
    return render_template('predict-output.html')


@app.route('/upload',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('u-p-l-o-a-d.html')
    else:
        if 'Upload' not  in  request.files:
            return Flask.redirect(request.url)
        file = request.files['Upload'] 
        fname=file.filename.split(".")[0]
        file_like_object = file.stream._file
        print(file_like_object)
        # fname=file_like_object.split(".")[0]  
        with zipfile.ZipFile(file_like_object, 'r') as zip_ref:
    # Iterate through all the files in the zip archive
            for file_info in zip_ref.infolist():
        # Check if the file has a .jpg extension
                if file_info.filename.lower().endswith('.jpg'):
            # Extract the file to the specified directory
                    zip_ref.extract(file_info, path="data")
        print("extracted to data folder")
        pipeline(fname)
        return render_template('u-p-l-o-a-d.html')
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True, port='5000')        

