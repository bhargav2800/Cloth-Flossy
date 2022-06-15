from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'product/home.html', context)

def Product_details(request):
    return render(request, 'product/filter_items_page.html')