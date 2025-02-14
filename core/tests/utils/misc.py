from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

from core.tests.fixtures.constants import DOMAIN, PROTOCOL

fake = Faker()


def create_upload_image_file(filename=None, size=(100, 100), format="JPEG"):
    image = Image.new("RGB", size, color=(255, 0, 0))
    image_file = BytesIO()
    image.save(image_file, format=format)
    image_file.seek(0)
    if not filename:
        filename = f"test_{fake.word()}.jpg"
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


def get_remaining_pages(query_pages, paginator, total_count):
    from math import floor

    max_pages = paginator.max_page_size
    default_pages = paginator.page_size

    per_page_count = min(query_pages, max_pages) if query_pages else default_pages
    return floor(total_count / per_page_count)
