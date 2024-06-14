from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ShelfViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'shelves', ShelfViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



