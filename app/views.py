from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth import logout
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def contact(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Ở đây bạn có thể xử lý dữ liệu, ví dụ: gửi email, lưu vào database, v.v.
        # Ví dụ: In dữ liệu ra console (thay thế bằng logic của bạn)
        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Chuyển hướng sau khi gửi form thành công
        return HttpResponseRedirect(reverse('contact'))  # Chuyển về chính trang Contact

    return render(request, 'app/contact.html')

# def shop(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         cartItems = order.get_cart_items
#     else:
#         order = {'get_cart_total': 0, 'get_cart_items': 0}
#         cartItems = order['get_cart_items']

#     # Lấy tham số category từ URL
#     category = request.GET.get('category')

#     # Truy xuất sản phẩm
#     products = Product.objects.all()

#     # Lọc sản phẩm theo danh mục nếu có
#     if category and category in ['vegetable', 'fruit']:
#         products = products.filter(category=category)
#     else:
#         category = None

#     # Truy vấn số lượng sản phẩm theo từng loại
#     fruits_count = Product.objects.filter(category='fruit').count()
#     vegetables_count = Product.objects.filter(category='vegetable').count()

#     # Phân trang: 6 sản phẩm mỗi trang
#     paginator = Paginator(products, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'fruits_count': fruits_count,
#         'vegetables_count': vegetables_count,
#         'category': category,
#         'cartItems': cartItems,
#     }

#     return render(request, 'app/shop.html', context)

def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    # Get category parameter from URL
    category = request.GET.get('category')

    # Query products
    products = Product.objects.all()

    # Filter by category if provided
    if category and category in ['vegetable', 'fruit']:
        products = products.filter(category=category)
    else:
        category = None

    # Count products by category
    fruits_count = Product.objects.filter(category='fruit').count()
    vegetables_count = Product.objects.filter(category='vegetable').count()

    # Pagination: 6 products per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'fruits_count': fruits_count,
        'vegetables_count': vegetables_count,
        'category': category,
        'cartItems': cartItems,
    }

    return render(request, 'app/shop.html', context)

def ajax_shop(request):
    # Get category and page from AJAX request
    category = request.GET.get('category')
    page_number = request.GET.get('page', 1)

    # Query products
    products = Product.objects.all()

    # Filter by category if provided
    if category and category in ['vegetable', 'fruit']:
        products = products.filter(category=category)

    # Pagination
    paginator = Paginator(products, 6)
    page_obj = paginator.get_page(page_number)

    # Render HTML for products and pagination
    product_html = render_to_string('app/partials/shop_product_list.html', {'page_obj': page_obj})
    pagination_html = render_to_string('app/partials/shop_pagination.html', {
        'page_obj': page_obj,
        'category': category
    })

    return JsonResponse({
        'product_html': product_html,
        'pagination_html': pagination_html,
    })
    
    
def detail(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}   
        cartItems = order['get_cart_items']
    
    product_id = request.GET.get('id')
    if not product_id:
        return JsonResponse({'error': 'Product ID is required'}, status=400)
    product = get_object_or_404(Product, id=product_id)

    # **Lấy danh sách sản phẩm liên quan cùng category, loại trừ sản phẩm hiện tại**
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]  


    context = {
        'product': product,
        'cartItems': cartItems,
        'related_products': related_products
    } 
    return render(request, 'app/detail.html',context)

# def home(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0}   
#         cartItems = order['get_cart_items']
#     products = Product.objects.all()
#     context = {
#         'products': products,
#         'cartItems': cartItems
#     }   
#     return render(request, 'app/home.html',context)

