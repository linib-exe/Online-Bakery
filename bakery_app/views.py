from django.shortcuts import render, get_object_or_404, redirect
from .models import BakeryProduct, Order,CustomBakeryOrder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomOrderForm,ProductForm


def home(request):
    # Retrieve paginated products for the main section
    products = BakeryProduct.objects.all()
    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generate recommended products (example uses random recommendation)
    recommended_products = BakeryProduct.objects.order_by('?')[:3]  # Random 3 products

    return render(request, 'home.html', {'page_obj': page_obj, 'recommended_products': recommended_products})
# Admin view to create a new bakery product
@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')

        product = BakeryProduct.objects.create(
            name=name,
            description=description,
            price=price,
            image=image
        )

        messages.success(request, 'Product created successfully.')
        return redirect('home')

    return render(request, 'create_product.html')

# Admin view to list all orders
@login_required
def list_orders(request):
    orders = Order.objects.all()
    paginator = Paginator(orders, 6)  # Pagination to display 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_orders.html', {'page_obj': page_obj})

# User view to place an order
@login_required
def place_order(request, product_id):
    product = get_object_or_404(BakeryProduct, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        total_price = quantity * product.price

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            payment_status='pending',
            delivery_status='pending'
        )

        messages.success(request, 'Order placed successfully.')
        return redirect('user_orders')

    return render(request, 'place_order.html', {'product': product})

# User view to see their orders
@login_required
def user_orders(request):
    # Retrieve standard orders for the logged-in user
    standard_orders = Order.objects.filter(user=request.user)

    # Retrieve custom bakery orders for the logged-in user
    custom_orders = CustomBakeryOrder.objects.filter(user=request.user)

    # Combine both standard and custom orders for pagination
    combined_orders = list(standard_orders) + list(custom_orders)

    paginator = Paginator(combined_orders, 10)  # Pagination for 10 orders per page
    page_number = request.GET.get('page')  # Get the current page
    page_obj = paginator.get_page(page_number)  # Get the relevant page object

    return render(request, 'user_orders.html', {'page_obj': page_obj})  # Pass orders to the template

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after signup
            login(request, user)
            messages.success(request, 'Signup successful!')
            return redirect('home')  # Redirect to home after signup
    else:
        form = UserCreationForm()  # Create an empty form for GET requests

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to home after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('home') 

def is_admin(user):
    return user.is_staff  # Change this as needed to suit your admin check

# View to list all orders and allow admin to change payment and delivery status
@user_passes_test(is_admin)  # Ensure only admin users can access this view
def manage_orders(request):
    if request.method == 'POST':
        # Get the order ID from the form and update the statuses
        order_id = request.POST.get('order_id')
        payment_status = request.POST.get('payment_status')
        delivery_status = request.POST.get('delivery_status')

        # Determine if it's a standard order or a custom order
        if Order.objects.filter(id=order_id).exists():
            order = get_object_or_404(Order, id=order_id)
        else:
            order = get_object_or_404(CustomBakeryOrder, id=order_id)

        order.payment_status = payment_status
        order.delivery_status = delivery_status
        order.save()

        messages.success(request, 'Order updated successfully.')

    # Combine standard orders and custom orders
    combined_orders = list(Order.objects.all()) + list(CustomBakeryOrder.objects.all())  # Combine both types of orders
    paginator = Paginator(combined_orders, 5)  # Pagination for 10 orders per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the relevant page object

    return render(request, 'manage_orders.html', {'page_obj': page_obj})  # Render the "Manage Orders" template

# @user_passes_test(is_admin)  # Restrict to admin users
# def admin_dashboard(request):
#     # Data for the dashboard
#     total_orders = Order.objects.count()  # Total number of orders
#     total_products = BakeryProduct.objects.count()  # Total number of products
#     pending_orders = Order.objects.filter(payment_status='pending').count()  # Count of pending orders
#     recent_orders = Order.objects.order_by('-order_date')[:5]  # Most recent 5 orders

#     context = {
#         'total_orders': total_orders,
#         'total_products': total_products,
#         'pending_orders': pending_orders,
#         'recent_orders': recent_orders,
#     }

#     return render(request, 'admin_dashboard.html', context)  # Render the dashboard template
@user_passes_test(is_admin)  # Restrict to admin users
def admin_dashboard(request):
    # Calculate key statistics
    total_standard_orders = Order.objects.count()  # Total number of standard orders
    total_custom_orders = CustomBakeryOrder.objects.count()  # Total custom bakery orders
    total_orders = total_standard_orders + total_custom_orders  # Sum of both types of orders
    pending_orders = Order.objects.filter(payment_status='pending').count()  # Pending standard orders
    total_products = BakeryProduct.objects.count()  # Total number of products

    # Retrieve recent orders
    recent_standard_orders = Order.objects.order_by('-order_date')[:5]  # Most recent 5 standard orders
    recent_custom_orders = CustomBakeryOrder.objects.order_by('-order_date')[:5]  # Most recent 5 custom orders
    combined_recent_orders = list(recent_standard_orders) + list(recent_custom_orders)  # Combine recent orders

    # Apply pagination to recent orders
    paginator = Paginator(combined_recent_orders, 3)  # Display 3 recent orders per page
    page_number = request.GET.get('page')  # Get the current page number
    recent_orders_page = paginator.get_page(page_number)  # Get the relevant page object

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_products': total_products,
        'total_custom_orders': total_custom_orders,
        'recent_orders_page': recent_orders_page,  # Paginated recent orders
    }

    return render(request, 'admin_dashboard.html', context)  # Render the dashboard template

