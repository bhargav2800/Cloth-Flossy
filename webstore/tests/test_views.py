from django.test import TestCase, Client
from django.urls import reverse
from webstore.models import User
from product.models import Product, sub_products, Brand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class RegisterCustomerTest(TestCase):

    # This Method Will Run before every single test method
    def setUp(self):
        self.client = Client()
        self.user_data = {'username': ['jlcdu'], 'email': ['2800bhargav@gmail.com'], 'password1': ['123456@As'], 'password2': ['123456@As'], 'name': ['ljcaegyb'], 'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+911234567895']}
        self.user_invalid_email_data = {'username': ['jlcdu'], 'email': ['2800bhargavgmail.com'], 'password1': ['123456@As'], 'password2': ['123456@As'], 'name': ['ljcaegyb'], 'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+911234567895']}
        self.user_missmatch_password_data = {'username': ['jlcdu'], 'email': ['2800bhargavgmail.com'],'password1': ['123456@A'], 'password2': ['123456@As'], 'name': ['ljcaegyb'],'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+911234567895']}
        self.user_invalid_password_data = {'username': ['jlcdu'], 'email': ['2800bhargavgmail.com'],'password1': ['123456@as'], 'password2': ['123456@as'],'name': ['ljcaegyb'], 'age': ['22'], 'gender': ['Male'],'mobile_no': ['+911234567895']}

    def test_register_customer_valid_data(self):
        #get request
        response = self.client.get(reverse('register-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/register_customer.html')

        # Post Request
        response = self.client.post(reverse('register-user'), self.user_data, format='text/html')
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_email_data(self):
        response = self.client.post(reverse('register-user'), self.user_invalid_email_data, format='text/html')
        self.assertEqual(response.url, reverse('register-user'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_missmatch_password_data(self):
        response = self.client.post(reverse('register-user'), self.user_missmatch_password_data, format='text/html')
        self.assertEqual(response.url, reverse('register-user'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_password_data(self):
        response = self.client.post(reverse('register-user'), self.user_invalid_password_data, format='text/html')
        self.assertEqual(response.url, reverse('register-user'))
        self.assertEqual(response.status_code, 302)


class RegisterBrandTest(TestCase):

    # This Method Will Run before every single test method
    def setUp(self):
        self.client = Client()
        self.brand_data = {'username': ['Ajio'], 'email': ['Ajio@gmail.com'], 'password1': ['123456@As'], 'password2': ['123456@As'], 'brand_name': ['Ajio']}
        self.brand_invalid_email_data = {'username': ['Ajio'], 'email': ['Ajiogmail.com'], 'password1': ['123456@As'], 'password2': ['123456@As'], 'brand_name': ['Ajio']}
        self.brand_missmatch_password_data = {'username': ['Ajio'], 'email': ['Ajio@gmail.com'], 'password1': ['123456@A'], 'password2': ['123456@As'], 'brand_name': ['Ajio']}
        self.brand_invalid_password_data = {'username': ['Ajio'], 'email': ['Ajio@gmail.com'], 'password1': ['123456@as'], 'password2': ['123456@as'], 'brand_name': ['Ajio']}
        new_group, created = Group.objects.get_or_create(name='brand_permission')
        ct1 = ContentType.objects.get_for_model(Product)
        ct2 = ContentType.objects.get_for_model(Brand)
        ct3 = ContentType.objects.get_for_model(sub_products)
        ct4 = ContentType.objects.get_for_model(User)
        # Now what - Say I want to add 'Can add project' permission to new_group?
        new_group.permissions.add(Permission.objects.create(codename='can_add_product',name='Can add product',content_type=ct1))
        new_group.permissions.add(Permission.objects.create(codename='can_change_product',name='Can change product',content_type=ct1))
        new_group.permissions.add(Permission.objects.create(codename='can_delete_product',name='Can delete product',content_type=ct1))
        new_group.permissions.add(Permission.objects.create(codename='can_view_product',name='Can view product',content_type=ct1))

        new_group.permissions.add(Permission.objects.create(codename='can_change_brand',name='Can change brand',content_type=ct2))
        new_group.permissions.add(Permission.objects.create(codename='can_delete_brand',name='Can delete brand',content_type=ct2))
        new_group.permissions.add(Permission.objects.create(codename='can_view_brand',name='Can view brand',content_type=ct2))

        new_group.permissions.add(Permission.objects.create(codename='can_add_sub_products', name='Can add sub_products', content_type=ct3))
        new_group.permissions.add(Permission.objects.create(codename='can_change_sub_products', name='Can change sub_products', content_type=ct3))
        new_group.permissions.add(Permission.objects.create(codename='can_delete_sub_products', name='Can delete sub_products', content_type=ct3))
        new_group.permissions.add(Permission.objects.create(codename='can_view_sub_products', name='Can view sub_products', content_type=ct3))

        new_group.permissions.add(Permission.objects.create(codename='can_change_user', name='Can change user', content_type=ct4))
        new_group.permissions.add(Permission.objects.create(codename='can_delete_user', name='Can delete user', content_type=ct4))
        new_group.permissions.add(Permission.objects.create(codename='can_view_user', name='Can view user', content_type=ct4))


    def test_register_brand_valid_data(self):
        #get request
        response = self.client.get(reverse('register-brand'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/register_brand.html')

        #post request
        response = self.client.post(reverse('register-brand'), self.brand_data, format='text/html')
        self.assertEqual(response.url, reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_email_data(self):
        response = self.client.post(reverse('register-brand'), self.brand_invalid_email_data, format='text/html')
        self.assertEqual(response.url, reverse('register-brand'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_missmatch_password_data(self):
        response = self.client.post(reverse('register-brand'), self.brand_missmatch_password_data, format='text/html')
        self.assertEqual(response.url, reverse('register-brand'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_password_data(self):
        response = self.client.post(reverse('register-brand'), self.brand_invalid_password_data, format='text/html')
        self.assertEqual(response.url, reverse('register-brand'))
        self.assertEqual(response.status_code, 302)



class LoginCustomerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_register_data = {'username': ['jlcdu'], 'email': ['2800bhargav@gmail.com'], 'password1': ['123456@As'],'password2': ['123456@As'], 'name': ['ljcaegyb'], 'age': ['22'], 'gender': ['Male'],'mobile_no': ['+911234567895']}
        self.customer_login_data = {'email': ['2800bhargav@gmail.com'], 'password': ['123456@As']}
        self.user_invalid_email_data = {'email': ['2800bharga@gmail.com'], 'password': ['123456@As']}
        self.user_invalid_password_data = {'email': ['2800bhargav@gmail.com'], 'password': ['123456@s']}


    def test_login_customer_valid_data(self):
        #get request
        response = self.client.get(reverse('login-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/login_customer.html')

        # Post Request
        self.client.post(reverse('register-user'), self.customer_register_data, format='text/html')
        user = User.objects.get(email='2800bhargav@gmail.com')
        user.is_active = True
        user.save()
        response = self.client.post(reverse('login-user'), self.customer_login_data, format='text/html')
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_email_data(self):
        response = self.client.post(reverse('login-user'), self.user_invalid_email_data, format='text/html')
        self.assertEqual(response.url, reverse('login-user'))
        self.assertEqual(response.status_code, 302)

    def test_register_customer_invalid_password_data(self):
        response = self.client.post(reverse('login-user'), self.user_invalid_password_data, format='text/html')
        self.assertEqual(response.url, reverse('login-user'))
        self.assertEqual(response.status_code, 302)


class UpdateCustomerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_register_data = {'username': ['jlcdu'], 'email': ['2800bhargav@gmail.com'],'password1': ['123456@As'], 'password2': ['123456@As'], 'name': ['ljcaegyb'],'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+911234567895']}
        self.customer_login_data = {'email': ['2800bhargav@gmail.com'], 'password': ['123456@As']}

        self.update_customer_data = {'email': ['2800bhargav@gmail.com'], 'name': ['ljcaegyb'], 'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+919662316938'], 'fav_brand_select': [], 'avatar': ['']}



    def test_update_customer_get_data(self):
        #get request
        self.client.post(reverse('register-user'), self.customer_register_data, format='text/html')
        user = User.objects.get(email='2800bhargav@gmail.com')
        user.is_active = True
        user.save()

        self.client.post(reverse('login-user'), self.customer_login_data, format='text/html')

        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webstore/user_profile.html')


    def test_update_customer_valid_data(self):
        self.client.post(reverse('register-user'), self.customer_register_data, format='text/html')
        user = User.objects.get(email='2800bhargav@gmail.com')
        user.is_active = True
        user.save()

        self.client.post(reverse('login-user'), self.customer_login_data, format='text/html')

        # Post Request
        response = self.client.post(reverse('user-profile'), self.update_customer_data, format='text/html')
        self.assertEqual(response.url, reverse('user-profile'))
        self.assertEqual(response.status_code, 302)