#from crypt import methods
from flask import Flask, render_template, request, redirect
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

from PIL import Image
import base64
import io
import os
from werkzeug.utils import secure_filename


# we are going to tell python that from here downwards we have a flask app
app = Flask(__name__)

# import model
model=load_model('xray_model.h5')

app.config["IMAGE_UPLOADS"] = "static/examples"

filename = ''

# Preprocessing the image
def preprocess_image(image):
    # if image.mode!= "grayscale":
    #     image=image.convert("grayscale")
    image= image.resize(200,200)
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)


    return image

@app.route('/', methods=["POST","GET"])
def my_function():
    if request.method == "POST":
        image = request.files['file']


        if image.filename == '':
            print("Image must have a file name")
            return redirect(request.url)
        
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir, app.config["IMAGE_UPLOADS"], filename))

        img = Image.open(app.config["IMAGE_UPLOADS"]+"/"+filename)
        data = io.BytesIO()
        img.save(data, "JPEG")
        print(type(img))

        encode_img_data = base64.b64encode(data.getvalue())
        # image=load_img("./examples/"+filename,target_size=(200,200), color_mode='grayscale')
        
        


        return render_template("index.html", filename = encode_img_data.decode("UTF-8"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=4552)


