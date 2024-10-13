"""
Views for the recipe APIs.
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Image,
    ProductionLine,
    Item,
    Camera,
)
from image.authentication import ConstantTokenAuthentication
# from image.permissions import ConstantTokenPermission

from image import serializers


class ImageViewSet(viewsets.ModelViewSet):
    """View for manage image APIs."""
    serializer_class = serializers.ImageDetailSerializer
    authentication_classes = [ConstantTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.ImageSerializer
        else:
            return self.serializer_class


class CameraViewSet(viewsets.ModelViewSet):
    """View for manage camera APIS."""
    serializer_class = serializers.CameraDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Camera.objects.all()


    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == 'list':
            return serializers.CameraSerializers
        else:
            return self.serializer_class


class ProductionLineViewSet(viewsets.ModelViewSet):
    """View for manage production line APIS."""
    serializer_class = serializers.ProductionLineSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProductionLine.objects.all()



class ItemViewSet(viewsets.ModelViewSet):
    """View for manage item APIS."""
    serializer_class = serializers.ItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
