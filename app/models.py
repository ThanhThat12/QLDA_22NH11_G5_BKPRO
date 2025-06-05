# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import re

class Customer(models.Model):
    ROLE_CHOICES = [
        (0, 'Customer'),
        (1, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)  # Mặc định là Customer

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
    ]

    name = models.CharField(max_length=255, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  # Thêm lựa chọn cho category
    description = models.TextField(default="No description")  # Thêm default để tránh lỗi migrate
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Product"
    
    @property
    def first_sentence(self):
        """Lấy câu đầu tiên từ mô tả."""
        match = re.search(r'[^.]*\.', self.description)
        return match.group(0) if match else self.description
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url  
    
    
          
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)    
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=100,null=True)
    shipping_cost = models.FloatField(default=0.0) 

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([
        (item.product.price * item.quantity) 
        for item in orderitems 
        if item.product is not None
    ])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_final_total(self):
        return self.get_cart_total + self.shipping_cost
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)    
    @property # Tính tổng tiền của sản phẩm
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipping')
    address = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=100,null=True)
    mobile = models.CharField(max_length=10,null=True)
    date_added = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.address

class Revenue(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()  # Số tiền chỉ tính giá trị món hàng (không bao gồm phí ship)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revenue for Order {self.order.id} - ${self.amount}"