def loginregisterPage(request):
    form = RegisterForm()
    login_error = ""
    login_username = ""
    is_register_failed = False
    is_register_submit = False

    if request.method == 'POST':
        # Đăng nhập
        if 'login' in request.POST:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            login_username = username

            if not username or not password:
                login_error = "Vui lòng nhập đầy đủ tài khoản và mật khẩu."
            elif not User.objects.filter(username=username).exists():
                login_error = "Tài khoản chưa được đăng ký."
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    # Kiểm tra vai trò của người dùng
                    try:
                        customer = Customer.objects.get(user=user)
                        if customer.role == 1:  # Admin
                            return redirect('dashboard')  # Chuyển hướng đến trang dashboard
                        else:  # Customer
                            return redirect('home')  # Chuyển hướng đến trang chủ
                    except Customer.DoesNotExist:
                        # Nếu không có bản ghi Customer, mặc định chuyển hướng đến trang chủ
                        return redirect('home')
                else:
                    login_error = "Mật khẩu không đúng!"

        # Đăng ký
        elif 'register' in request.POST:
            is_register_submit = True
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Bạn đã đăng ký thành công! Vui lòng đăng nhập.")
                return redirect('loginregister')
            else:
                is_register_failed = True
                messages.error(request, "Thông tin đăng ký không hợp lệ. Vui lòng kiểm tra lại.")

    return render(request, 'app/loginregister.html', {
        'form': form,
        'login_error': login_error,
        'login_username': login_username,
        'register_failed': is_register_failed,
        'is_register_submit': is_register_submit,
        'is_login_submit': 'login' in request.POST,
        'is_reload': not request.POST,
    })


def logoutUser(request):
    logout(request)
    return redirect("home")

@login_required
def account(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        cartItems = order.get_cart_items

         # Lấy các đơn hàng đã hoàn tất
        completed_orders = Order.objects.filter(customer=customer, complete=True).order_by('-date_order')

    context = {
        'cartItems': cartItems,
        'customer': customer,
        'completed_orders': completed_orders,
        
    }
    return render(request, "app/account.html", context)



#@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}   
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
        
    }         
    return render(request, 'app/cart.html',context)

# def checkout(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         items = []
#         order = {'get_cart_total':0, 'get_cart_items':0}   
#         cartItems = order['get_cart_items']
#     context = {
#         'items': items,
#         'order': order,
#         'cartItems': cartItems,

#     }         
#     return render(request, 'app/checkout.html',context)


from django.core.mail import send_mail
from django.conf import settings
from .forms import BillingForm


# def checkout(request):
#     if not request.user.is_authenticated:
#         return redirect('loginregister')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập

#     customer = request.user.customer
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     items = order.orderitem_set.all()
#     cartItems = order.get_cart_items

#     if request.method == 'POST':
#         form = BillingForm(request.POST)
#         if form.is_valid():
#             # Lưu thông tin vào ShippingAddress
#             shipping_address = form.save(commit=False)
#             shipping_address.customer = customer
#             shipping_address.order = order
#             shipping_address.save()

#             # Lấy thông tin từ form
#             shipping_method = form.cleaned_data['ShippingMethod']
#             payment_method = form.cleaned_data['payment']
#             shipping_cost = float(shipping_method)  # Phí vận chuyển: 5$ hoặc 3$

#             if payment_method == 'cod':
#                 # Tính tổng tiền bao gồm phí vận chuyển
#                 cart_total = order.get_cart_total
#                 final_total = cart_total + shipping_cost

#                 # Đánh dấu đơn hàng là hoàn thành
#                 order.date_order = timezone.now()  # Cập nhật lại thời gian đặt hàng thật sự
#                 order.complete = True
#                 order.transaction_id = f"TRANS-{order.id}"
#                 order.shipping_cost = shipping_cost  # Lưu phí vận chuyển vào đơn hàng
#                 order.save()

#                 # Lưu doanh thu vào model Revenue (chỉ tính cart_total, không bao gồm phí ship)
#                 Revenue.objects.create(
#                     order=order,
#                     customer=customer,
#                     amount=cart_total  # Chỉ lấy tổng tiền các món hàng
#                 )

#                 # Lấy thông tin đơn hàng để gửi email
#                 order_items = OrderItem.objects.filter(order=order)
#                 cart_items = order.get_cart_items

#                 # Tạo nội dung email
#                 subject = 'Your Order Confirmation'
#                 message = f"""
#                 Dear {form.cleaned_data['name']},

#                 Thank you for your order! Here are your billing and order details:

#                 **Billing Details:**
#                 Name: {form.cleaned_data['name']}
#                 Address: {shipping_address.address}, {shipping_address.city}
#                 Mobile: {shipping_address.mobile}
#                 Email: {form.cleaned_data['email']}
#                 Order Notes: {form.cleaned_data['order_notes'] if form.cleaned_data['order_notes'] else 'None'}

