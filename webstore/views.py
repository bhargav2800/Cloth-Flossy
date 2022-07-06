from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import MyUserCreationForm,MyUserUpdateForm_customer,MyBrandUpdateForm_Brand,UserProfile_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Customer
from product.models import Brand,Favourites
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
def register_customer(request):
    """
    Display the registration Page and Register the customer.

    **Context**

    ``form_c``
        An Instance Form Of :model:`webstore.User`

    ``form_u``
        An Instance Form Of :model:`webstore.Customer`

    **Template:**

    :template:`webstore/register_customer.html`, ``
    """

    form_c = MyUserCreationForm()
    form_u = MyUserUpdateForm_customer()

    if request.method == 'POST':
        form_c = MyUserCreationForm(request.POST)
        form_u = MyUserUpdateForm_customer(request.POST)
        if form_c.is_valid() and form_u.is_valid():
            user_c = form_c.save(commit=False)  # We done this because We need to clean data and we get that user object...
            # user_c.username = user_c.username.lower()
            user_u = form_u.save(commit=False)
            user_u.user = user_c
            user_u.email = user_c.email
            user_c.save()
            user_u.save()
            login(request, user_c)  #login user
            messages.success(request, f'Your account has been created Successfully!')
            messages.success(request, f'You are logged In ')
            return redirect('home') # Redirect to home_page
        else:
            if form_c.errors:
                for i in form_c.errors.as_data():
                    messages.error(request, form_c.errors.as_data()[i][0].message)
            elif form_u.errors:
                for i in form_u.errors.as_data():
                    messages.error(request,form_u.errors.as_data()[i][0].message)
            else:
                messages.error(request, "Some Internal issue")

            # messages.error(request, form_u.brand_name.errors)
            return redirect('register-user')

    return render(request, 'webstore/register_customer.html', {'form_c':form_c, 'form_u':form_u})


def register_brand(request):
    """
        Display the registration Page For Brand and Register the brand.

        **Context**

        ``form_c``
            An Instance Form Of :model:`webstore.User`

        ``form_u``
            An Instance Form Of :model:`product.Brand.`

        **Template:**

        :template:`webstore/register_brand.html`
        """

    form_c = MyUserCreationForm()
    form_u = MyBrandUpdateForm_Brand()

    if request.method == 'POST':
        form_c = MyUserCreationForm(request.POST)
        form_u = MyBrandUpdateForm_Brand(request.POST)
        if form_c.is_valid() and form_u.is_valid():
            user_c = form_c.save(commit=False)  # We done this because We need to clean data and we get that user object...
            # user_c.username = user_c.username.lower()
            user_c.is_staff = True

            user_u = form_u.save(commit=False)
            user_u.user = user_c
            user_u.email = user_c.email
            user_c.save()
            my_group = Group.objects.get(name='brand_permission')
            my_group.user_set.add(user_c)
            user_u.save()
            login(request, user_c) # make login brand_Admin
            return redirect(reverse('admin:index')) # Redirect to admin panel
        else:
            if form_c.errors:
                for i in form_c.errors.as_data():
                    messages.error(request, form_c.errors.as_data()[i][0].message)
            elif form_u.errors:
                print(form_u.errors.as_json)
                for i in form_u.errors.as_data():
                    messages.error(request,form_u.errors.as_data()[i][0].message)
            else:
                messages.error(request, "Some Internal issue")

            return redirect('register-brand')

    return render(request, 'webstore/register_brand.html', {'form_c':form_c, 'form_u':form_u})


def loginPage(request):
    """
        Display the login Page For Customer and Allow the user to login after Ck=heck Credintials.

        **Context**

        **Template:**

        :template:`webstore/login_customer.html`
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User Does Not Exist !')
            return redirect('login-user')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid password!')
            return redirect('login-user')


    context = {}
    return render(request, 'webstore/login_customer.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login-user')
def user_profile(request):
    """
        Display the User Profile and Update the User Profile.

        **Context**

        ``form_u``
            An Instance Form Of :model:`webstore.Customer` for Update User Profile

        ``brands_lst``
            List of Available Brands

        ``brands_fav``
            List of Current User's Favorite Brands

        ``profile_url``
            Url of Current user's Profile Picture

        **Template:**

        :template:`webstore/user_profile.html`,
    """

    current_user = request.user
    current_user_info = Customer.objects.filter(user=current_user).first()
    form_u = UserProfile_Form(instance=current_user_info)
    brands_lst = Brand.objects.values_list('brand_name', flat=True)
    brands_fav = []
    for ins in Favourites.objects.filter(customer = current_user_info):
        brands_fav += [ins.brand.brand_name]
    if request.method == 'POST':
        Favourites.objects.filter(customer = current_user_info).delete()
        form_u = UserProfile_Form(request.POST, request.FILES, instance=current_user_info)
        fav_brand_lst = request.POST.getlist('fav_brand_select')
        for i in fav_brand_lst:
            Favourites.objects.create(customer = current_user_info, brand = Brand.objects.filter(brand_name=i).first())
        if form_u.is_valid():
            updated_email = form_u.cleaned_data['email']
            form_c = current_user
            form_c.email = updated_email
            form_c.save()
            form_u.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user-profile')
        else:
            if form_u.errors:
                for i in form_u.errors.as_data():
                    messages.error(request,form_u.errors.as_data()[i][0].message)
            else:
                messages.error(request, "Some Internal issue")
            return redirect('user-profile')

    return render(request, 'webstore/user_profile.html', {'form_u':form_u,'brands_lst':brands_lst,'brands_fav':brands_fav,'profile_url':current_user_info.avatar.url})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """
        Change the Current user's Password.

        **Context**

        **Template:**

        :template:`webstore/change_password.html`
    """

    template_name = 'webstore/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('user-profile')