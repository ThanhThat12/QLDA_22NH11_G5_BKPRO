from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)  # Đặt trường user thành chỉ đọc

admin.site.register(Customer, CustomerAdmin)
# Register your models here.
# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

