from decimal import Decimal
from unittest import mock
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage

from mainapp.utils import recalc_cart
from mainapp.views import BaseView, AddToCartView

from mainapp.models import (
    Category,
    Notebook,
    CartProduct,
    Cart,
    Customer
)

User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='password')
        self.category = Category.objects.create(name='Notebook', slug='notebook')
        image = SimpleUploadedFile('notebook_image.jpg', content=b'', content_type='image/jpg')
        self.notebook = Notebook.objects.create(
            category=self.category,
            title='Test Notebook',
            slug='test-slug',
            description='Wciągnij się w obraz z miliardem odcieni kolorów.',
            image=image,
            price=Decimal('2399.00'),
            diagonal='15.6',
            display_type='LED',
            processor_freg='Intel Core i7-10750H',
            ram='6 GB',
            video='NVIDIA GeForce GTX 1650 TI',
            time_without_charge='6 hours'
        )
        self.customer = Customer.objects.create(user=self.user, phone='813813813', address='Krakow')
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.notebook
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal(2399.00))

    def test_response_from_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = AddToCartView.as_view()(request, ct_model='notebook', slug='test-slug')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)
