from django import forms
from django.contrib.auth import get_user_model

from .models import Order

User = get_user_model()


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Data otrymania zamowienia'

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Użytkownik "{username} nie zarejestrowany!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Nieprawidlowe hasło")
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['password'].label = 'Hasło'
        self.fields['confirm_password'].label = 'Powtórzyć hasło'
        self.fields['phone'].label = 'Telefon'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazviśko'
        self.fields['address'].label = 'Adres'
        self.fields['email'].label = 'Email'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net']:
            raise forms.ValidationError(
                f'Rejestracja domeny {domain} niemożliwa'
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                f'Ten email już zarejestrowany'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'Imię {username} zajęte'
            )
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Nie prawidłowe hasło')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']
