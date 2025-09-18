from rest_framework import viewsets, permissions
from .models import Product, CartItem,Category
from .serializers import ProductSerializer, CartItemSerializer,CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.none() 
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset
    

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]



class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.none() 
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_cart(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = self.get_serializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def remove(self, request, pk=None):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response({'message': 'Item removed'})
        except CartItem.DoesNotExist:
            return Response({'message': 'Item not found'}, status=404)