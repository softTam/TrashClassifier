import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./norse-lens-411805-d1b767e58bfa.json"
def localize_objects(path):
    """Localize objects in the local image.
    Args:
    path: The path to the local file.
    """
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    return objects[0].name

if __name__ == '__main__':
    print(localize_objects('./banana.jpeg'))