#                 **Order Details:**
#                 Order ID: {order.id}
#                 Transaction ID: {order.transaction_id}
#                 Total Items: {cart_items}
#                 Subtotal: ${cart_total:.2f}
#                 Shipping Method: {'Fast delivery' if shipping_method == '5' else 'Economy delivery'} (${shipping_cost})
#                 Payment Method: {payment_method.upper()}
#                 Final Total: ${final_total:.2f}

#                 **Items:**
#                 """
#                 for item in order_items:
#                     message += f"- {item.product.name} (x{item.quantity}): ${item.get_total:.2f}\n"

#                 message += """
#                 We will process your order soon.

#                 Best regards,
#                 Your Company Name
#                 """

#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = [form.cleaned_data['email']]

#                 # Gửi email
#                 try:
#                     send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#                     messages.success(request, "Order placed successfully! A confirmation email has been sent.")
#                 except Exception as e:
#                     messages.error(request, f"Order placed, but failed to send email: {e}")

#                 return redirect('success_page')
#     else:
#         form = BillingForm(initial={'name': customer.name, 'email': customer.email, 'address': customer.address, 'mobile': customer.phone})

#     context = {
#         'form': form,
#         'order': order,
#         'items': items,
#         'cartItems': cartItems,
#     }
#     return render(request, 'app/checkout.html', context)


# def checkout(request):
#     if not request.user.is_authenticated:
#         return redirect('loginregister')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập

#     customer = request.user.customer
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     items = order.orderitem_set.all()
#     cartItems = order.get_cart_items

#     if request.method == 'POST':
#         form = BillingForm(request.POST)
#         if form.is_valid():
#             # Lưu thông tin vào ShippingAddress
#             shipping_address = form.save(commit=False)
#             shipping_address.customer = customer
#             shipping_address.order = order
#             shipping_address.save()

#             # Lấy thông tin từ form
#             shipping_method = form.cleaned_data['ShippingMethod']
#             payment_method = form.cleaned_data['payment']
#             shipping_cost = float(shipping_method)  # Phí vận chuyển: 5$ hoặc 3$

#             if payment_method == 'cod':
#                 # Tính tổng tiền bao gồm phí vận chuyển
#                 cart_total = order.get_cart_total
#                 final_total = cart_total + shipping_cost

#                 # Đánh dấu đơn hàng là hoàn thành
#                 order.date_order = timezone.now()  # Cập nhật lại thời gian đặt hàng thật sự
#                 order.complete = True
#                 order.transaction_id = f"TRANS-{order.id}"
#                 order.shipping_cost = shipping_cost  # Lưu phí vận chuyển vào đơn hàng
#                 order.save()

#                 # Lưu doanh thu vào model Revenue (chỉ tính cart_total, không bao gồm phí ship)
#                 Revenue.objects.create(
#                     order=order,
#                     customer=customer,
#                     amount=cart_total  # Chỉ lấy tổng tiền các món hàng
#                 )

#                 # Lấy thông tin đơn hàng để gửi email
#                 order_items = OrderItem.objects.filter(order=order)
#                 cart_items = order.get_cart_items

#                 # Tạo nội dung email với HTML
#                 subject = 'Your Order Confirmation'
#                 message = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                     <style>
#                         body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
#                         .container {{ width: 80%; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
#                         h2 {{ color: #2c3e50; }}
#                         .section {{ margin-bottom: 20px; }}
#                         .section-title {{ font-weight: bold; font-size: 18px; margin-bottom: 10px; }}
#                         .details {{ padding: 10px; background-color: #f9f9f9; border-radius: 5px; }}
#                         .details p {{ margin: 5px 0; }}
#                         .items-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
#                         .items-table th, .items-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
#                         .items-table th {{ background-color: #f2f2f2; }}
#                         .footer {{ margin-top: 20px; font-style: italic; }}
#                     </style>
#                 </head>
#                 <body>
#                     <div class="container">
#                         <h2>Order Confirmation</h2>
#                         <p>Dear {form.cleaned_data['name']},</p>
#                         <p>Thank you for your order! Below are your billing and order details:</p>

#                         <div class="section">
#                             <div class="section-title">Billing Details</div>
#                             <div class="details">
#                                 <p><strong>Name:</strong> {form.cleaned_data['name']}</p>
#                                 <p><strong>Address:</strong> {shipping_address.address}, {shipping_address.city}</p>
#                                 <p><strong>Mobile:</strong> {shipping_address.mobile}</p>
#                                 <p><strong>Email:</strong> {form.cleaned_data['email']}</p>
#                                 <p><strong>Order Notes:</strong> {form.cleaned_data['order_notes'] if form.cleaned_data['order_notes'] else 'None'}</p>
#                             </div>
#                         </div>

