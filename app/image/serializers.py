"""
Serializers for the user API View.
"""
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from core.models import (
    Image,
    Item,
    Camera,
    ProductionLine,
)


class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'index']
        read_only_fields = ['id']


class ProductionLineSerializer(serializers.ModelSerializer):
    """Serializer for product line"""

    class Meta:
        model = ProductionLine
        fields = ['id', 'name', 'product']
        read_only_fields = ['id']
        extra_kwargs = {'name': {'required': True}}

    def create(self, validated_data):
        # Perform any custom actions or transformations with the data
        auth_user = self.context['request'].user
   
        # Create the Item object
        production_line = self.Meta.model.objects.create(
            user=auth_user,
            **validated_data)
        return production_line


class CameraSerializers(serializers.ModelSerializer):
    """Serializer for creting camera"""
    production_line = ProductionLineSerializer(many=False)

    class Meta:
        model = Camera
        fields = ['id', 'production_line', 'IP']
        read_only_fields = ['id']
        extra_kwargs = {
            'user': {'required': True},
            'production_line': {'required': True},
            'IP': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
        }


class CameraDetailSerializer(CameraSerializers):
    """Srializer for camera detail view."""

    class Meta(CameraSerializers.Meta):
        fields = CameraSerializers.Meta.fields + ['username', 'password']
        CameraSerializers.Meta.extra_kwargs['username'] = {'required': True}
        CameraSerializers.Meta.extra_kwargs['password'] = {'required': True}

    def _get_or_create_production_line(self, production_line_data):
        """
        Helper method to get or create a production line based on the provided data.
        """
        auth_user = self.context['request'].user
        production_line, created = ProductionLine.objects.get_or_create(
            user=auth_user,
            name=production_line_data.get('name'),
            defaults={**production_line_data}  # Add any additional fields necessary
        )
        return production_line

    def create(self,validated_data):
        auth_user = self.context['request'].user  # Get the user making the request

        # Extract production_line data from validated_data
        production_line_data = validated_data.pop('production_line', None)

        # Get or create the production line
        production_line = self._get_or_create_production_line(production_line_data)

        # Now that the production line is handled, create the camera instance
        camera = Camera.objects.create(
            user=auth_user,
            production_line=production_line,
            **validated_data
        )

        return camera

class ImageSerializer(serializers.ModelSerializer):
    """Serializer for image"""
    item = ItemSerializer(many=False)

    class Meta:
        model = Image
        fields = ['id', 'item', 'grade', 'capture_time']
        read_only_fields = ['id']
    

class ImageDetailSerializer(ImageSerializer):
    """Serializer for Image detail view."""
    camera = CameraSerializers(many=False)

    class Meta(ImageSerializer.Meta):
        fields = ImageSerializer.Meta.fields + \
            ['camera', 'created_at',  'image']

    def _get_or_create_item(self, item_data):
        """
        Helper method to get or create a production line based on the provided data.
        """
        auth_user = self.context['request'].user
        item, created = ProductionLine.objects.get_or_create(
            user=auth_user,
            index = item_data.get('index'),
            defaults={**item_data}  # Add any additional fields necessary
        )
        return item
    
    def _get_camera_by_ip(self, ip_address):
        """
        Helper method to fetch a camera based on its IP address.
        Raise a NotFound error if the camera does not exist.
        """
        try:
            return Camera.objects.get(IP=ip_address)
        except Camera.DoesNotExist:
            raise PermissionDenied(detail="Camera with the specified IP address not found.")


    def create(self, validated_data):
        """Create an Image and link it to the appropriate item and camera."""

        # auth_user = self.context['request'].user  # Get the user making the request

        # Extract item data from validated_data
        item_data = validated_data.pop('item', None)
        # Get or create the item
        item = self._get_or_create_item(item_data)

        # Extract camera data and fetch the camera by IP
        camera_data = validated_data.pop('camera', None)
        if camera_data is None:
            raise PermissionDenied(detail="Camera information is required.")

        # Get camera by IP and raise an error if it doesn't exist
        camera = self._get_camera_by_ip(camera_data.get('IP'))

        # Create the image object with the item and camera
        image = Image.objects.create(
            item=item,
            camera=camera,  # Associate the image with the fetched camera
            **validated_data
        )

        return image
