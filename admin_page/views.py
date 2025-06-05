from django.shortcuts import render
from .models import Product, Order,Customer, OrderItem
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
import json
from django.db.models.functions import TruncMonth
from datetime import datetime
from app.models import Order, OrderItem, Product, Customer, Revenue
from app.models import Customer
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginregister')
def dashboard(request):
    recent_orders = Order.objects.select_related(
        'customer',
        'revenue'
    ).prefetch_related(
        'shipping'
    ).filter(complete=1).order_by('-date_order')[:10]

    # Tính tổng doanh thu từ bảng revenue
    total_sales = Order.objects.filter(
        complete=1
    ).aggregate(
        total_amount=Sum('revenue__amount')
    )['total_amount'] or 0

    # Đếm tổng số đơn hàng có trạng thái complete=1
    total_orders = Order.objects.filter(complete=1).count()
    
    total_visitors = Customer.objects.count()
    
     # Lấy dữ liệu sản phẩm cho biểu đồ
    products = Product.objects.all()
    product_labels = [product.name for product in products]
    product_data = [product.price for product in products]

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_visitors': total_visitors,
        'recent_orders': recent_orders,
        'product_labels': json.dumps(product_labels),
        'product_data': json.dumps(product_data),
    }
    # Lấy dữ liệu sản phẩm bán chạy
    best_selling = OrderItem.objects.values('product__name')\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')[:5]
    
    best_selling_labels = [item['product__name'] for item in best_selling]
    best_selling_data = [item['total_quantity'] for item in best_selling]

    context.update({
        'best_selling_labels': json.dumps(best_selling_labels),
        'best_selling_data': json.dumps(best_selling_data),
    })
    return render(request, 'admin/dashboard/dashboard.html', context)
    return render(request, 'admin/dashboard/dashboard.html', context)
# def user(request):
#     users = User.objects.all()
#     return render(request, 'admin/users/show.html' , {'users': users})

# def order(request):
#     orders = Order.objects.filter(complete=1).prefetch_related('orderitem_set')
#     return render(request, 'admin/orders/show.html', {'orders': orders})
@login_required(login_url='loginregister')
def order(request):
    orders = Order.objects.filter(complete=1)

    # Tìm kiếm theo mã đơn hàng
    order_id = request.GET.get('order_id')
    if order_id:
        orders = orders.filter(id=order_id)

    # Tìm kiếm theo tên khách hàng
    customer_name = request.GET.get('customer_name')
    if customer_name:
        orders = orders.filter(customer__name__icontains=customer_name)

    # Tìm kiếm theo ngày
    order_date = request.GET.get('order_date')
    if order_date:
        date_obj = datetime.strptime(order_date, '%Y-%m-%d')
        orders = orders.filter(date_order__date=date_obj)

    # Tối ưu query
    orders = orders.select_related('customer').prefetch_related('orderitem_set').order_by('-date_order')

    return render(request, 'admin/orders/show.html', {'orders': orders})

# def product(request):
#     products = Product.objects.all()
#     return render(request, 'admin/products/show.html', {'products': products})

# def statistical(request):
#     statistical = Product.objects.all()
#     return render(request, 'admin/statistical/show.html', {'statistical': statistical})

@login_required(login_url='loginregister')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order_detail.html', {'order': order})

