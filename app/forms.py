from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer  # Import model Customer
from .models import ShippingAddress

        
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Nhập mật khẩu")
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'phone', 'address']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã được sử dụng.")
        return username


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa số.")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Email phải có định dạng @gmail.com")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user


class BillingForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Order Notes (Optional)'})
    )
    # Trường ShippingMethod và payment không thuộc model, nên khai báo riêng
    SHIPPING_CHOICES = [
        ('5', 'Fast delivery: 5$'),
        ('3', 'Economy delivery: 3$'),
    ]
    PAYMENT_CHOICES = [
        ('cod', 'Cash On Delivery'),
        ('online', 'Online Payment'),
    ]
    ShippingMethod = forms.ChoiceField(
        choices=SHIPPING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input bg-primary border-0'}),
        required=False
    )
    payment = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input bg-primary border-0'}),
        required=False
    )

    class Meta:
        model = ShippingAddress
        fields = ['address', 'mobile', 'city']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House Number Street Name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your City Address*'}),
        }