#                         <div class="section">
#                             <div class="section-title">Order Details</div>
#                             <div class="details">
#                                 <p><strong>Order ID:</strong> {order.id}</p>
#                                 <p><strong>Transaction ID:</strong> {order.transaction_id}</p>
#                                 <p><strong>Total Items:</strong> {cart_items}</p>
#                                 <p><strong>Subtotal:</strong> ${cart_total:.2f}</p>
#                                 <p><strong>Shipping Method:</strong> {'Fast delivery' if shipping_method == '5' else 'Economy delivery'} (${shipping_cost})</p>
#                                 <p><strong>Payment Method:</strong> {payment_method.upper()}</p>
#                                 <p><strong>Final Total:</strong> ${final_total:.2f}</p>
#                             </div>
#                         </div>

#                         <div class="section">
#                             <div class="section-title">Items</div>
#                             <table class="items-table">
#                                 <tr>
#                                     <th>Product</th>
#                                     <th>Quantity</th>
#                                     <th>Total</th>
#                                 </tr>
#                 """
#                 for item in order_items:
#                     message += f"""
#                                 <tr>
#                                     <td>{item.product.name}</td>
#                                     <td>{item.quantity}</td>
#                                     <td>${item.get_total:.2f}</td>
#                                 </tr>
#                     """
#                 message += """
#                             </table>
#                         </div>

#                         <div class="footer">
#                             <p>We will process your order soon.</p>
#                             <p>Best regards,<br>Your Company Name</p>
#                         </div>
#                     </div>
#                 </body>
#                 </html>
#                 """

#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = [form.cleaned_data['email']]

#                 # Gửi email
#                 try:
#                     send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)
#                     messages.success(request, "Order placed successfully! A confirmation email has been sent.")
#                 except Exception as e:
#                     messages.error(request, f"Order placed, but failed to send email: {e}")

#                 return redirect('success_page')
#     else:
#         form = BillingForm(initial={'name': customer.name, 'email': customer.email, 'address': customer.address, 'mobile': customer.phone})

