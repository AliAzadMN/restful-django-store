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
    

class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_10 = "<10"
    BETWEEN_10_AND_50 = "10<=50"
    MORE_THAN_50 = ">50"

    title = "Inventory Status"
    parameter_name = "inventory"

    # Define the lookup method to return filter options for the admin interface
    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_10, 'Low'),
            (InventoryFilter.BETWEEN_10_AND_50, 'Medium'),
            (InventoryFilter.MORE_THAN_50, 'High'),
        ]
    
    # Define the queryset method for Data Filtering based on the selected option
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_10:
            return queryset.filter(inventory__lt=10)
        if self.value() == InventoryFilter.BETWEEN_10_AND_50:
            return queryset.filter(inventory__range=(10, 50))
        if self.value() == InventoryFilter.MORE_THAN_50:
            return queryset.filter(inventory__gt=50)  


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'inventory', 'price', 'status_inventory', ]
    list_editable = ['price', ]
    list_filter = ["datetime_created", InventoryFilter, ]

    def status_inventory(self, product):
        if product.inventory < 10:
            return "Low"
        if product.inventory > 50:
            return "High"
        return "Medium"
