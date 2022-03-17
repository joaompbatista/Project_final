from flask import Flask, render_template, request, redirect
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

from PIL import Image
import base64
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
# app.config["IMAGE_UPLOADS"] = "static/examples"

# filename = ''

@app.route('/', methods = ["GET"])
def homepage():
    return render_template('index.html')

# Preprocessing the image
def preprocess_image(image):
    # if image.mode!= "grayscale":
    #     image=image.convert("grayscale")
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)


    return image

# import the model
# def get_model():
#     global model
#     model=load_model('xray_model.h5')
#     print(" * Model loaded")

@app.route('/', methods = ["POST"])
def predict():
    imagefile = request.files['imagefile']
    image_path = "./examples/" + imagefile.filename
    imagefile.save(image_path)

    image=load_img(image_path,target_size=(200,200), color_mode='grayscale')
    # print(image)
    image = preprocess_image(image)
    print(image)
    model=load_model('xray_model.h5')
    img_preds= model.predict(image)

    if img_preds>= 0.5: 
        out = ('I am {:.2%} percent confirmed that this is a Pneumonia case'.format(img_preds[0][0]))
    
    else: 
        out = ('I am {:.2%} percent confirmed that this is a Normal case'.format(1-img_preds[0][0]))




    return render_template('index.html', predict = out)


if __name__ == "__main__":
    app.run(debug=True, port=8888)