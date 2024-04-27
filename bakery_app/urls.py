from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('create-product/', views.create_product, name='create_product'),
    path('orders/', views.list_orders, name='list_orders'),
    path('place-order/<int:product_id>/', views.place_order, name='place_order'),
    path('user-orders/', views.user_orders, name='user_orders'),
    path('manage-orders/', views.manage_orders, name='manage_orders'), 
    path('custom-order/', views.custom_order, name='custom_order'), 
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    path('all-orders/', views.all_orders, name='all_orders'),  # View for total orders
    path('pending-orders/', views.pending_orders, name='pending_orders'),  # View for pending orders
    path('all-products/', views.all_products, name='all_products'),  # View for total products
    path('custom-orders/', views.custom_orders, name='custom_orders'),  # View for custom orders
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),  # URL pattern for updating product
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),  # URL pattern for deleting product
]
