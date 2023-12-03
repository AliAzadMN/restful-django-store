from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]
    ordering = ['user__last_name',]
    search_fields = ['user__last_name__istartswith',]

    def email(self, customer):
        return customer.user.email
        