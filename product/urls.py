from django.urls import path
from . import views

urlpatterns = [
    path('',views.home.as_view(), name="home"),
    path('product_details/<int:pk>/', views.Product_details.as_view(), name="product_details"),
    path('product_page/<str:category>/', views.product_page.as_view(), name="product_page"),
    path('target_audience/<str:target_audience>/', views.product_page.as_view(), name="target_audience"),
    path('cart/', views.view_cart.as_view(), name="view_cart"),
    path('wishlist/', views.view_wishlist.as_view(), name="view_wishlist"),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('add_to_wish/<str:product_id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name="remove_from_cart"),
    path('remove_from_wishlist/<int:product_id>', views.remove_from_wishlist, name="remove_from_wishlist"),
    path('confirm_order/', views.confirm_order.as_view(), name="confirm_order"),
]