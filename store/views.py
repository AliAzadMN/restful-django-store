from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .paginations import DefaultPagination
from .filters import ProductFilter
from .serializers import (
    CategorySerializer,
    CreateUpdateCategorySerializer,
    ProductSerializer,
    CreateUpdateProductSerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related("products")
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, pk):
        category = self.get_object()
        if category.products.count() > 0:
            return Response(
                data={"error": "There is some products relating this category. Please remove them first"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return CreateUpdateCategorySerializer
        return CategorySerializer
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category")
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', ]
    filterset_class = ProductFilter
    ordering_fields = ['id', 'inventory', ]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return CreateUpdateProductSerializer
        return ProductSerializer

    def destroy(self, request, pk):
        product = self.get_object()
        if product.order_items.count() > 0:
            return Response(
                data={"Error": "There is some order items including that product. Please remove them first"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
