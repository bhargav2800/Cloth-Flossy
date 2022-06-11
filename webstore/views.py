from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import MyUserCreationForm,MyUserUpdateForm_customer,MyBrandUpdateForm_Brand
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, User,Customer
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.
def register_customer(request):
    form_c = MyUserCreationForm()
    form_u = MyUserUpdateForm_customer()

    if request.method == 'POST':
        form_c = MyUserCreationForm(request.POST)
        form_u = MyUserUpdateForm_customer(request.POST)
        if form_c.is_valid() and form_u.is_valid():
            user_c = form_c.save(commit=False)  # We done this because We need to clean data and we get that user object...
            user_c.username = user_c.username.lower()
            user_u = form_u.save(commit=False)
            user_u.user = user_c
            user_u.email = user_c.email
            user_c.save()
            user_u.save()
            login(request, user_c)  #login user
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('home') # Redirect to home_page
        else:
            messages.error(request, 'An error occured during registration')
            return redirect('register-user')

    return render(request, 'register_customer.html', {'form_c':form_c, 'form_u':form_u})


def register_brand(request):
    form_c = MyUserCreationForm()
    form_u = MyBrandUpdateForm_Brand()

    if request.method == 'POST':
        form_c = MyUserCreationForm(request.POST)
        form_u = MyBrandUpdateForm_Brand(request.POST)
        if form_c.is_valid() and form_u.is_valid():
            user_c = form_c.save(commit=False)  # We done this because We need to clean data and we get that user object...
            user_c.username = user_c.username.lower()
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
            messages.error(request, 'An error occured during registration')
            return redirect('register-brand')

    return render(request, 'register_brand.html', {'form_c':form_c, 'form_u':form_u})


def loginPage(request):
    # if request.user.is_authenticated:
    #     # return render(request, 'home')
    #     return HttpResponse("You Are On Home Page")

    if request.method == 'POST':
        email = request.POST.get('email').lower()
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
            messages.error(request, 'Invalid Username or password!')
            return redirect('login-user')


    context = {}
    return render(request, 'login_customer.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url='login-user')
def user_profile(request):
    current_user = request.user
    current_user_info = Customer.objects.filter(user=current_user).first()
    form_u = MyUserUpdateForm_customer(instance=current_user_info)


    if request.method == 'POST':
        form_u = MyUserUpdateForm_customer(request.POST, instance=current_user_info)
        if form_u.is_valid():
            updated_email = form_u.cleaned_data['email']
            form_c = current_user
            form_c.email = updated_email
            form_c.save()

            form_u.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user-profile')
        else:
            messages.error(request, 'Please Enter Valid input!')
            return redirect('user-profile')

    return render(request, 'user_profile.html', {'form_u':form_u})