from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartItemViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
