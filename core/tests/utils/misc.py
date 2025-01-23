from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core.tests.fixtures.constants import DOMAIN, PROTOCOL


def create_upload_image_file(filename="test_image.jpg", size=(100, 100), format="JPEG"):
    image = Image.new("RGB", size, color=(255, 0, 0))
    image_file = BytesIO()
    image.save(image_file, format=format)
    image_file.seek(0)
    return SimpleUploadedFile(
        filename, content=image_file.read(), content_type=f"image/{format.lower()}"
    )


def full_url(
    url,
    query_term=None,
    protocol=PROTOCOL,
    domain=DOMAIN,
):
    return f"{protocol}://{domain}{url}{query_term if query_term else ''}"
