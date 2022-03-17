import numpy as np
import io


from flask import Flask, render_template, request
from keras.models import load_model
from keras_preprocessing import image

app = Flask(__name__)

# import the model
def get_model():
    global model
    model=load_model('xray_model.h5')
    print(" * Model loaded")


#img = image.load_img(path, target_size=(200, 200),color_mode='grayscale')
#target_size=(200,200)

# Preprocessing the image
def preprocess_image(image, target_size):
    if image.mode!= "grayscale":
        image=image.convert("grayscale")
    image = image.resize(target_size)
    image = image.img_to_array(image)
    image = image/255
    image = np.expand_dims(image, axis=0)

    return image

print(" * Loading Keras model...")
get_model()

@app.route("/predict", methods=["GET", "POST"])
#predict
def predict():
    message=request.get_json(force=True)
    encoded = message['image']
    decoded=base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(200,200))
    img_preds= model.predict(image)

if __name__ == "__main__":
    app.run(debug=True, port=4545)