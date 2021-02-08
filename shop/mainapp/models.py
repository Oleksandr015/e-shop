import sys
from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_urls(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


'''
1 Category
2 Product
3 CartProduct
4 Cart
5 Order
6 Customer
'''


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Laptopy': 'notebook__count',
        'Smartfony': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
                for c in qs
                ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa kategorii')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728  # 3Mb

    class Meta:
        abstract = True

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

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MIN_RESOLUTION
        if img.height < min_height or img.weihgt < min_width:
            raise MinResolutionErrorException('Rozmiar zdjecia mniejszy za minimalne')
        if img.height > max_height or img.weihgt > max_width:
            raise MaxResolutionErrorException('Rozmiar zdjecia wiekszy za maksymalne')
        super().save(*args, **kwargs)
        # Jesli zachcemy pokroic rysunek w locie -->
        #
        # image = self.image
        # img = Image.open(image)
        # new_img = img.convert('RGB')
        # resized_new_img = new_img.resize((800, 800), Image.ANTIALIAS)
        # filestream = BytesIO()
        # file_ = resized_new_img.save(filestream, 'JPEG', quality=90)
        # file_.seek(0)
        # name = '{}.{}'.format(*self.image.name.split('.'))
        # self.image = InMemoryUploadedFile(
        #    file_, 'ImageField', name, 'jpeg/image', sys.getsizeof(file_), None)


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Cale')
    display_type = models.CharField(max_length=255, verbose_name='Typ displeja')
    processor_freg = models.CharField(max_length=255, verbose_name='Czastotnosc procesora')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    video = models.CharField(max_length=255, verbose_name='Karta graficzna')
    time_without_charge = models.CharField(max_length=255, verbose_name='Czas pracy baterii')

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_urls(self, 'product_detail')

    def get_model_name(self):
        return self.__class__._meta.model_name


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Cale')
    display_type = models.CharField(max_length=255, verbose_name='Rodzaj displeja')
    resolution = models.CharField(max_length=255, verbose_name='Rozdzielczosc ekranu')
    accum_volume = models.CharField(max_length=255, verbose_name='Pojemnosc baterii')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    sd = models.BooleanField(default=True, verbose_name='Dostępność karty SD')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Objętość pamieci'
    )
    main_cam_mp = models.CharField(max_length=255, verbose_name='Glowna kamera')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Selfi camera')

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_urls(self, 'product_detail')

    def get_model_name(self):
        return self.__class__._meta.model_name


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Konsument', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Koszyk', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Cena')

    def __str__(self):
        return f"Produkt: {self.content_object.title} (w koszyku)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Client', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Cena')
    in_order = models.BooleanField(default=False)
    for_ananymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Konsument', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Numer tel.', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Adres', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='zamowienia klienta', related_name='related_customer')

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

