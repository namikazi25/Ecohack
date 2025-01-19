import sys
import os

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import torch
import open_clip
from PIL import Image
import io
from backend.image_classifier import classify_with_biotrove

@pytest.fixture(scope="module")
def sample_image():
    """Load a sample image for testing."""
    #image_path = "assests\\biotrove-test.jpg"  # Ensure this file exists in `tests/`
    image_path = "C:/Users/share/Documents/Ecohack/tests/biotrove-test.jpg"
    with open(image_path, "rb") as img_file:
        return img_file.read()

def test_model_loading():
    """Check if the BioTrove-CLIP model loads properly."""
    try:
        model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('hf-hub:BGLab/BioTrove-CLIP')
        assert model is not None, "Model failed to load"
    except Exception as e:
        pytest.fail(f"Model failed to load: {str(e)}")

def test_image_classification(sample_image):
    """Check if BioTrove-CLIP correctly classifies an image."""
    try:
        prediction = classify_with_biotrove(sample_image)
        assert isinstance(prediction, str), "Prediction is not a string"
        assert len(prediction) > 0, "Prediction is empty"
        print(f"Predicted species: {prediction}")
    except Exception as e:
        pytest.fail(f"Classification failed: {str(e)}")
