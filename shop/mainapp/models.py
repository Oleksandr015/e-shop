from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

'''
1 Category
2 Product
3 CartProduct
4 Cart
5 Order
6 Customer
'''


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa kategorii')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_fields_for_filter_in_template(self):
        return ProductFeatures.objects.filter(
            category=self,
            use_in_filter=True
        ).prefetch_related('category').value('feature_key', 'feature_measure', 'feature_name', 'filter_type')


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Kategoria', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Nazwa towaru')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Zdjecie')
    description = models.TextField(verbose_name="Opis towaru")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Cena')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class ProductFeatures(models.Model):

    RADIO = 'radio'
    CHECKBOX = 'checkbox'

    FILTER_TYPE_CHOISES = (
        (RADIO, 'Radiobutton'),
        (CHECKBOX, 'Czekboks')
    )
    feature_key = models.CharField(max_length=100, verbose_name='Cechy charakterystyczne')
    feature_name = models.CharField(max_length=255, verbose_name='Imię charakterystyczne')
    category = models.ForeignKey(Category, verbose_name='Kategoria', on_delete=models.CASCADE)
    postfix_for_value = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Przyrostek',
        help_text=f'Na przykład możesz dla "Godziny pracy" dodać przyrostek godzin - "10 godzin".'
    )
    use_in_filter = models.BooleanField(
        default=False,
        verbose_name='Służy do filtrowania produktów w szablonie'
    )
    filter_type = models.CharField(
        max_length=20,
        verbose_name='Typ filtra',
        default=CHECKBOX,
        choices=FILTER_TYPE_CHOISES
    )
    filter_measure = models.CharField(
        max_length=50,
        verbose_name='Służy do filtrowania produktów w szablonie',
        help_text='Jednostka miary dla konkretnego filtra, na przykład - częstotliwość procesora (Ghz).'
    )

    def __str__(self):
        return f'Kategoria - "{self.category.name}" | Charakterystyka - "{self.feature_name}"'


class ProductFeatureValidators(models.Model):

    category = models.ForeignKey(Category, verbose_name='Kategory', on_delete=models.CASCADE)
    feature = models.ForeignKey(
        ProductFeatures, verbose_name='Charakterystyka', null=True, blank=True, on_delete=models.CASCADE
    )
    feature_value = models.CharField(
        max_length=255, unique=True, null=True, blank=True, verbose_name='Wartość сharakterystyky'
    )

    def __str__(self):
        if not self.feature:
            return f'Nie wybrano cech walidatora kategorii"{self.category.name}"'
        return f'Walidator kategorii "{self.category.name}"| ' \
               f'Charakterystyka - "{self.feature.feature_name}" | ' \
               f'Wartość - "{self.feature_value}"'


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Konsument', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Koszyk', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Tovar', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Cena')

    def __str__(self):
        return f"Produkt: {self.product.title} (w koszyku)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Klient', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Cena')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Konsument', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Numer tel.', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Adres', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Zamowienia klienta', related_name='related_customer')

    def __str__(self):
        return f"Konsument: {self.user.first_name} {self.user.last_name}"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Nowe zamowienie'),
        (STATUS_IN_PROGRESS, 'Zamowienie w toku'),
        (STATUS_READY, 'Zamowienie gotowe'),
        (STATUS_COMPLETED, 'Zamowienie wykonane')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Odbior osobisty'),
        (BUYING_TYPE_DELIVERY, 'Z dostawa')
    )

    customer = models.ForeignKey(Customer, verbose_name='Klient', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Imie')
    last_name = models.CharField(max_length=255, verbose_name='Nazwisko')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    cart = models.ForeignKey(Cart, verbose_name='Koszyk', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Adres', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Typ zamowienia',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Komentarz do zamowienia', null=True, blank='True')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Data stworzenia zamowienia')
    order_date = models.DateTimeField(verbose_name='Data otrymania zamowienia', default=timezone.now)

    def __str__(self):
        return str(self.id)

