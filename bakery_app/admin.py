from django.contrib import admin
from .models import BakeryProduct, Order, CustomBakeryOrder

# Register BakeryProduct model
admin.site.register(BakeryProduct)

# Register Order model
admin.site.register(Order)

admin.site.register(CustomBakeryOrder)
