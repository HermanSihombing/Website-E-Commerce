from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Category, Product, Reviewed
from cart.forms import CartAddProductForm
from .forms import ReviewedForm
import math


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    catname = "Product List"

    reviewed_product = Reviewed.objects.all()
    all_review = dict()
    all_rating = dict()

    count_review = 0
    count_star = 0
    for pro in products:
        for rev in reviewed_product:
            if pro.id == rev.product_id:
                count_review += 1
                count_star += int(rev.rating)
        all_review[pro.id] = count_review
        if count_review > 0:
            all_rating[pro.id] = math.floor(count_star / count_review)
        count_star = 0
        count_review = 0


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        catname = category.name
        products = products.filter(category=category)

    context = {
        'category' : categories,
        'catname' : catname,
        'products' : products,
        'review': all_review,
        'rating': all_rating,
    }

    return render(request, 'product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviewed_product = Reviewed.objects.filter(product=product)
    cart_product_form = CartAddProductForm()

    jlh_reviewed = reviewed_product.count()
    if jlh_reviewed == 0:
        rating_produk = 0
    else:
        jlh_rating = 0
        for produk in reviewed_product:
            jlh_rating += int(produk.rating)

        rating_produk = jlh_rating // jlh_reviewed

    if request.method == 'POST':
        reviewed_form = ReviewedForm(request.POST)
        if reviewed_form.is_valid():
            reviewed_form = Reviewed()
            reviewed_form.nama = request.user
            reviewed_form.product = product
            reviewed_form.rating = request.POST['rating']
            reviewed_form.comment = request.POST['comment']
            reviewed_form.save()
            reviewed_form = ReviewedForm()
    else:
        reviewed_form = ReviewedForm()

    context = {
        'product' : product,
        'reviewed_form':reviewed_form,
        'reviewed_product':reviewed_product,
        'rating_produk':rating_produk,
        'cart_product_form': cart_product_form,
    }

    return render(request, 'product/detail.html', context)