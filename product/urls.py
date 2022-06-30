from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('product_details/<int:pk>/', views.ProductDetails.as_view(), name="product_details"),
    path('product_sizes/', views.GetSize.as_view(), name="get_sizes"),
    path('product_details/<int:pk>/add_review/', views.ProductDetails.as_view(), name="add_review"),
    path('product_page/<str:category>/', views.ProductPage.as_view(), name="product_page"),
    path('target_audience/<str:target_audience>/', views.ProductPage.as_view(), name="target_audience"),
    path('cart/', views.ViewCart.as_view(), name="view_cart"),
    path('wishlist/', views.ViewWishlist.as_view(), name="view_wishlist"),
    path('add_to_cart/<int:product_id>/', views.AddToCart.as_view(), name="add_to_cart"),
    path('add_to_wish/<int:product_id>/', views.AddToWishlist.as_view(), name="add_to_wishlist"),
    path('remove_from_cart/<int:product_id>', views.RemoveFromCart, name="remove_from_cart"),
    path('remove_from_wishlist/<int:product_id>', views.RemoveFromWishlist, name="remove_from_wishlist"),
    path('confirm_order/', views.ConfirmOrder.as_view(), name="confirm_order"),
    path('cart/update', views.UpdateQuantity.as_view(), name="update_quantity"),
    path('faviorites/', views.FavioriteBrands.as_view(), name="faviorite_section"),
    path('searched_item/', views.SearchProduct.as_view(), name="searched_product"),
    path('filtered_item/', views.FilterProduct.as_view(), name="filter_product"),
    path('paymentHandler/', views.paymenthandler, name="PaytmentHandler"),
    path('view_orders/', views.ViewOrders.as_view(), name="ViewOrders"),
    path('view_order_details/<int:order_id>', views.ViewOrderDetails.as_view(), name="ViewOrderDetails"),
    path('invoice/<str:order_id>', views.GenerateInvoice.as_view(), name="GenerateInvoice"),
]