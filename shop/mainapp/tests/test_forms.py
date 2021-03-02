from django.test import TestCase

import datetime

from mainapp.forms import OrderForm


class OrderFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = OrderForm()
        self.assertTrue(
            form.fields['order_date'].label is None
            or form.fields['order_date'].label == 'Data otrymania zamowienia')

    def test_order_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'order_date': date}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_order_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'order_date': date}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
