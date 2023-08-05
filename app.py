from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from warnings import filterwarnings
import zipfile
# from sklearn.preprocessing import StandardScaler
# from src.pipeline.predict_pipeline import CustomData,PredictPipeline
# from src.mergeGeotag import pipeline
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=1024*1024*1024
filterwarnings('ignore')

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return """<form action="." method="post" enctype=multipart/form-data>
        <input type="file" accept="application/zip" name="data_zip_file" accept="application/zip" required>
         <button type="submit">Send zip file!</button>
        </form>"""

    else:
        file = request.files['data_zip_file']  
        file_like_object = file.stream._file
        # fname=file_like_object.split(".")[0]  
        with zipfile.ZipFile(file_like_object, 'r') as zip_ref:
    # Iterate through all the files in the zip archive
            for file_info in zip_ref.infolist():
        # Check if the file has a .jpg extension
                if file_info.filename.lower().endswith('.jpg'):
            # Extract the file to the specified directory
                    zip_ref.extract(file_info, path="data")
        print("extracted to data folder")
        return """ <h1> written to data folder</h1>
"""
        
        # data=CustomData(
        #     pregnancies=float(request.form.get('pregnancies')),
        #     glucose=float(request.form.get('glucose')),
        #     bloodPressure=float(request.form.get('bloodPressure')),
        #     skinThickness=float(request.form.get('skinThickness')),
        #     insulin=float(request.form.get('insulin')),
        #     BMI=float(request.form.get('BMI')),
        #     diabetesPedigreeFunction=float(request.form.get('diabetesPedigreeFunction')),
        #     age=float(request.form.get('age'))
        # )
        
        # pred_df=data.get_data_as_data_frame()
        # print(pred_df)
        # predict_pipeline=PredictPipeline()
        # results=predict_pipeline.predict(pred_df)
        # result = 'Non-Diabetic' if not results else 'Diabetic'
        # result = result
        # return render_template('home.html',results=result, table=pred_df.to_html(index=False))
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True, port='5000')        

