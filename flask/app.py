from flask import Flask, render_template, request, jsonify
from keras.models import load_model
import cv2
import numpy as np
import base64
from PIL import Image
from keras_preprocessing import image
import io

#img_size=100

app = Flask(__name__) 

#model=load_model('/model_f/saved_model.pb')

# import the model
def get_model():
    global model
    model=load_model('xray_model.h5')
    print(" * Model loaded")

label_dict={0:'Normal', 1:'Pneumonia'}

#img = image.load_img(path, target_size=(200, 200),color_mode='grayscale')
target_size=(200,200)

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

# def preprocess(img):

# 	img=np.array(img)

# 	if(img.ndim==3):
# 		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# 	else:
# 		gray=img

# 	gray=gray/255
# 	resized=cv2.resize(gray,(img_size,img_size))
# 	reshaped=resized.reshape(1,img_size,img_size)
# 	return reshaped

@app.route("/")
def index():
	return(render_template("index.html"))

# @app.route("/predict", methods=["GET", "POST"])
# #predict
# def predict():
#     message=request.get_json(force=True)
#     encoded = message['image']
#     decoded=base64.b64decode(encoded)
#     image = Image.open(io.BytesIO(decoded))
#     processed_image = preprocess_image(image, target_size=(200,200))
#     img_preds= model.predict(image)


@app.route("/predict", methods=["POST"])
def predict():
	print('HERE')
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image = Image.open(dataBytesIO)
	test_image=preprocess_image(image, target_size=(200,200))
	prediction = model.predict(test_image)

	result=np.argmax(prediction,axis=1)[0]
	accuracy=float(np.max(prediction,axis=1)[0])

	label=label_dict[result]

	print(prediction,result,accuracy)

	response = {'prediction': {'result': label,'accuracy': accuracy}}

	return jsonify(response)

#app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, port=4545)

#<img src="" id="img" crossorigin="anonymous" width="400" alt="Image preview...">