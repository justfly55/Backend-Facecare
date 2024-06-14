import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import numpy as np
import io
from PIL import Image
from flask import Flask, request, jsonify


model = keras.models.load_model('FaceCare_Xception_v1.h5')

def transform_image(pillow_img):
    """Transform the image to the required input shape and format."""
    # Resize image to (600, 600)
    pillow_img = pillow_img.resize((600, 600))
    
    # Convert the image to a numpy array
    img_array = np.array(pillow_img)
    
    # Ensure the image has 3 channels (RGB), if the image is grayscale, we need to convert it
    if len(img_array.shape) == 2 or img_array.shape[2] == 1:
        img_array = np.stack((img_array,)*3, axis=-1)
    
    # Normalize the image (optional, depending on how your model was trained)
    img_array = img_array / 255.0
    
    # Expand dimensions to match the input shape of the model (1, 600, 600, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict(image_tensor):
    """Predict the class of the input image using the loaded model."""
    predictions = model.predict(image_tensor)[0][0]
    if predictions > 0.5:
        return "Sehat", predictions
    else:
        return "Jerawat", predictions

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            tensor = transform_image(pillow_img)
            kondisi, prediction = predict(tensor)
            data = {"kondisi": str(kondisi),
                    "prediction": float(prediction)}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)