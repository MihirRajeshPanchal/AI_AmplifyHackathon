from flask import Flask, request, jsonify
from flask_cors import CORS
import wolframalpha
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import base64
import io
from PIL import Image as PILImage

app = Flask(__name__)
CORS(app)

# Replace 'YOUR_WOLFRAM_ALPHA_APP_KEY' with your actual WolframAlpha app key
wolfram_alpha_app_key = 'JGUTQ4-RG973Q6L5E'
client = wolframalpha.Client(wolfram_alpha_app_key)

@app.route('/query', methods=['POST', 'GET'])
def process_query():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        # Process the user query using WolframAlpha API
        res = client.query(query)
        output = next(res.results).text

        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

# Load the pre-trained emotion recognition model (VGG-Face)
emotion_model_path = "best_model.h5"  # Replace this with the actual path
emotion_model = tf.keras.models.load_model(emotion_model_path, compile=False)
emotion_model.compile()

# Define the emotion mapping
emotion_mapping = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "neutral",
    5: "sad",
    6: "surprise"
}

# Function to preprocess the image (replace this with the actual preprocessing steps)
def preprocess_image(image):
    # Resize the image to the desired input size for the emotion model
    resized_image = cv2.resize(image, (224, 224))
    # Convert to RGB (VGG-Face model expects RGB images)
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    # Normalize the pixel values to be in the range [0, 1]
    normalized_image = rgb_image / 255.0
    return normalized_image

# Function to predict emotion from the preprocessed image
def predict_emotion(preprocessed_image):
    # Reshape the image to match the input shape of the emotion model
    input_image = np.expand_dims(preprocessed_image, axis=0)

    # Get the predicted emotion probabilities
    predictions = emotion_model.predict(input_image)[0]
    # Get the index of the maximum probability as the predicted class
    predicted_class_index = np.argmax(predictions)

    predicted_emotion = emotion_mapping[predicted_class_index]
    return predicted_emotion

# Function to identify emotions from facial expressions using the pre-trained model
def identify_emotion(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Use the emotion_model to predict the emotional state
    emotion = predict_emotion(preprocessed_image)

    # Return the predicted emotion
    return emotion

@app.route('/compute', methods=['POST'])
def predict_emotion_api():
    try:
        # Get the uploaded image file from the request
        if 'image' not in request.files:
            return jsonify({'message': 'No image provided'}), 400

        image = request.files['image'].read()
        image = PILImage.open(io.BytesIO(image))

        # Process the image and identify the emotion
        emotion = identify_emotion(np.array(image))

        # Return the predicted emotion as part of the response
        result = {'emotion': emotion}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='192.160.161.157')