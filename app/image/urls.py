"""
URL mappings for the recipe app
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from image import views


router = DefaultRouter()
router.register('image', views.ImageViewSet)
router.register('production_line', views.ProductionLineViewSet)
router.register('camera', views.CameraViewSet)
router.register('item', views.ItemViewSet)

app_name = 'image'

urlpatterns = [
    path('', include(router.urls))
]