#     context = {
#         'form': form,
#         'order': order,
#         'items': items,
#         'cartItems': cartItems,
#     }
#     return render(request, 'app/checkout.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Order, OrderItem, Customer, Revenue
from .forms import BillingForm

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('loginregister')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập

    # Kiểm tra và lấy hoặc tạo bản ghi Customer
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        # Nếu không có bản ghi Customer, tạo mới với thông tin mặc định
        customer = Customer.objects.create(
            user=request.user,
            name=request.user.username,  # Sử dụng username làm tên mặc định
            email=request.user.email if request.user.email else '',  # Sử dụng email từ User nếu có
            phone='',  # Để trống, sẽ được điền qua form
            address='',  # Để trống, sẽ được điền qua form
            role=1 if request.user.is_staff else 0  # Nếu người dùng là admin (is_staff), role=1, ngược lại role=0
        )

    # Lấy hoặc tạo đơn hàng chưa hoàn thành
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = customer
            shipping_address.order = order
            shipping_address.save()

            shipping_method = form.cleaned_data['ShippingMethod']
            payment_method = form.cleaned_data['payment']
            shipping_cost = float(shipping_method)

            cart_total = order.get_cart_total
            final_total = cart_total + shipping_cost

            if payment_method in ['cod', 'online']:
                order.date_order = timezone.now()
                order.complete = True
                order.transaction_id = f"TRANS-{order.id}"
                order.shipping_cost = shipping_cost
                order.save()

                Revenue.objects.create(
                    order=order,
                    customer=customer,
                    amount=cart_total
                )

                # Tạo email nội dung chung
                order_items = OrderItem.objects.filter(order=order)
                cart_items = order.get_cart_items

                subject = 'Your Order Confirmation'
                message = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
                        .container {{ width: 80%; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                        h2 {{ color: #2c3e50; }}
                        .section {{ margin-bottom: 20px; }}
                        .section-title {{ font-weight: bold; font-size: 18px; margin-bottom: 10px; }}
                        .details {{ padding: 10px; background-color: #f9f9f9; border-radius: 5px; }}
                        .details p {{ margin: 5px 0; }}
                        .items-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                        .items-table th, .items-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        .items-table th {{ background-color: #f2f2f2; }}
                        .footer {{ margin-top: 20px; font-style: italic; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Order Confirmation</h2>
                        <p>Dear {form.cleaned_data['name']},</p>
                        <p>Thank you for your order! Below are your billing and order details:</p>

                        <div class="section">
                            <div class="section-title">Billing Details</div>
                            <div class="details">
                                <p><strong>Name:</strong> {form.cleaned_data['name']}</p>
                                <p><strong>Address:</strong> {shipping_address.address}, {shipping_address.city}</p>
                                <p><strong>Mobile:</strong> {shipping_address.mobile}</p>
                                <p><strong>Email:</strong> {form.cleaned_data['email']}</p>
                                <p><strong>Order Notes:</strong> {form.cleaned_data['order_notes'] if form.cleaned_data['order_notes'] else 'None'}</p>
                            </div>
                        </div>

                        <div class="section">
                            <div class="section-title">Order Details</div>
                            <div class="details">
                                <p><strong>Order ID:</strong> {order.id}</p>
                                <p><strong>Transaction ID:</strong> {order.transaction_id}</p>
                                <p><strong>Total Items:</strong> {cart_items}</p>
                                <p><strong>Subtotal:</strong> ${cart_total:.2f}</p>
                                <p><strong>Shipping Method:</strong> {'Fast delivery' if shipping_method == '5' else 'Economy delivery'} (${shipping_cost})</p>
                                <p><strong>Payment Method:</strong> {payment_method.upper()}</p>
                                <p><strong>Final Total:</strong> ${final_total:.2f}</p>
                            </div>
                        </div>

                        <div class="section">
                            <div class="section-title">Items</div>
                            <table class="items-table">
                                <tr>
                                    <th>Product</th>
                                    <th>Quantity</th>
                                    <th>Total</th>
                                </tr>
                """
                for item in order_items:
                    message += f"""
                                <tr>
                                    <td>{item.product.name}</td>
                                    <td>{item.quantity}</td>
                                    <td>${item.get_total:.2f}</td>
                                </tr>
                    """
                message += """
                            </table>
                        </div>

                        <div class="footer">
                            <p>We will process your order soon.</p>
                            <p>Best regards,<br>Fruitables Shop</p>
                        </div>
                    </div>
                </body>
                </html>
                """

                from_email = settings.EMAIL_HOST_USER
                recipient_list = [form.cleaned_data['email']]

                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)
                    messages.success(request, "Order placed successfully! A confirmation email has been sent.")
                except Exception as e:
                    messages.error(request, f"Order placed, but failed to send email: {e}")

                # Lưu city vào session
                request.session['last_city'] = shipping_address.city
                return redirect('success_page')

            else:
                messages.error(request, "Invalid payment method.")
                return redirect('checkout')

    else:
        form = BillingForm(initial={
            'name': customer.name if customer.name else request.user.username,
            'email': customer.email if customer.email else request.user.email,
            'address': customer.address if customer.address else '',
            'mobile': customer.phone if customer.phone else ''
        })

    context = {
        'form': form,
        'order': order,
        'items': items,
        'cartItems': cartItems,
        'username': request.user.username if request.user.is_authenticated else '',
    }
    return render(request, 'app/checkout.html', context)


def success_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
       
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']   
    last_city = request.session.get('last_city', '')
    # Xóa khỏi session sau khi lấy để tránh lưu mãi
    if 'last_city' in request.session:
        del request.session['last_city']
    context = {
        'last_city': last_city,
        'cartItems': cartItems,
    }
    return render(request, 'app/success.html', context )




# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     customer = request.user.customer
#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#     if action == 'add' or action == 'add_cart':  
#         orderItem.quantity += 1
#         orderItem.save()
#     elif action == 'remove':  # Giảm số lượng
#         orderItem.quantity -= 1
#         if orderItem.quantity <= 0:
#             orderItem.delete()
#         else:
#             orderItem.save()
#     elif action == 'delete':  # Xóa sản phẩm khỏi giỏ hàng
#         orderItem.delete()  
#     return JsonResponse({'quantity': orderItem.quantity if orderItem else 0}, safe=False)
def updateItem(request):
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Bạn chưa đăng nhập. Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.'}, status=401)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add' or action == 'add_cart':  
        orderItem.quantity += 1
        orderItem.save()
    elif action == 'remove':  
        orderItem.quantity -= 1
        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()
    elif action == 'delete':  
        orderItem.delete()  
    return JsonResponse({'quantity': orderItem.quantity if orderItem else 0}, safe=False)


def get_cart_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items  # Đếm tổng số lượng sản phẩm trong giỏ hàng
    else:
        cartItems = 0

    return JsonResponse({'cartItems': cartItems})

def get_cart_totalPrice(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_price = order.get_cart_total  # Lấy tổng giá trị giỏ hàng
    else:
        total_price = 0

    return JsonResponse({'total_price': total_price})

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        keys = Product.objects.filter(name__icontains=search)

    return render(request, 'app/search.html', {'keys': keys, 'search': search})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_item_quantity(request):
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ request body
            data = json.loads(request.body)
            product_id = data.get('productId')

            if not product_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)

            # Lấy đơn hàng chưa hoàn thành của người dùng hiện tại
            customer = request.user.customer  # Giả sử User có OneToOneField với Customer
            order, created = Order.objects.get_or_create(
                customer=customer,
                complete=False
            )

            # Lấy OrderItem tương ứng với productId trong đơn hàng
            order_item = OrderItem.objects.filter(
                order=order,
                product__id=product_id
            ).first()

            if order_item:
                return JsonResponse({'quantity': order_item.quantity})
            else:
                return JsonResponse({'quantity': 0})  # Nếu không tìm thấy, trả về 0

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# thêm sản phẩm ở trang detail
# def updateitemdetail(request):
#     try:
#         data = json.loads(request.body)
#         print('Request data:', data)  # Debugging

#         productId = data['productId']
#         action = data['action']
#         quantity = int(data['quantity'])

#         customer = request.user.customer
#         product = Product.objects.get(id=productId)
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

#         if action == 'add-cart-detail':
#             orderItem.quantity += quantity
#             orderItem.save()

#         return JsonResponse({'quantity': orderItem.quantity}, safe=False)
#     except Exception as e:
#         print('Error:', str(e))  # Debugging
#         return JsonResponse({'error': str(e)}, status=500)
def updateitemdetail(request):
    # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Bạn chưa đăng nhập. Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.'}, status=401)

    try:
        data = json.loads(request.body)
        print('Request data:', data)  # Debugging

        productId = data['productId']
        action = data['action']
        quantity = int(data['quantity'])

        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add-cart-detail':
            orderItem.quantity += quantity
            orderItem.save()

        return JsonResponse({'quantity': orderItem.quantity}, safe=False)
    except Exception as e:
        print('Error:', str(e))  # Debugging
        return JsonResponse({'error': str(e)}, status=500)
    

from django.core.paginator import Paginator
from django.template.loader import render_to_string


# def home(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0}
#         cartItems = order['get_cart_items']

#     products = Product.objects.all()
#     category = request.GET.get('category', 'all')
#     page_number = request.GET.get('page', 1)

#     if category == 'all':
#         products = Product.objects.all()
#     else:
#         products = Product.objects.filter(category=category)

#     paginator = Paginator(products, 8)
#     page_obj = paginator.get_page(page_number)

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         products_html = render_to_string('app/partials/product_list.html', {
#             'page_obj': page_obj,
#             'cartItems': cartItems
#         })
#         pagination_html = render_to_string('app/partials/pagination.html', {
#             'page_obj': page_obj,
#             'category': category,
#         })
#         return JsonResponse({'products_html': products_html, 'pagination_html': pagination_html})

#     context = {
#         'page_obj': page_obj,
#         'category': category,
#         'cartItems': cartItems,
#         'products': products,
#     }
#     return render(request, 'app/home.html', context)

from django.db.models import Sum

def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    # Lấy 3 sản phẩm được đặt nhiều nhất
    bestseller_products = Product.objects.filter(
        orderitem__order__complete=True
    ).annotate(
        total_quantity=Sum('orderitem__quantity')
    ).order_by('-total_quantity')[:3]

    products = Product.objects.all()
    category = request.GET.get('category', 'all')
    page_number = request.GET.get('page', 1)

    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)

    paginator = Paginator(products, 8)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('app/partials/product_list.html', {
            'page_obj': page_obj,
            'cartItems': cartItems
        })
        pagination_html = render_to_string('app/partials/pagination.html', {
            'page_obj': page_obj,
            'category': category,
        })
        return JsonResponse({'products_html': products_html, 'pagination_html': pagination_html})

    context = {
        'page_obj': page_obj,
        'category': category,
        'cartItems': cartItems,
        'products': products,
        'bestseller_products': bestseller_products,  # Thêm bestseller_products vào context
    }
    return render(request, 'app/home.html', context)

@login_required
def update_personal_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer = request.user.customer
        # Cập nhật thông tin cá nhân
        customer.name = data.get('fullname')
        customer.email = data.get('email')
        customer.address = data.get('address')
        customer.phone = data.get('phone')
        customer.save()
        return JsonResponse({'success': True})
    
#from django.contrib.auth import update_session_auth_hash  
@login_required
def update_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Kiểm tra mật khẩu hiện tại
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()

            # Cập nhật session auth hash để người dùng không bị đăng xuất
            # update_session_auth_hash(request, user)  
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Mật khẩu hiện tại không đúng'}, status=400)

from django.utils.timezone import localtime
import pytz
def order_detail_api(request, order_id):
  
    order = get_object_or_404(Order, id=order_id)

     # Chuyển đổi giờ về múi giờ Việt Nam
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    order_date_vn = localtime(order.date_order, vietnam_tz).strftime("%d/%m/%Y %H:%M")
    
    # Prepare order data
    order_data = {
        "order_id": order.id,
        "customer_name": order.customer.name,
        "address": order.customer.address,
        "order_date": order_date_vn,
        "products": [
            {
                "name": item.product.name,
                "quantity": item.quantity,
                "price": f"{item.product.price}$"
            } for item in order.orderitem_set.all()
        ],
        "product_total": f"{order.get_cart_total}$",
        "shipping_fee": f"{order.shipping_cost}$",
        "total": f"{order.get_final_total}$"
    }

    return JsonResponse(order_data)

@login_required
def reorder_order(request, order_id):
    if request.method == 'POST':
        try:
            # Lấy đơn hàng cũ
            old_order = get_object_or_404(Order, id=order_id)
            
           
            
            # Lấy hoặc tạo giỏ hàng hiện tại (đơn hàng chưa hoàn thành)
            current_order, created = Order.objects.get_or_create(
                customer=request.user.customer,
                complete=False
            )
            
            # Lấy tất cả sản phẩm từ đơn hàng cũ
            old_items = OrderItem.objects.filter(order=old_order)
            
            # Thêm từng sản phẩm vào giỏ hàng hiện tại
            for item in old_items:
                # Kiểm tra xem sản phẩm còn tồn tại không
                if not Product.objects.filter(id=item.product.id).exists():
                    continue
                
                # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
                existing_item = OrderItem.objects.filter(
                    order=current_order,
                    product=item.product
                ).first()
                
                if existing_item:
                    # Nếu đã có thì tăng số lượng
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    # Nếu chưa có thì tạo mới
                    OrderItem.objects.create(
                        product=item.product,
                        order=current_order,
                        quantity=item.quantity
                    )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Phương thức không hợp lệ'}, status=405)


import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product
import re

COHERE_API_KEY = "44Mhomk58aaLnmrHPSXzc56vSsXtNjwtQwMZRGIa"

def search_products_from_db(message):
    filters = Q()
    message = message.lower()

    # Tìm giá
    price_min = None
    price_max = None
    match_min = re.search(r'giá trên (\d+)', message)
    match_max = re.search(r'giá dưới (\d+)', message)
    if match_min:
        price_min = float(match_min.group(1)) * 1
        filters &= Q(price__gte=price_min)
    if match_max:
        price_max = float(match_max.group(1)) * 1
        filters &= Q(price__lte=price_max)

    # Tìm theo từ khóa
    keywords = [w for w in message.split() if len(w) > 2]
    if keywords:
        q_desc = Q()
        for kw in keywords:
            q_desc |= Q(name__icontains=kw) | Q(description__icontains=kw)
        filters &= q_desc

    # Bán chạy
    if "bán chạy" in message:
        bestsellers = Product.objects.filter(
            orderitem__order__complete=True
        ).annotate(
            total_quantity=Sum('orderitem__quantity')
        ).filter(
            total_quantity__gt=0
        ).order_by('-total_quantity')
        
        # Lấy IDs của top 5 sản phẩm bán chạy nhất
        bestseller_ids = list(bestsellers.values_list('id', flat=True)[:5])
        return Product.objects.filter(id__in=bestseller_ids)

    # Trả về kết quả tìm kiếm dựa trên các filter
    return Product.objects.filter(filters)


@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Chỉ hỗ trợ POST request."})

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip().lower()

        # Kiểm tra nếu tin nhắn liên quan đến bảo hành hoặc đổi trả
        warranty_keywords = ['bảo hành', 'đổi trả', 'bảo đảm', 'hoàn tiền', 'đổi size', 'lỗi sản phẩm']
        is_warranty_query = any(keyword in user_message for keyword in warranty_keywords)

        if is_warranty_query:
            contact_info = """
            Để được hỗ trợ về bảo hành hoặc đổi trả sản phẩm, quý khách vui lòng liên hệ với chúng tôi qua:
            
            📞 Hotline: 039-2728-222
            📧 Email: nguyenthat.20072004@gmail.com
            🏪 Địa chỉ: 192 Nguyễn Lương Bằng, Quận Liên Chiểu, TP Đà Nẵng.
            
            Thời gian làm việc: 8:00 - 22:00 (Thứ 2 - Chủ nhật)
            """
            return JsonResponse({"reply": contact_info})
        # Tìm sản phẩm phù hợp
        products = search_products_from_db(user_message)
        product_list_html = ""

        if products.exists():
            product_list_html += "<br><br><strong>Đây là một số mẫu giày phù hợp với bạn:</strong><br>"
            for p in products:
                product_list_html += f"""
                <div class='product-item'>
                    <img class='product-image' src='{p.ImageURL}' alt='{p.name}' />
                    <div class='product-details'>
                        <a href='/detail/?id={p.id}'>{p.name}</a>
                        <div class='price'>{p.price:,.0f} $</div>
                        <div class='description'>{p.first_sentence}</div>
                    </div>
                </div>
                """

        # Gọi API Cohere với context về shop giày
        url = "https://api.cohere.com/v1/chat"
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        } 
        
        # Thêm context về shop giày
        shop_context = """
        Bạn là trợ lý AI của shop giày thể thao BKPro Shop. Shop chuyên cung cấp các mẫu giày thể thao từ thương hiệu Nike và Adidas.
        Bạn có thể tư vấn về:
        - Các mẫu giày phù hợp với từng mục đích sử dụng
        - Cách chọn size giày phù hợp
        - Cách bảo quản giày
        - Chính sách bảo hành, đổi trả
        - Thông tin về các chương trình khuyến mãi
        - Hướng dẫn mua hàng và thanh toán

        Thông tin liên hệ của shop:
        - Hotline: 039-22728-222
        - Email: nguyenthat.20072004@gmail.com
        - Địa chỉ: 192 Nguyễn Lương Bằng, Quận Liên Chiểu, TP Đà Nẵng.

        Khi khách hàng hỏi về bảo hành hoặc đổi trả, hãy cung cấp thông tin liên hệ của shop và chính sách cơ bản:
        - Thời gian bảo hành: 30 ngày kể từ ngày mua
        - Điều kiện đổi trả: Sản phẩm còn nguyên tem mác, chưa qua sử dụng
        - Hướng dẫn khách liên hệ qua hotline hoặc email của shop để được hỗ trợ

        Hãy trả lời mọi câu hỏi trong context của một shop giày thể thao.
        """

        payload = {
            "message": user_message,
            "stream": False,
            "chat_history": [],
            "connectors": [],
            "preamble_override": shop_context  # Thêm context
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        cohere_reply = result.get("text", "").strip()
        final_reply = cohere_reply + product_list_html

        return JsonResponse({"reply": final_reply})

    except requests.exceptions.HTTPError as http_err:
        print("Cohere HTTP Error:", http_err.response.text)
        return JsonResponse({"reply": "Xin lỗi, AI đang bận. Vui lòng thử lại sau."})
    except Exception as e:
        print("Error in chatbot:", e)
        return JsonResponse({"reply": "Đã xảy ra lỗi không mong muốn. Vui lòng thử lại."})