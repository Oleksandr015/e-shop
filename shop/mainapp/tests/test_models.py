from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from mainapp.models import (
    Category,
    Product,
    Notebook,
    Smartphone,
    CartProduct,
    Cart,
    Customer,
    Order
)

User = get_user_model()


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='TV', slug='tv')

    def test_name_label(self):
        new_category = Category.objects.get(id=1)
        field_label = new_category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Nazwa kategorii')

    def test_first_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_model_output(self):
        category = Category.objects.get(id=1)
        expected_category_output = category.name
        self.assertEqual(expected_category_output, str(category))

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.get_absolute_url(), '/category/tv/')


class NotebookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Notebook', slug='notebook')
        image = SimpleUploadedFile('notebook_image.jpg', content=b'', content_type='image/jpg')
        Notebook.objects.create(category=category,
                                title='SAMSUNG LED UE55TU8502',
                                slug='sumsung-led-uE55tu8502',
                                description='Wciągnij się w obraz z miliardem odcieni kolorów.',
                                image=image,
                                price=Decimal('2399.00'),
                                diagonal='15.6',
                                display_type='LED',
                                processor_freg='Intel Core i7-10750H',
                                ram='6 GB',
                                video='NVIDIA GeForce GTX 1650 TI',
                                time_without_charge='6 hours')

    def test_name_category(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'Kategoria')

    def test_name_title(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Nazwa towaru')

    def test_name_description(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Opis towaru')

    def test_name_price(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'Cena')

    def test_name_diagonal(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('diagonal').verbose_name
        self.assertEqual(field_label, 'Cale')

    def test_name_display_type(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('display_type').verbose_name
        self.assertEqual(field_label, 'Typ displeja')

    def test_name_processor_freg(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('processor_freg').verbose_name
        self.assertEqual(field_label, 'Czastotnosc procesora')

    def test_name_ram(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('ram').verbose_name
        self.assertEqual(field_label, 'RAM')

    def test_name_video(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('video').verbose_name
        self.assertEqual(field_label, 'Karta graficzna')

    def test_name_time_without_charge(self):
        new_product = Notebook.objects.get(id=1)
        field_label = new_product._meta.get_field('time_without_charge').verbose_name
        self.assertEqual(field_label, 'Czas pracy baterii')

    def test_price_type(self):
        self.new_product = Notebook.objects.get(id=1)
        self.assertEqual(self.new_product.price, Decimal('2399.00'))

    def test_title_max_length(self):
        notebook = Notebook.objects.get(id=1)
        max_length = notebook._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_diagonal_max_length(self):
        notebook = Notebook.objects.get(id=1)
        max_length = notebook._meta.get_field('diagonal').max_length
        self.assertEquals(max_length, 255)

    def test_processor_freg_max_length(self):
        notebook = Notebook.objects.get(id=1)
        max_length = notebook._meta.get_field('processor_freg').max_length
        self.assertEquals(max_length, 255)

    def test_ram_max_length(self):
        notebook = Notebook.objects.get(id=1)
        max_length = notebook._meta.get_field('ram').max_length
        self.assertEquals(max_length, 255)

    def test_video_max_length(self):
        notebook = Notebook.objects.get(id=1)
        max_length = notebook._meta.get_field('video').max_length
        self.assertEquals(max_length, 255)

    def test_notebook_output(self):
        notebook = Notebook.objects.get(id=1)
        expected_notebook_output = notebook.title
        self.assertEqual(expected_notebook_output, 'SAMSUNG LED UE55TU8502')

    def test_get_absolute_url(self):
        notebook = Notebook.objects.get(id=1)
        self.assertEquals(notebook.get_absolute_url(), '/products/notebook/sumsung-led-uE55tu8502/')


class SmartphoneModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Smartphone', slug='smartphone')
        image = SimpleUploadedFile('smartphone_image.jpg', content=b'', content_type='image/jpg')
        Smartphone.objects.create(
            category=category,
            title='APPLE iPhone 12 128GB Niebieski 5G',
            slug='apple-iphone-12-5g-blue-128gb',
            description='Nowy iPhone 12 to smartfon wyposażony '
                        'we wszystko, czego możesz potrzebować. '
                        'Superszybka technologia 5G, udoskonalony tryb nocny, '
                        'wyświetlacz w technologii OLED.',
            image=image,
            price=Decimal('4220.00'),
            diagonal='6.1"',
            display_type='2532 x 1170px',
            resolution='OLED Super Retina XDR',
            accum_volume='12 god.',
            ram='4 GB',
            sd='False',
            sd_volume_max='128 GB',
            main_cam_mp='12 Mpx',
            frontal_cam_mp=' 2 x 12 Mpx'
        )

    def test_name_diagonal(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('diagonal').verbose_name
        self.assertEqual(field_label, 'Cale')

    def test_name_display_type(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('display_type').verbose_name
        self.assertEqual(field_label, 'Rodzaj displeja')

    def test_name_resolution(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('resolution').verbose_name
        self.assertEqual(field_label, 'Rozdzielczosc ekranu')

    def test_name_accum_volume(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('accum_volume').verbose_name
        self.assertEqual(field_label, 'Pojemnosc baterii')

    def test_name_ram(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('ram').verbose_name
        self.assertEqual(field_label, 'RAM')

    def test_name_sd(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('sd').verbose_name
        self.assertEqual(field_label, 'Dostępność karty SD')

    def test_name_sd_volume_max(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('sd_volume_max').verbose_name
        self.assertEqual(field_label, 'Objętość pamieci')

    def test_name_main_cam_mp(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('main_cam_mp').verbose_name
        self.assertEqual(field_label, 'Glowna kamera')

    def test_name_frontal_cam_mp(self):
        new_product = Smartphone.objects.get(id=1)
        field_label = new_product._meta.get_field('frontal_cam_mp').verbose_name
        self.assertEqual(field_label, 'Selfi camera')

    def test_diagonal_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('diagonal').max_length
        self.assertEquals(max_length, 255)

    def test_display_type_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('display_type').max_length
        self.assertEquals(max_length, 255)

    def test_resolution_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('resolution').max_length
        self.assertEquals(max_length, 255)

    def test_accum_volume_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('accum_volume').max_length
        self.assertEquals(max_length, 255)

    def test_ram_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('ram').max_length
        self.assertEquals(max_length, 255)

    def test_sd_volume_max_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('sd_volume_max').max_length
        self.assertEquals(max_length, 255)

    def test_main_cam_mp_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('main_cam_mp').max_length
        self.assertEquals(max_length, 255)

    def test_frontal_cam_mp_max_length(self):
        product = Smartphone.objects.get(id=1)
        max_length = product._meta.get_field('frontal_cam_mp').max_length
        self.assertEquals(max_length, 255)

    def test_smartphone_output(self):
        smartphone = Smartphone.objects.get(id=1)
        expected_smartphone_output = smartphone.title
        self.assertEqual(expected_smartphone_output, 'APPLE iPhone 12 128GB Niebieski 5G')

    def test_get_absolute_url(self):
        smartphone = Smartphone.objects.get(id=1)
        self.assertEquals(smartphone.get_absolute_url(), '/products/smartphone/apple-iphone-12-5g-blue-128gb/')


class CartModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user', password='password')
        customer = Customer.objects.create(user=user, phone='813813813', address='Krakow')
        cart = Cart.objects.create(owner=customer)
        category = Category.objects.create(name='Notebook', slug='notebook')
        image = SimpleUploadedFile('notebook_image.jpg', content=b'', content_type='image/jpg')
        notebook = Notebook.objects.create(category=category,
                                           title='SAMSUNG LED UE55TU8502',
                                           slug='sumsung-led-uE55tu8502',
                                           description='Wciągnij się w obraz z miliardem odcieni kolorów.',
                                           image=image,
                                           price=Decimal('2399.00'),
                                           diagonal='15.6',
                                           display_type='LED',
                                           processor_freg='Intel Core i7-10750H',
                                           ram='6 GB',
                                           video='NVIDIA GeForce GTX 1650 TI',
                                           time_without_charge='6 hours')
        CartProduct.objects.create(user=customer, cart=cart, content_object=notebook)
        Order.objects.create(
            customer=customer,
            first_name='Piotr',
            last_name='Kowalski',
            phone='112112112',
            cart=cart,
            address='Warszawa',
            status='Nowe zamowienie',
            buying_type='delivery')

    def test_name_main_user(self):
        user = CartProduct.objects.get(id=1)
        field_label = user._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Konsument')

    def test_name_main_cart(self):
        name = CartProduct.objects.get(id=1)
        field_label = name._meta.get_field('cart').verbose_name
        self.assertEqual(field_label, 'Koszyk')

    def test_name_main_final_price(self):
        name = CartProduct.objects.get(id=1)
        field_label = name._meta.get_field('final_price').verbose_name
        self.assertEqual(field_label, 'Cena')

    def test_name_main_owner(self):
        name = Cart.objects.get(id=1)
        field_label = name._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'Klient')

    def test_name_main_user_customer(self):
        name = Customer.objects.get(id=1)
        field_label = name._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Konsument')

    def test_name_main_phone(self):
        name = Customer.objects.get(id=1)
        field_label = name._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Numer tel.')

    def test_name_main_address(self):
        name = Customer.objects.get(id=1)
        field_label = name._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'Adres')

    def test_name_main_orders(self):
        name = Customer.objects.get(id=1)
        field_label = name._meta.get_field('orders').verbose_name
        self.assertEqual(field_label, 'Zamowienia klienta')

    def test_phone_max_length(self):
        product = Customer.objects.get(id=1)
        max_length = product._meta.get_field('phone').max_length
        self.assertEquals(max_length, 20)

    def test_address_max_length(self):
        product = Customer.objects.get(id=1)
        max_length = product._meta.get_field('address').max_length
        self.assertEquals(max_length, 255)

    def test_cart_product_output(self):
        new_cp = CartProduct.objects.get(id=1)
        expected_cp_output = 'Produkt: %s (w koszyku)' % (new_cp.content_object.title)
        self.assertEqual(expected_cp_output, str(new_cp))

    def test_cart_output(self):
        new_cart = Cart.objects.get(id=1)
        expected_cp_output = new_cart.id
        self.assertEqual(expected_cp_output, int(str(new_cart)))

    def test_customer_output(self):
        new_customer = Customer.objects.get(id=1)
        expected_cp_output = 'Konsument: %s %s' % (new_customer.user.first_name, new_customer.user.last_name)
        self.assertEqual(expected_cp_output, str(new_customer))
