from django.shortcuts import redirect, render
from django.template.loader import get_template
from dotenv import load_dotenv
from .models import Product, Category, Cart, WishList, Order, Invoice, Favourites, Reviews, sub_products
from webstore.models import Customer
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib import messages
from .forms import confirm_order_form
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.sites.shortcuts import get_current_site
import razorpay
from io import BytesIO
from xhtml2pdf import pisa
from . import messages as msg
from datetime import datetime


# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'product/home.html'
    extra_context = {'best_selling': Product.objects.order_by('no_of_purchases')[:10]}


class ProductDetails(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product_detail.html'

    def post(self, request, *args, **kwargs):
        p_id = self.kwargs.get('pk')
        review_body = request.POST.get('review_field')
        Reviews.objects.create(customer=Customer.objects.get(user=self.request.user),
                               product=Product.objects.get(id=p_id), review=review_body)
        return redirect('product_details', pk=p_id)


class GetSize(View):
    def get(self, request, *args, **kwargs):
        color = request.GET['color']
        p_id = request.GET['p_id']
        context = {'color_wise_size': list(sub_products.objects.filter(product_id=p_id, color=color).values('size'))}
        return JsonResponse(context)


class ProductPage(ListView):
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


class UpdateQuantity(View):
    def post(self, request):
        pid = request.POST['pid']
        u_qua = request.POST['quantity']
        cart_obj = Cart.objects.get(customer=Customer.objects.get(user=self.request.user), product=pid)
        cart_obj.added_quantity = int(u_qua)
        cart_obj.save()
        product_quantity = sub_products.objects.get(id=pid).quantity
        print(product_quantity)
        if product_quantity == 0:
            product_message = "Out Of Stock"
        elif int(u_qua) > product_quantity:
            product_message = f"Only {product_quantity} Quantity Of Product Available !"
        else:
            product_message = ""

        return JsonResponse({'total': cart_obj.get_total, 'product_message': product_message}, safe=False)


class ViewCart(ListView):
    model = Cart
    template_name = 'product/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        customer_instance = Customer.objects.get(user=self.request.user)
        return Cart.objects.filter(customer=customer_instance)


class ViewWishlist(ListView):
    model = WishList
    template_name = 'product/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        customer_instance = Customer.objects.get(user=self.request.user)
        return WishList.objects.filter(customer=customer_instance)


class AddToCart(View):
    def post(self, request, product_id):
        # print(self.request.POST.)
        customer_instance = Customer.objects.get(user=request.user)
        color_select = self.request.POST.get('color_dropdown')
        size_select = self.request.POST.get('size_dropdown')
        product_instance = sub_products.objects.get(product=Product.objects.get(id=product_id), color=color_select,
                                                    size=size_select)

        try:
            Cart.objects.get(customer=customer_instance, product=product_instance)
            messages.error(request, )
            return redirect('home')
        except:
            Cart.objects.create(customer=customer_instance, product=product_instance, added_quantity=1)

            # WishList_instance = WishList.objects.get(customer=customer_instance, product=product_instance)
            # WishList_instance.delete()
            messages.success(request, msg.cart_Add)
            return redirect('home')


class AddToWishlist(View):
    def get(self, request, product_id):
        customer_instance = Customer.objects.get(user=request.user)
        product_instance = Product.objects.get(id=product_id)

        try:
            WishList.objects.get(customer=customer_instance, product=product_instance)
            messages.error(request, msg.already_in_cart)
            return redirect('view_wishlist')
        except:
            WishList.objects.create(customer=customer_instance, product=product_instance)

            # WishList_instance = WishList.objects.get(customer=customer_instance, product=product_instance)
            # WishList_instance.delete()
            messages.success(request, msg.wishlist_add)
            return redirect('view_wishlist')

    def post(self, request, product_id):
        customer_instance = Customer.objects.get(user=request.user)
        product_instance = Product.objects.get(id=product_id)

        try:
            WishList.objects.get(customer=customer_instance, product=product_instance)
            messages.error(request, msg.already_in_cart)
            return redirect('view_wishlist')
        except:
            WishList.objects.create(customer=customer_instance, product=product_instance)

            # WishList_instance = WishList.objects.get(customer=customer_instance, product=product_instance)
            # WishList_instance.delete()
            messages.success(request, msg.wishlist_add)
            return redirect('view_wishlist')


def RemoveFromCart(request, product_id):
    customer_instance = Customer.objects.get(user=request.user)
    Cart_product_instance = Cart.objects.get(customer=customer_instance, id=product_id)
    Cart_product_instance.delete()
    messages.success(request, msg.item_remove)
    return redirect('view_cart')


def RemoveFromWishlist(request, product_id):
    customer_instance = Customer.objects.get(user=request.user)
    WishList_product_instance = WishList.objects.get(customer=customer_instance, product=product_id)
    WishList_product_instance.delete()
    messages.success(request, msg.item_remove)
    return redirect('view_wishlist')


client = razorpay.Client(auth=(os.environ.get('RAZORPAY_API_KEY'), os.environ.get('RAZORPAY_API_SECRET_KEY')))


class ConfirmOrder(CreateView):
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
                if request.POST.get("COD"):
                    my_form = my_form.save(commit=False)
                    curr_cust = Customer.objects.get(user=self.request.user)
                    my_form.customer = curr_cust
                    my_form.total_amount = float(request.POST.get('total_amount'))
                    my_form.save()
                    orderid = my_form.id
                    for product in Cart.objects.filter(customer=curr_cust):
                        Invoice.objects.create(order=my_form, product=product.product,
                                               product_quantity=product.added_quantity,
                                               brand_name=product.product.product.brand,
                                               product_name=product.product.product.name,
                                               buy_price=product.product.product.discount_price(),
                                               product_discount=product.product.product.discount,
                                               product_size=product.product.size, product_color=product.product.color)
                        product_instance = sub_products.objects.get(id=product.product.id)
                        product_instance.quantity -= product.added_quantity
                        product_instance.save()

                    messages.success(request, msg.order_success)
                    return redirect('home')
                else:
                    my_form = my_form.save(commit=False)
                    curr_cust = Customer.objects.get(user=self.request.user)
                    my_form.customer = curr_cust
                    my_form.total_amount = float(request.POST.get('total_amount'))
                    my_form.save()
                    my_form.order_id = my_form.order_date.strftime('PAY2ME%Y%m%dODR') + str(my_form.id)
                    my_form.save()
                    orderid = my_form.id
                    for product in Cart.objects.filter(customer=curr_cust):
                        Invoice.objects.create(order=my_form, product=product.product,
                                               product_quantity=product.added_quantity,
                                               brand_name=product.product.product.brand,
                                               product_name=product.product.product.name,
                                               buy_price=product.product.product.discount_price(),
                                               product_discount=product.product.product.discount,
                                               product_size=product.product.size, product_color=product.product.color)

                    load_dotenv()
                    # RazorPay Payment
                    callback_url = 'http://' + str(get_current_site(request)) + "/paymentHandler/"
                    order_amount = float(request.POST.get('total_amount'))
                    order_currency = 'INR'
                    razorpay_order = client.order.create(
                        dict(amount=order_amount * 100, currency=order_currency, receipt=my_form.order_id,
                             payment_capture='0'))
                    my_form.razorpay_order_id = razorpay_order['id']
                    my_form.save()

                    return render(request, 'product/paymentsummary.html',
                                  {'order': my_form, 'order_id': razorpay_order['id'], 'orderId': my_form.order_id,
                                   'final_price': order_amount,
                                   'razorpay_merchant_id': os.environ.get('RAZORPAY_API_KEY'),
                                   'callback_url': callback_url, 'user_details': curr_cust})

            else:
                messages.error(request, msg.order_fail)
                return redirect('home')
        else:
            messages.error(request, msg.no_product_in_cart)
            return redirect('view_cart')


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {'razorpay_order_id': order_id, 'razorpay_payment_id': payment_id,
                           'razorpay_signature': signature}
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = client.utility.verify_payment_signature(params_dict)
            if result:
                amount = order_db.total_amount * 100  # we have to pass in paisa
                try:
                    client.payment.capture(payment_id, amount)
                    order_db.payment_status = 'SUCCESS'
                    order_db.save()
                    for product in Invoice.objects.filter(order=order_db):
                        product_instance = sub_products.objects.get(id=product.product.id)
                        product_instance.quantity -= product.product_quantity
                        product_instance.save()
                    return render(request, 'product/paymentsuccess.html')
                except:
                    order_db.payment_status = 'FAILURE'
                    order_db.save()
                    return render(request, 'product/paymentfailed.html')
            else:
                order_db.payment_status = 'FAILURE'
                order_db.save()
                return render(request, 'product/paymentfailed.html')
        except:
            return HttpResponse("505 not found")


class FavioriteBrands(ListView):
    model = Product
    template_name = 'product/filter_items_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        try:
            fav_brands = Favourites.objects.filter(customer=Customer.objects.get(user=self.request.user))
            query_set = Product.objects.filter(brand=fav_brands[0].brand)
            for brand_obj in fav_brands[1:]:
                query_set |= Product.objects.get(brand=brand_obj.brand)
            return query_set.distinct('name')
        except:
            return None


class SearchProduct(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        products = Product.objects.filter(
            Q(name__icontains=q) | Q(short_line__icontains=q) | Q(brand__brand_name__icontains=q) | Q(
                category__name__icontains=q))
        return render(request, 'product/filter_items_page.html', {'products': products})


class FilterProduct(View):
    def get(self, request):
        min_price_range = request.GET.get('min_price_range') if request.GET.get('min_price_range') != '' else 0
        max_price_range = request.GET.get('max_price_range') if request.GET.get('max_price_range') != '' else \
        Product.objects.order_by('-price').values_list('price', flat=True)[0]
        checked_brands = request.GET.getlist('size_checks')
        products = Product.objects.filter(price__gte=float(min_price_range), price__lte=float(max_price_range))
        # products |= Product.objects.filter(product_size__in = checked_brands).distinct('name')
        return render(request, 'product/filter_items_page.html', {'products': products})


class ViewOrders(ListView):
    def get(self, request):
        Orders = Order.objects.filter(customer__user=request.user)
        return render(request, 'product/order_history.html', {'orders': Orders})


class ViewOrderDetails(ListView):
    def get(self, request, order_id):
        Products = Invoice.objects.filter(order__id=order_id)
        return render(request, 'product/order_history_details.html', {'products': Products})


def RenderToPdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)  # , link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GenerateInvoice(View):
    def get(self, request, order_id):
        order = Order.objects.get(order_id=order_id, customer__user=request.user)
        data = {'order_id': order.order_id, 'transaction_id': order.razorpay_payment_id,
                'user_email': order.customer.email, 'date': str(order.order_date), 'name': order.customer.name,
                'order': order, 'amount': order.total_amount, 'payment_method': order.payment_method,
                'payment_status': order.payment_status, }
        pdf = RenderToPdf('product/invoice.html', data)
        # return HttpResponse(pdf, content_type='application/pdf')

        # # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % (data['order_id'])
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class ReplaceReturn(View):
    def get(self,request, pid, purpose):
        if purpose == 'return':
            return render(request, 'product/return.html', {})
        else:
            product_instance = Invoice.objects.get(id=pid).product
            return render(request, 'product/replace.html', {'product':Product.objects.get(id=product_instance.product.id)})

    def post(self, request, pid, purpose):
        if purpose == 'return':
            product_obj = Invoice.objects.get(id=pid)
            product_obj.returned_status = True
            product_obj.returned_date = datetime.now()
            product_obj.returned_reason = request.POST.get('return_tab')
            product_obj.save()
            return redirect('ViewOrders')
        else:
            product_obj = Invoice.objects.get(id=pid)
            product_obj.replaced_status = True
            product_obj.replaced_date = datetime.now()
            product_obj.replacement_reason = request.POST.get('return_tab')
            product_obj.replace_product_size = request.POST.get('size_dropdown')
            product_obj.replace_product_color = request.POST.get('color_dropdown')
            product_obj.save()
            return redirect('ViewOrders')


class ReplaceReturnStatus(View):
    def get(self, request, pid, purpose):
        if purpose == 'return':
            return render(request, 'product/returnstatus.html', {'product': Invoice.objects.get(id=pid)})
        else:
            return render(request, 'product/replacestatus.html', {'product': Invoice.objects.get(id=pid)})