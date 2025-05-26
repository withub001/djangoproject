from django.shortcuts import render
from .models import Category, Product

# Create your views here.

def home_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products
    }

    return render(request, 'home.html', context)


def category_page(request, pk):

    chosen_category = Category.objects.get(id=pk)
    current_products = Product.objects.filter(product_category=chosen_category)


    context = {
        'category': chosen_category,
        'products': chosen_category
    }

    return render(request, 'category.html', context)

def product_page(request, pk):

    chosen_product = Product.objects.get(id=pk)

    context = {
        'product': chosen_product
    }

    return render(request, 'product.html', context)