@login_required(login_url='loginregister')
def statistical(request):
    # Thống kê doanh thu
    revenue_by_month = Order.objects.filter(complete=1)\
        .annotate(month=TruncMonth('date_order'))\
        .values('month')\
        .annotate(
            total_revenue=Sum('revenue__amount'),
            order_count=Count('id')
        ).order_by('month')

    # Thống kê khách hàng
    top_customers = Order.objects.filter(complete=1)\
        .values('customer__name')\
        .annotate(
            total_spent=Sum('revenue__amount'),
            order_count=Count('id')
        ).order_by('-total_spent')[:5]

    # Thống kê đơn hàng
    order_status = Order.objects.values('complete')\
        .annotate(count=Count('id'))

    orders_by_city = Order.objects.filter(complete=1)\
        .values('shipping__city')\
        .annotate(count=Count('id'))\
        .order_by('-count')[:10]

    # Thống kê sản phẩm
    top_selling_products = OrderItem.objects.values('product__name')\
        .annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('product__price') * F('quantity'))
        ).order_by('-total_quantity')[:10]

    products_by_category = Product.objects.values('category')\
        .annotate(
            product_count=Count('id'),
            total_value=Sum('price')
        )

    context = {
        # Dữ liệu doanh thu
        'revenue_data': json.dumps({
            'labels': [item['month'].strftime("%m/%Y") for item in revenue_by_month],
            'revenue': [float(item['total_revenue']) for item in revenue_by_month],
            'orders': [item['order_count'] for item in revenue_by_month]
        }),

        # Dữ liệu khách hàng
        'customer_data': json.dumps({
            'labels': [item['customer__name'] for item in top_customers],
            'spent': [float(item['total_spent']) for item in top_customers],
            'orders': [item['order_count'] for item in top_customers]
        }),

        # Dữ liệu đơn hàng
        'order_data': json.dumps({
            'status_labels': ['Hoàn thành' if item['complete'] else 'Chưa hoàn thành' 
                            for item in order_status],
            'status_values': [item['count'] for item in order_status],
            'city_labels': [item['shipping__city'] or 'Unknown' for item in orders_by_city],
            'city_values': [item['count'] for item in orders_by_city]
        }),

        # Dữ liệu sản phẩm
        'product_data': json.dumps({
            'top_labels': [item['product__name'] for item in top_selling_products],
            'quantities': [item['total_quantity'] for item in top_selling_products],
            'revenues': [float(item['total_revenue']) if item['total_revenue'] is not None else 0.0 for item in top_selling_products],
            'category_labels': [item['category'] for item in products_by_category],
            'category_counts': [item['product_count'] for item in products_by_category],
            'category_values': [float(item['total_value']) for item in products_by_category]
        })
    }
    
    return render(request, 'admin/statistical/show.html', context)







@login_required(login_url='loginregister')
def user(request):
    customers = Customer.objects.select_related('user').all()
    show_create_form = request.GET.get('action') == 'create'
    edit_customer_id = request.GET.get('edit_id')
    edit_customer = None
    delete_customer_id = request.GET.get('delete_id')
    delete_customer = None
    show_customer_list = True

    if request.method == 'POST':
        if 'create_customer' in request.POST:
            # Tạo user mới trong auth_user với mật khẩu mặc định
            username = request.POST['username']
            email = request.POST['email']
            # Tạo user với mật khẩu mặc định 123456
            user = User.objects.create_user(
                username=username,
                email=email,
                password='123456'
            )
            user.save()

            # Tạo customer và liên kết với user
            role = request.POST.get('role', '0')
            Customer.objects.create(
                user=user,
                name=request.POST['name'],
                email=email,
                phone=request.POST['phone'],
                address=request.POST['address'],
                role=role
            )
            messages.success(request, 'Thêm khách hàng thành công!')
            return redirect('user')

        elif 'update_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id)
            role = request.POST.get('role')
            
            print(f"Updating customer {customer_id} with role: {role}")  # Debug line
            
            customer.name = request.POST['name']
            customer.email = request.POST['email']
            customer.phone = request.POST['phone']
            customer.address = request.POST['address']
            customer.role = role
            
            customer.save()
            messages.success(request, 'Cập nhật khách hàng thành công!')
            return redirect('user')

        elif 'delete_confirm' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id)
            customer.delete()
            messages.success(request, 'Xóa khách hàng thành công!')
            return redirect('user')

    if edit_customer_id:
        edit_customer = get_object_or_404(Customer, id=edit_customer_id)
        show_customer_list = False
    
    if show_create_form:
        show_customer_list = False

    if delete_customer_id:
        delete_customer = get_object_or_404(Customer, id=delete_customer_id)

    context = {
        'customers': customers,
        'show_create_form': show_create_form,
        'edit_customer': edit_customer,
        'delete_customer': delete_customer,
        'show_customer_list': show_customer_list
    }

    return render(request, 'admin/users/show.html', context)

