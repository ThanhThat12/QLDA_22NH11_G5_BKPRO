from django.urls import path
from . import views
from .views import chatbot
urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('update_item_detail/', views.updateitemdetail, name='update_item_detail'),
    path('detail/', views.detail, name='detail'),
    path('loginregister/', views.loginregisterPage, name='loginregister'),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.account, name='account'),
    path('get_cart_count/', views.get_cart_count, name="get_cart_count"),  # API lấy số lượng giỏ hàng
    path('get_cart_total/', views.get_cart_totalPrice, name="get_cart_total"),  # API lấy tổng tiền giỏ hàng
    path('search/', views.search, name='search'),  # Tìm kiếm sản phẩm
    path('get_item_quantity/', views.get_item_quantity, name='get_item_quantity'),  # API lấy số lượng sản phẩm
    path('success/', views.success_page, name='success_page'),
    path('update_personal_info/', views.update_personal_info, name='update_personal_info'),  # Cập nhật thông tin cá nhân
    path('update_password/', views.update_password, name='update_password'),  # Cập nhật mật khẩu
    path('order_detail_api/<int:order_id>/', views.order_detail_api, name='order_detail_api'),
    path('reorder/<int:order_id>/', views.reorder_order, name='reorder_order'),
    path('shop/', views.shop, name='shop'),
    path('ajax_shop/', views.ajax_shop, name='ajax_shop'),
    path('contact/', views.contact, name='contact'),
    
    path('chatbot/', chatbot, name='chatbot'),
]
