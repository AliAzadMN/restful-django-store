from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.IntegerField(source='products.count')

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'description', 'num_of_products', ]
