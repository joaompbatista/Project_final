#from crypt import methods
from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pyttsx3

from PIL import Image



# we are going to tell python that from here downwards we have a flask app
app = Flask(__name__)

# import model
model=load_model('xray_model.h5')

# Preprocessing the image
def preprocess_image(image_path):
    image=load_img(image_path,target_size=(200,200), color_mode='grayscale')
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)
    img_preds= model.predict(image)



    if img_preds>= 0.9: 
        out = ('Humm not good news. There is a {:.2%} chance that you have Pneumonia'.format(img_preds[0][0]))
    elif img_preds>= 0.5:
        out = ('Using my deep learning capacities I will say that although not certain, you probably have Pneumonia. I am {:.2%} percent sure of it'.format(img_preds[0][0]))
    else: 
        out = ('Good news my dear patient - your lungs look marvelous. No pneumonia here. May the god of machine learning be with you!')

    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume",1)
    #engine.setProperty('voice', 'David')
    engine.say(out)
    engine.runAndWait()

    return out

    


# route
@app.route('/', methods=["POST","GET"])
def my_function():
    if request.method == "POST":
        imagefile = request.files['imagefile']
        image_path = "static/examples/" + imagefile.filename
        imagefile.save(image_path)

        predict = preprocess_image(image_path)

        return render_template("index.html", prediction = predict, img_path=image_path)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=4552)


