from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'description', 'num_of_products', ]

    def validate(self, data):
        if len(data['title']) < 3:
            return serializers.ValidationError("Product title length should be at least 3")
        return data
