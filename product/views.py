from django.shortcuts import redirect, render
from .models import Product, Category, Cart, WishList, Order, Invoice, Favourites
from webstore.models import Customer
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.contrib import messages
from .forms import confirm_order_form
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q


# Create your views here.
class home(ListView):
    model = Product
    template_name = 'product/home.html'
    extra_context = {'best_selling': Product.objects.all().order_by('-no_of_purchases')[:10]}


class Product_details(DetailView):
    model = Product
    template_name = 'product/product_detail.html'


class product_page(ListView):
    model = Product
    template_name = 'product/filter_items_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        try:
            category = Category.objects.get(name=self.kwargs.get('category'))
            return Product.objects.filter(category=category)
        except:
            target_audience = self.kwargs.get('target_audience')
            return Product.objects.filter(target_audience=target_audience)


class update_quantity(View):
    def post(self, request, product_instance):
        cart_obj = Cart.objects.get(customer=Customer.objects.get(user=self.request.user), product=product_instance)
        cart_obj.added_quantity = self.request.POST.get('quantity')
        cart_obj.save()
        return redirect('view_cart')


class view_cart(ListView):
    model = Cart
    template_name = 'product/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        customer_instance = Customer.objects.get(user=self.request.user)
        return Cart.objects.filter(customer=customer_instance)


class view_wishlist(ListView):
    model = WishList
    template_name = 'product/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        customer_instance = Customer.objects.get(user=self.request.user)
        return WishList.objects.filter(customer=customer_instance)


class add_to_cart(View):
    def get(self, request, product_id):
        customer_instance = Customer.objects.get(user=request.user)
        product_instance = Product.objects.get(id=product_id)
        try:
            Cart.objects.get(customer=customer_instance, product=product_instance)
            messages.error(request, 'Item Alredy Exist')
            return redirect('home')
        except:
            Cart.objects.create(customer=customer_instance, product=product_instance, added_quantity=1)

            # WishList_instance = WishList.objects.get(customer=customer_instance, product=product_instance)
            # WishList_instance.delete()
            messages.success(request, 'Item Added To Cart')
            return redirect('home')


class add_to_wishlist(View):
    def get(self, request, product_id):
        customer_instance = Customer.objects.get(user=request.user)
        product_instance = Product.objects.get(id=product_id)
        try:
            WishList.objects.get(customer=customer_instance, product=product_instance)
            messages.error(request, 'Item Alredy Exist')
            return redirect('view_wishlist')
        except:
            WishList.objects.create(customer=customer_instance, product=product_instance)

            # WishList_instance = WishList.objects.get(customer=customer_instance, product=product_instance)
            # WishList_instance.delete()
            messages.success(request, 'Item Added To Wishlist')
            return redirect('view_wishlist')


def remove_from_cart(request, product_id):
    customer_instance = Customer.objects.get(user=request.user)
    Cart_product_instance = Cart.objects.get(customer=customer_instance, product=product_id)
    Cart_product_instance.delete()
    messages.success(request, 'Item Removed successfully')
    return redirect('view_cart')


def remove_from_wishlist(request, product_id):
    customer_instance = Customer.objects.get(user=request.user)
    WishList_product_instance = WishList.objects.get(customer=customer_instance, product=product_id)
    WishList_product_instance.delete()
    messages.success(request, 'Item Removed successfully')
    return redirect('view_wishlist')


class confirm_order(CreateView):
    model = Order
    template_name = 'product/confirm_order.html'
    form_class = confirm_order_form
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_instance = Customer.objects.get(user=self.request.user)
        context['products'] = Cart.objects.filter(customer=customer_instance)
        return context

    def post(self, request, *args, **kwargs):
        my_form = confirm_order_form(request.POST)
        if float(request.POST.get('total_amount')) > 20:
            if my_form.is_valid():
                my_form = my_form.save(commit=False)
                curr_cust = Customer.objects.get(user=self.request.user)
                my_form.customer = curr_cust
                my_form.total_amount = float(request.POST.get('total_amount'))
                my_form.save()
                for product in Cart.objects.filter(customer=curr_cust):
                    Invoice.objects.create(order=my_form, product=product.product,
                                           product_quantity=product.added_quantity)
                messages.success(request, "Order has been Placed Successfully")
                return redirect('home')
            else:
                messages.error(request, 'Order Has been failed')
                return redirect('home')
        else:
            messages.error(request, "Please Add Products to cart Firstly !")
            return redirect('view_cart')


class faviorite_brands(ListView):
    model = Product
    template_name = 'product/filter_items_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        try:
            fav_brands = Favourites.objects.filter(customer=Customer.objects.get(user=self.request.user))
            query_set = Product.objects.filter(brand=fav_brands[0].brand)
            for brand_obj in fav_brands[1:]:
                query_set |= Product.objects.get(brand=brand_obj.brand)
            return query_set
        except:
            return None


class SearchProduct(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(brand__brand_name__icontains=q) | Q(category__name__icontains=q)).distinct()
        return render(request, 'product/filter_items_page.html', {'products': products})


class FilterProduct(View):
    def get(self, request):
        min_price_range = request.GET.get('min_price_range') if request.GET.get('min_price_range') != '' else 0
        max_price_range = request.GET.get('max_price_range') if request.GET.get('max_price_range') != '' else Product.objects.order_by('-price').values_list('price', flat=True)[0]
        checked_brands = request.GET.getlist('size_checks')
        print(min_price_range)
        print(max_price_range)
        print(checked_brands)
        products = Product.objects.filter(price__gte=float(min_price_range),  price__lte = float(max_price_range))
        products |= Product.objects.filter(product_size__in = checked_brands)
        return render(request, 'product/filter_items_page.html', {'products': products})