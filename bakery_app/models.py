from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Bakery Product model
class BakeryProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(BakeryProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    delivery_status = models.CharField(max_length=10, choices=[('shipped', 'Shipped'), ('pending', 'Pending')], default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class CustomBakeryOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who placed the order
    weight = models.FloatField()  # Weight in grams
    flavor = models.CharField(max_length=50)  # Flavor of the bakery item
    shape = models.CharField(max_length=50)  # Shape of the bakery item
    order_date = models.DateTimeField(auto_now_add=True)  # When the order was placed
    delivery_date = models.DateField(null=True, blank=True)  # Optional delivery date
    payment_status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    delivery_status = models.CharField(max_length=10, choices=[('shipped', 'Shipped'), ('pending', 'Pending')], default='pending')
    total_price = models.DecimalField(max_digits=6, decimal_places=2)  # Total price
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.flavor} {self.shape} - {self.weight}g"

