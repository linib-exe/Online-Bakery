from django import forms
from .models import CustomBakeryOrder,BakeryProduct

# Form for custom bakery orders
class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomBakeryOrder  # Link to the CustomBakeryOrder model
        fields = ['weight', 'flavor', 'shape']  # Fields to capture user input

    # Options for weight, flavor, and shape
    WEIGHT_CHOICES = [
        (500, '500g'),
        (1000, '1kg'),
        (1500, '1.5kg'),
    ]

    FLAVOR_CHOICES = [
        ('vanilla', 'Vanilla'),
        ('chocolate', 'Chocolate'),
        ('strawberry', 'Strawberry'),
    ]

    SHAPE_CHOICES = [
        ('round', 'Round'),
        ('square', 'Square'),
        ('heart', 'Heart'),
    ]

    # Define the fields with specific choices
    weight = forms.ChoiceField(choices=WEIGHT_CHOICES, label="Weight")  # Dropdown for weight
    flavor = forms.ChoiceField(choices=FLAVOR_CHOICES, label="Flavor")  # Dropdown for flavor
    shape = forms.ChoiceField(choices=SHAPE_CHOICES, label="Shape")  # Dropdown for shape

class ProductForm(forms.ModelForm):
    class Meta:
        model = BakeryProduct  # Connect the form to the BakeryProduct model
        fields = ['name', 'description', 'price', 'image']  # Fields to include in the form