@login_required(login_url='loginregister')
def product(request):
    products = Product.objects.all()
    show_create_form = request.GET.get('action') == 'create'
    edit_product_id = request.GET.get('edit_id')
    delete_product_id = request.GET.get('delete_id')
    edit_product = None
    delete_product = None
    show_product_list = True

    if request.method == 'POST':
        if 'create_product' in request.POST:
            # Xử lý thêm sản phẩm
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            category = request.POST['category']
            image = request.FILES['image']
            
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image
            )
            messages.success(request, 'Thêm sản phẩm thành công!')
            return redirect('product')

        elif 'update_product' in request.POST:
            # Xử lý sửa sản phẩm
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.name = request.POST['name']
            product.description = request.POST['description']
            product.price = request.POST['price']
            product.category = request.POST['category']
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, 'Cập nhật sản phẩm thành công!')
            return redirect('product')

    if edit_product_id:
        edit_product = get_object_or_404(Product, id=edit_product_id)
        show_product_list = False
    
    if show_create_form:
        show_product_list = False  # Ẩn danh sách khi thêm mới

    if delete_product_id:
        delete_product = get_object_or_404(Product, id=delete_product_id)
    
    if request.method == 'POST' and 'delete_confirm' in request.POST:
        product = get_object_or_404(Product, id=request.POST.get('product_id'))
        product.delete()
        messages.success(request, 'Xóa sản phẩm thành công!')
        return redirect('product')
    context = {
        'products': products,
        'show_create_form': show_create_form,
        'edit_product': edit_product,
         'delete_product': delete_product,
        'show_product_list': show_product_list
    }
    return render(request, 'admin/products/show.html', context)

@login_required(login_url='loginregister')
def create_product(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        image = request.FILES['image']

        # Lưu sản phẩm vào database
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )
        messages.success(request, 'Thêm sản phẩm thành công!')
        return redirect('/products')  # Chuyển hướng về trang danh sách sản phẩm

    return render(request, 'admin/products/create.html')

@login_required(login_url='loginregister')
def update_product(request, id):
    # Lấy sản phẩm theo ID
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.category = request.POST['category']

        # Kiểm tra nếu có hình ảnh mới
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        # Lưu thay đổi
        product.save()
        messages.success(request, 'Cập nhật sản phẩm thành công!')
        return redirect('/products')  # Hoặc chuyển hướng đến danh sách sản phẩm

    return render(request, 'admin/products/update.html', {'product': product})

@login_required(login_url='loginregister')
def delete_product(request, id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        product.delete()
        messages.success(request, 'Xóa sản phẩm thành công!')
        return redirect('product')
    return redirect('product')


@login_required(login_url='loginregister')
def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # Tạo user với mật khẩu mặc định 123456
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password='123456'
        )
        user.is_active = True
        user.save()
        messages.success(request, 'Thêm người dùng thành công!')
        return redirect('/users')
    return render(request, 'admin/users/create.html')


@login_required(login_url='loginregister')
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        messages.success(request, 'Cập nhật người dùng thành công!')
        return redirect('/users')
    return render(request, 'admin/users/update.html', {'user': user})


@login_required(login_url='loginregister')
def delete_user(request, id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=id)
        # Delete associated user if exists
        if customer.user:
            customer.user.delete()
        customer.delete()
        messages.success(request, 'Xóa khách hàng thành công!')
        return redirect('user')
    return redirect('user')


from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required(login_url='loginregister')
def admin_logout(request):
    logout(request)
    return redirect('loginregister')  # Chuyển hướng về trang đăng nhập

@login_required(login_url='loginregister')
def profile_view(request):
    return render(request, 'admin/dashboard/profile.html', {
        'user': request.user
    })
