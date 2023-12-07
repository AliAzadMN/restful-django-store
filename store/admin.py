from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from .models import Address, Category, Comment, Customer, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    ordering = ['user__last_name',]
    search_fields = ['user__last_name__istartswith',]
    list_select_related = ['user', ]

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
    list_display = ['id', 'name', 'category', 'inventory', 'price', 'status_inventory', 'num_of_comments', ]
    list_editable = ['price', ]
    list_filter = ["datetime_created", InventoryFilter, ]
    actions = ['clear_inventory', ]
    search_fields = ['name', ]
    prepopulated_fields = {
        'slug': ['name', ]
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments').annotate(comments_count=Count('comments'))

    def status_inventory(self, product):
        if product.inventory < 10:
            return "Low"
        if product.inventory > 50:
            return "High"
        return "Medium"
    
    @admin.display(ordering="comments_count", description="# comments")
    def num_of_comments(self, product):
        url = reverse("admin:store_comment_changelist") + "?" + urlencode({"product__id": product.id})
        return format_html("<a href={}>{}</a>", url, product.comments_count)

    @admin.action(description="Clear inventory to zero")
    def clear_inventory(self, request, queryset):
        update_counts = queryset.update(inventory=0)
        self.message_user(request, f"{update_counts} of products inventories cleared to zero")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'status', ]
    list_editable = ['status', ]
    list_per_page = 50
    autocomplete_fields = ['product', ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'province', 'city', ]
