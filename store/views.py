from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Comment, Product
from .permissions import IsAdminOrReadOnly
from .paginations import DefaultPagination
from .filters import ProductFilter
from .serializers import (
    CategorySerializer,
    AdminCommentSerializer,
    CreateCommentSerializer,
    UpdateCommentSerializer,
    UserCommentSerializer,
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


class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        queryset = Comment.objects.select_related('user').filter(product_id=product_pk)
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(status=Comment.COMMENT_STATUS_APPROVED)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return list()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        if self.request.method == 'PATCH':
            return UpdateCommentSerializer
        if self.request.user.is_staff:
            return AdminCommentSerializer
        return UserCommentSerializer
    
    def get_serializer_context(self):
        return {
            "request": self.request, 
            "product_pk": self.kwargs['product_pk'],
        }
