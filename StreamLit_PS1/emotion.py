# Import required libraries
import streamlit as st
import cv2
import numpy as np
from PIL import Image as PILImage
import tensorflow as tf
import tensorflow_hub as hub

st.set_page_config(
    page_title="Surf",
    page_icon="assets/logo.jpeg",
)
# Load the pre-trained emotion recognition model (VGG-Face)
emotion_model_path = "best_model.h5"  # Replace this with the actual path
emotion_model = tf.keras.models.load_model(emotion_model_path,compile=False)
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

# Dictionary to map emotions to their respective images in the "assets" folder
emotion_images = {
    "angry": "assets/angry.png",
    "disgust": "assets/disgust.png",
    "fear": "assets/fear.png",
    "happy": "assets/happy.png",
    "neutral": "assets/neutral.png",
    "sad": "assets/sad.png",
    "surprise": "assets/surprise.png"
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

# Streamlit app
def main():
    # Set title and description
    st.title("Emotion Recognition from Image")
    st.write("Upload an image of your facial expression to recognize your emotion!")

    # Upload user-provided image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Text area to accept user's emotion prompt
    user_prompt = st.text_area("How are you feeling today?")

    if uploaded_image is not None:
        # Display the uploaded image
        image = PILImage.open(uploaded_image)
        # Resize the image to reduce its size
        image = image.resize((400, 400))
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Process the image and identify the emotion
        emotion = identify_emotion(np.array(image))

        # Display the identified emotional status
        st.write(f"Emotional Status: {emotion}")

        # Check if the user prompt is a valid emotion and display the corresponding image
        if emotion in emotion_images:
            emotion_image = PILImage.open(emotion_images[emotion])
            # Resize the emotion image to reduce its size
            emotion_image = emotion_image.resize((400, 400))
            st.image(emotion_image, caption=f'{emotion.capitalize()} Image', use_column_width=True)
            
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# Run the app
if __name__ == "__main__":
    main()
