from django.test import TestCase, Client
from django.urls import reverse
from webstore.models import User, Customer
from webstore.views import loginPage
class TestViews(TestCase):

    # This Method Will Run before every single test method
    def setUp(self):
        self.client = Client()

    def test_register_customer(self):
        responce = self.client.get(reverse('register-user'))
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, 'webstore/register_customer.html')

