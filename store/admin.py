from django.contrib import admin
from django.db.models import Count

from .models import Category, Customer, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    ordering = ['user__last_name',]
    search_fields = ['user__last_name__istartswith',]

    def email(self, customer):
        return customer.user.email


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'num_of_products', 'top_product', ]
    search_fields = ['title__istartswith', ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products').annotate(products_count=Count('products'))
    
    @admin.display(ordering="products_count")
    def num_of_products(self, category):
        return category.products_count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'price', 'status_inventory', ]
    list_editable = ['price', ]

    def status_inventory(self, product):
        if product.inventory < 10:
            return "Low"
        if product.inventory > 50:
            return "High"
        return "Medium"
