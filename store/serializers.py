from rest_framework import serializers

from django.utils.text import slugify

from . import models


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.IntegerField(source='products.count')

    class Meta:
        model = models.Category
        fields = ['id', 'title', 'description', 'num_of_products', ]


class CreateUpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'description', ]

    def validate(self, data):
        title = data.get('title')
        if title and len(title) < 3:
            return serializers.ValidationError("Product title length should be at least 3")
        return data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title')

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'category', 'inventory', 'price', 'description', ]


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['name', 'category', 'description', 'price', 'inventory', ]
    
    def create(self, validated_data):
        product = models.Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    
    def update(self, instance, validated_data):
        for field in CreateUpdateProductSerializer.Meta.fields:
            setattr(
                instance,
                field,
                validated_data.get(field, getattr(instance, field))
            )
        instance.slug = slugify(instance.name)
        instance.save()
        return instance
