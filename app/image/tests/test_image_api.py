"""
Tests for image APIs.
"""
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from core.models import (
    Image,
    Camera,
    ProductionLine,
    Item,
)

from PIL import Image

import io

from image.serializers import (
    ImageSerializer,
    ImageDetailSerializer,
)

IMAGES_URL = reverse('image:image-list')


def create_image_with_color(color):
    """
    Creates a 300x200 image with the specified RGB color and returns the image as a JPG file in memory.
    
    Args:
        color (tuple): A tuple of three integers representing the RGB color, e.g., (255, 0, 0) for red.
    
    Returns:
        io.BytesIO: The JPG image in memory.
    """
    # Create a new image with the specified color
    image = Image.new('RGB', (300, 200), color)
    
    # Save the image to a BytesIO object
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    
    # Move the cursor to the start of the BytesIO object
    img_bytes.seek(0)
    
    # Return the image as a file-like object
    return img_bytes


def detail_url(image_id):
    """Create and return a image detail URL."""
    return reverse('image:image-detail', args=[image_id])

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicImageAPITest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(IMAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateImageAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='userpassword'
        )
        self.client.force_login(self.user)

    def test_retrieve_images(self):
        """Test retrieving a list of images."""
        pass