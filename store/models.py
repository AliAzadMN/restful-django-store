from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from .validators import validate_phone_number

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    
    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = (
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_phone_number],
        unique=True,
    )
    birth_date = models.DateField(blank=True, null=True)
