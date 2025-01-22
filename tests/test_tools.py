import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from backend.tools.image_tools import process_image
from backend.tools.pdf_tools import extract_text_from_pdf
from backend.tools.wiki_tool import fetch_wikipedia_summary

@pytest.fixture
def sample_pdf():
    """Load a sample PDF for testing."""
    with open(r"assests\cureus-0015-00000037574.pdf", "rb") as pdf_file:
        return pdf_file.read()

@pytest.fixture
def sample_image():
    """Load a sample image for testing."""
    with open(r"assests\pest-and-disease_turkey-tail_banner_1440x500.jpeg", "rb") as img_file:
        return img_file.read()

def test_process_image(sample_image):
    """Test that image processing returns a response."""
    response = process_image(sample_image)
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"

def test_extract_text_from_pdf(sample_pdf):
    """Test that text extraction from a PDF works."""
    text = extract_text_from_pdf(sample_pdf)
    assert isinstance(text, str), "Extracted text should be a string"
    assert len(text) > 0, "Extracted text should not be empty"

# def test_fetch_wikipedia_summary():
#     """Test Wikipedia API call."""
#     response = fetch_wikipedia_summary("Red Fox")
#     assert isinstance(response, str), "Response should be a string"
#     assert len(response) > 0, "Wikipedia summary should not be empty"
