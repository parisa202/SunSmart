
# Imports the Google Cloud client library
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/Parisa/Downloads/norse-sequence-418921-300db4e0d1a3.json"



def run_quickstart() -> vision.EntityAnnotation:
    """Provides a quick start example for Cloud Vision."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The URI of the image file to annotate
    file_uri = "https://images.pexels.com/photos/70497/pexels-photo-70497.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    image = vision.Image()
    image.source.image_uri = file_uri

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:")
    for label in labels:
        print(label.description)

    return labels


if __name__ == "__main__":
    print(run_quickstart())
    
    
    