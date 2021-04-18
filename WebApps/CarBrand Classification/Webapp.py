from flask import Flask, request, render_template
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

MODEL_PATH = 'car_brand_model_resnet50.h5'

model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    img = image.img_to_array(img)

    x = x/255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    if preds == 0:
        preds = "The Car IS Audi"
    elif preds == 1:
        preds = "The Car is Lamborghini"
    else:
        preds = "The Car Is Mercedes"

    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result = preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
