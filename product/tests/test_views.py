from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from webstore.models import User, Customer
from product.models import Category,Product, sub_products, Brand, Cart, WishList

def create_login_user(client):
    customer_register_data = {'username': ['jlcdu'], 'email': ['2800bhargav@gmail.com'],'password1': ['123456@As'], 'password2': ['123456@As'], 'name': ['ljcaegyb'],'age': ['22'], 'gender': ['Male'], 'mobile_no': ['+911234567895']}
    customer_login_data = {'email': ['2800bhargav@gmail.com'], 'password': ['123456@As']}
    client.post(reverse('register-user'), customer_register_data, format='text/html')
    user = User.objects.get(email='2800bhargav@gmail.com')
    user.is_active = True
    user.save()
    customer = Customer.objects.get(email='2800bhargav@gmail.com')
    client.post(reverse('login-user'), customer_login_data, format='text/html')

    return customer

def create_product(client):
    brand_data = {'username': ['Ajio'], 'email': ['Ajio@gmail.com'], 'password1': ['123456@As'],'password2': ['123456@As'], 'brand_name': ['Ajio']}
    new_group, created = Group.objects.get_or_create(name='brand_permission')
    ct1 = ContentType.objects.get_for_model(Product)
    ct2 = ContentType.objects.get_for_model(Brand)
    ct3 = ContentType.objects.get_for_model(sub_products)
    ct4 = ContentType.objects.get_for_model(User)
    new_group.permissions.add(Permission.objects.create(codename='can_add_product', name='Can add product', content_type=ct1))
    new_group.permissions.add(Permission.objects.create(codename='can_change_product', name='Can change product', content_type=ct1))
    new_group.permissions.add(Permission.objects.create(codename='can_delete_product', name='Can delete product', content_type=ct1))
    new_group.permissions.add(Permission.objects.create(codename='can_view_product', name='Can view product', content_type=ct1))

    new_group.permissions.add(Permission.objects.create(codename='can_change_brand', name='Can change brand', content_type=ct2))
    new_group.permissions.add(Permission.objects.create(codename='can_delete_brand', name='Can delete brand', content_type=ct2))
    new_group.permissions.add(Permission.objects.create(codename='can_view_brand', name='Can view brand', content_type=ct2))

    new_group.permissions.add(Permission.objects.create(codename='can_add_sub_products', name='Can add sub_products', content_type=ct3))
    new_group.permissions.add(Permission.objects.create(codename='can_change_sub_products', name='Can change sub_products', content_type=ct3))
    new_group.permissions.add(Permission.objects.create(codename='can_delete_sub_products', name='Can delete sub_products', content_type=ct3))
    new_group.permissions.add(Permission.objects.create(codename='can_view_sub_products', name='Can view sub_products', content_type=ct3))

    new_group.permissions.add(Permission.objects.create(codename='can_change_user', name='Can change user', content_type=ct4))
    new_group.permissions.add(Permission.objects.create(codename='can_delete_user', name='Can delete user', content_type=ct4))
    new_group.permissions.add(Permission.objects.create(codename='can_view_user', name='Can view user', content_type=ct4))
    cat = Category.objects.create(name="traditional")
    client.post(reverse('register-brand'), brand_data, format='text/html')
    brand_ins = Brand.objects.get(brand_name='Ajio')
    product_ins = Product.objects.create(brand=brand_ins, category=cat, name="Ajio Pent", image="/static/images/10.png", short_line="Best quality pents", price=1234.5, discount=12, target_audience='Men')
    sub_product_ins = sub_products.objects.create(product=product_ins, quantity=2, size='XL', color='red', description="Red color, XL size Pent From Ajio Qality Brand")

    return [sub_product_ins, product_ins]



def create_cart_instance(client, user, product):
    cart = Cart.objects.create(customer = user, product = product[0], added_quantity=1)
    return cart

def create_wishlist_instance(client, user, product):
    wishlist = WishList.objects.create(customer = user, product = product[1])
    return wishlist


class ViewHomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/home.html')


class ProductDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.review = {'review_field': 'This Product is awesome'}

    def test_view_product_detail_page(self):

        # Firstly Make An Product
        Created_product = create_product(self.client)

        response = self.client.get(reverse('product_details', kwargs={'pk':Created_product[0].id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_detail.html')

    def test_product_review(self):
        Created_product = create_product(self.client)

        user = create_login_user(self.client)

        response = self.client.post(reverse('product_details', kwargs={'pk':Created_product[0].id}), self.review, format='text/html')
        self.assertEqual(response.url, reverse('product_details', kwargs={'pk':Created_product[0].id}))
        self.assertEqual(response.status_code, 302)


class ProductPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_filter_product(self):

        Created_product = create_product(self.client)

        response = self.client.get(reverse('target_audience', kwargs={'target_audience':'Men'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/filter_items_page.html')

        response = self.client.get(reverse('product_page', kwargs={'category': 'traditional'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/filter_items_page.html')


class UpdateQuantityTest(TestCase):
    def test_update_cart_quantity(self):
        user = create_login_user(self.client)
        created_product = create_product(self.client)

        cart = create_cart_instance(self.client, user, created_product)
        create_login_user(self.client)
        response = self.client.post(reverse('update_quantity'), {'pid':cart.product.id, 'quantity':3},format='text/html')
        self.assertEqual(Cart.objects.get(id=cart.id).added_quantity, 3)
        self.assertEqual(response.status_code, 200)


class ViewCartTest(TestCase):
    def test_view_cart(self):
        create_login_user(self.client)
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/cart.html')


class ViewWishlistTest(TestCase):
    def test_view_cart(self):
        create_login_user(self.client)
        response = self.client.get(reverse('view_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/wishlist.html')


class AddToCartTest(TestCase):
    def test_add_to_cart(self):
        created_product = create_product(self.client)
        user = create_login_user(self.client)
        response = self.client.post(reverse('add_to_cart', kwargs={'product_id': created_product[1].id}), {'color_dropdown':created_product[0].color , 'size_dropdown':created_product[0].size}, format='text/html')
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(response.status_code, 302)

class AddToWishlistTest(TestCase):
    def test_add_to_wishlist(self):
        created_product = create_product(self.client)
        user = create_login_user(self.client)
        response = self.client.post(reverse('add_to_wishlist', kwargs={'product_id': created_product[1].id}), format='text/html')
        self.assertEqual(response.url, reverse('view_wishlist'))
        self.assertEqual(response.status_code, 302)


class RemoveFromCartTest(TestCase):
    def test_rermove_from_cart(self):
        created_product = create_product(self.client)
        user = create_login_user(self.client)
        cart = create_cart_instance(self.client, user, created_product)
        response = self.client.post(reverse('remove_from_cart', kwargs={'product_id': cart.id}),format='text/html')
        self.assertEqual(response.url, reverse('view_cart'))
        self.assertEqual(response.status_code, 302)

class RemoveFromWishlistTest(TestCase):
    def test_rermove_from_wishlist(self):
        created_product = create_product(self.client)
        user = create_login_user(self.client)
        wishlist = create_wishlist_instance(self.client, user, created_product)
        response = self.client.post(reverse('remove_from_wishlist', kwargs={'product_id': wishlist.product.id}),format='text/html')
        self.assertEqual(response.url, reverse('view_wishlist'))
        self.assertEqual(response.status_code, 302)

class ConfirmOrderTest(TestCase):
    def test_confirm_order_get(self):
        user = create_login_user(self.client)
        response = self.client.get(reverse('confirm_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/confirm_order.html')

    def test_confirm_order_COD(self):
        user = create_login_user(self.client)
        response = self.client.post(reverse('confirm_order'),{'total_amount':2000,'COD':True,'address':"jgacs"},format='text/html')
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(response.status_code, 302)


    def test_confirm_order_Razorpay(self):
        user = create_login_user(self.client)
        response = self.client.post(reverse('confirm_order'),{'total_amount':2000,'address':"jgacs"},format='text/html')
        self.assertTemplateUsed(response, 'product/paymentsummary.html')
        self.assertEqual(response.status_code, 200)