@user_passes_test(is_admin)
def all_orders(request):
    # Combine standard and custom orders
    all_orders = list(Order.objects.all()) + list(CustomBakeryOrder.objects.all())
    paginator = Paginator(all_orders, 3)  # Pagination for 10 orders per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the relevant page object

    return render(request, 'all_orders.html', {'page_obj': page_obj})

# View to display pending orders
@user_passes_test(is_admin)
def pending_orders(request):
    # Get pending standard orders
    pending_orders = Order.objects.filter(payment_status='pending')
    paginator = Paginator(pending_orders, 3)  # Pagination for 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pending_orders.html', {'page_obj': page_obj})

# View to display all products
@user_passes_test(is_admin)
def all_products(request):
    # Get all products
    products = BakeryProduct.objects.all()
    paginator = Paginator(products, 3)  # Pagination for 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_products.html', {'page_obj': page_obj})



# @login_required
# def custom_order(request):
#     if request.method == 'POST':
#         form = CustomOrderForm(request.POST)
#         if form.is_valid():
#             custom_order = form.save(commit=False)
#             custom_order.user = request.user  # Assign the current user to the order
            
#             # Calculate price based on various factors
#             base_price = 20  # Base price for a custom order
#             weight_price = custom_order.weight * 0.02  # Price based on weight (e.g., 2 cents per gram)
            
#             # Flavor-based pricing (example: chocolate is slightly more expensive)
#             flavor_price = 0
#             if custom_order.flavor == 'chocolate':
#                 flavor_price = 5  # Chocolate costs an additional 5 units

#             # Shape-based pricing (example: heart shape costs more due to complexity)
#             shape_price = 0
#             if custom_order.shape == 'heart':
#                 shape_price = 10  # Heart shape adds an additional cost

#             # Calculate the total price
#             total_price = base_price + weight_price + flavor_price + shape_price
#             custom_order.price = total_price  # Set the calculated price

#             custom_order.save()  # Save the custom order
#             messages.success(request, f'Custom order placed! Total price: ${total_price:.2f}')  # Display success message
#             return redirect('user_orders')  # Redirect to the user's orders page
#     else:
#         form = CustomOrderForm()  # Create an empty form for GET requests

#     return render(request, 'custom_order.html', {'form': form})

@login_required
def custom_order(request):
    if request.method == 'POST':
        form = CustomOrderForm(request.POST)  # Get form data
        if form.is_valid():
            custom_order = form.save(commit=False)
            custom_order.user = request.user  # Assign the current user
            
            # Calculate price based on various factors
            base_price = 20  # Base price for a custom order
            weight_price = custom_order.weight * 0.02  # Price based on weight
            flavor_price = 0
            if custom_order.flavor == 'chocolate':
                flavor_price = 5  # Additional cost for chocolate flavor
            shape_price = 0
            if custom_order.shape == 'heart':
                shape_price = 10  # Additional cost for heart shape

            # Calculate the total price
            total_price = base_price + weight_price + flavor_price + shape_price
            custom_order.total_price = total_price  # Set the calculated price
            
            custom_order.save()  # Save the custom order
            messages.success(request, f'Custom order placed! Total price: ${total_price:.2f}')  # Success message
            return redirect('user_orders')  # Redirect to the user's orders page
    else:
        form = CustomOrderForm()  # Create an empty form for GET requests

    return render(request, 'custom_order.html', {'form': form})

# @user_passes_test(is_admin)
# def custom_orders(request):
#     # Get all custom bakery orders
#     custom_orders = CustomBakeryOrder.objects.all()
#     paginator = Paginator(custom_orders, 10)  # Pagination for 10 orders per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'custom_orders.html', {'page_obj': page_obj})

@user_passes_test(is_admin)  # Ensure only admin users can access this view
def custom_orders(request):
    # Get all custom bakery orders
    custom_orders = CustomBakeryOrder.objects.all()
    paginator = Paginator(custom_orders, 10)  # Pagination for 10 orders per page
    page_number = request.GET.get('page')  # Get the current page
    page_obj = paginator.get_page(page_number)  # Get the correct page object

    return render(request, 'custom_orders.html', {'page_obj': page_obj})  # Render the custom orders page

@user_passes_test(is_admin)  # Restrict access to admin users
def update_product(request, product_id):
    product = get_object_or_404(BakeryProduct, id=product_id)  # Get the product to update
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Update form with existing product
        if form.is_valid():
            form.save()  # Save the updated product
            messages.success(request, 'Product updated successfully.')
            return redirect('all_products')  # Redirect to the product list
    else:
        form = ProductForm(instance=product)  # Populate the form with existing product data

    return render(request, 'update_product.html', {'form': form, 'product': product})  # Render the update product template

@user_passes_test(is_admin)  # Restrict access to admin users
def delete_product(request, product_id):
    product = get_object_or_404(BakeryProduct, id=product_id)  # Get the product to delete
    if request.method == 'POST':  # Confirmation of deletion
        product.delete()  # Delete the product
        messages.success(request, 'Product deleted successfully.')
        return redirect('all_products')  # Redirect to the product list

    return render(request, 'delete_product.html', {'product': product})  # Render the delete product template
