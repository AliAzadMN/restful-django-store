from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer, CreateUpdateCategorySerializer
from .permissions import IsAdminOrReadOnly


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
    