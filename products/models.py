from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.CharField(max_length=100)
    stock_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    image_url = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)   
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null= False, blank=False)
    updated = models.DateTimeField(auto_now=True)

    def reduce_stock_quantity(self, quantity):
        self.stock_quantity -= quantity
        self.save()

    def __str__(self):
        return self.name 

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlisted_by')

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()