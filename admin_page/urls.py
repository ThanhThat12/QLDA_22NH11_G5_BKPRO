from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product, name='product'),
    path('users/', views.user, name='user'),
    path('orders/', views.order, name='order'),
    path('statistical/', views.statistical, name='statistical'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),


    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:id>/update/', views.update_product, name='update_product'),
    path('products/<int:id>/delete/', views.delete_product, name='delete_product'),  # Xóa sản phẩm

    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:id>/update/', views.update_user, name='update_user'),
    path('users/<int:id>/delete/', views.delete_user, name='delete_user'),


    path('logout/', views.admin_logout, name='admin_logout'),
    path('profile/', views.profile_view, name='profile'),
]
