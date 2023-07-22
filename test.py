from flask import Flask, request, jsonify
from flask_cors import CORS
import wolframalpha
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import base64
import io

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

@app.route('/compute', methods=['POST'])
def compute():
    try:
        # Assuming the image is sent in the request as a file named 'image'
        if 'image' not in request.files:
            return jsonify({'message': 'No image provided'}), 400
        image = request.files['image']
        
        # Log to check if the image is correctly received
        print('Image received:', image)

        emotion_mapping = {
            0: "angry",
            1: "disgust",
            2: "fear",
            3: "happy",
            4: "neutral",
            5: "sad",
            6: "surprise"
        }
        emotion_model_path = "best_model.h5"  # Replace this with the actual path
        emotion_model = tf.keras.models.load_model(emotion_model_path)

        # Perform your computation with the image here
        # Replace this with your actual computation code

        def preprocess_image(image_data):
            try:
                # Decode the base64-encoded image data
                decoded_image = base64.b64decode(image_data)
                
                # Convert the decoded image data to a NumPy array
                np_image = np.frombuffer(decoded_image, dtype=np.uint8)
                image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
                
                # Check if the image has valid dimensions
                if image is None or image.size == 0:
                    raise ValueError("Invalid image data or empty image")
                
                # Resize the image to the desired input size for the emotion model
                resized_image = cv2.resize(image, (224, 224))
                # Convert to RGB (VGG-Face model expects RGB images)
                rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                # Normalize the pixel values to be in the range [0, 1]
                normalized_image = rgb_image / 255.0
                return normalized_image

            except Exception as e:
                print("Error in preprocess_image:", str(e))
                # Return a default value with the expected input shape of the Keras model
                return np.zeros((224, 224, 3), dtype=np.float32)

        def predict_emotion(preprocessed_image):
            # Reshape the image to match the input shape of the emotion model
            input_image = np.expand_dims(preprocessed_image, axis=0)

            # Get the predicted emotion probabilities
            predictions = emotion_model.predict(input_image)[0]
            # Get the index of the maximum probability as the predicted class
            predicted_class_index = np.argmax(predictions)
            # print('Predicted class index:', predicted_class_index)
            predicted_emotion = emotion_mapping[predicted_class_index]
            return predicted_emotion

        def identify_emotion(image):
            preprocessed_image = preprocess_image(image)
            emotion = predict_emotion(preprocessed_image)
            return emotion

        emotion = identify_emotion(image.read())
        print('Emotion:', emotion)
        # Return the emotion as part of the response
        result = {'emotion': emotion}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='192.160.161.157')
