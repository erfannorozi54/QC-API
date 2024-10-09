"""
Serializers for the user API View.
"""
from rest_framework import serializers

from core.models import (
    Image,
    Item,
    Camera,
    ProductionLine,
)


class ItemSerializer(serializers.ModelSerializer):
    model = Item


class ProductionLineSerializer(serializers.ModelSerializer):
    """Serializer for product line"""

    class Meta:
        model = ProductionLine
        fields = ['id', 'name', 'product']
        read_only_fields = ['id']
        extra_kwargs = {'name': {'require': True}}


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


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for image"""
    item = ItemSerializer(many=False)

    class Meta:
        model = Image
        fields = ['id', 'item', 'grade', 'capure_time']
        read_only_fields = ['id']
    

class ImageDetailSerializer(ImageSerializer):
    """Serializer for Image detail view."""
    camera = CameraSerializers(many=False)

    class Meta(ImageSerializer.Meta):
        fields = ImageSerializer.Meta.fields + \
            ['camera', 'created_at',  'image']

    def create(self, validated_data):
        """Create a Image."""
        item = validated_data.pop('item', None)
        camera = Camera.objects.create(**validated_data)
        if item is None:
            raise serializers.ValidationError(
                {'production_line':
                'Invalid production line name.'}
            )
        item_obj, created = Item.objects.get_or_create(index=item)
        camera.item.add(item_obj)

