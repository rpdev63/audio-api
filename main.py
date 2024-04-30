"""
Module to define FastAPI endpoints for sound prediction.
"""

import json
import numpy as np
from fastapi import UploadFile, File, FastAPI
from keras.models import load_model
from utils import FeatureExtractor

app = FastAPI()


@app.get("/")
def root():
    """
    Endpoint
    """
    return {"Hello": "World"}


def extract_features(filepath: str):
    """Extracts features from the audio file located at the given filepath.

    Args:
        filepath (str): The path to the audio file.

    Returns:
        features (np.ndarray): The extracted features.
    """
    feature_extractor = FeatureExtractor(
        'config/feature_extraction.json')
    return feature_extractor.extract_features(filepath)


def process_predictions(predictions: np.ndarray, classes_dictionary_json: str):
    """Processes the model predictions and returns the probabilities and corresponding classes.

    Args:
        predictions (np.ndarray): _description_
        classes_dictionary_json (_type_): _description_

    Returns:
        prediction_probabilities (List[float]): The probabilities of each class.
        prediction_classes (List[str]): The corresponding class names.
    """
    with open(classes_dictionary_json, 'r', encoding='utf-8') as file:
        class_dictionary = json.load(file)
    # Sort classes by keys
    classes = [class_dictionary[key]
               for key in sorted(class_dictionary.keys())]
    classes = np.array(classes)
    top_predictions_indices = np.argsort(predictions)[::-1]
    return predictions[top_predictions_indices], classes[top_predictions_indices]


@app.post("/predict")
async def predict_sound(audio_file: UploadFile = File(...)):
    """Endpoint to predict the class of an uploaded audio file.

    Args:
        audio_file (UploadFile, optional): The uploaded audio file.

    Returns:
        json: response containing the probabilities and classes of the predictions.
    """

    features = extract_features(audio_file.file)
    print(features)
    features = np.expand_dims(features, 0)
    model = load_model('models/best_model.keras')
    predictions = model.predict(features)[0]
    # Process predictions and render results
    prediction_probabilities, prediction_classes = process_predictions(predictions,
                                                                       'config/classes.json')
    print(prediction_probabilities)
    return {"probas": prediction_probabilities.tolist(),
            "classes": prediction_classes.tolist()}
