from django.test import SimpleTestCase
from django.urls import reverse, resolve
from webstore.views import loginPage
from cloth_store import urls

class TestUrls(SimpleTestCase):
    def test_loginpage(self):
        url = reverse('login-user')
        self.assertEquals(resolve(url).func, loginPage)