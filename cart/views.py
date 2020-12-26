from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST    # to post the form
from gallery.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from pprint import pprint
# Create your views here.
@require_POST # this is to ensure that only post request are allowed
def cart_add(request, product_id):    #a method to add items to the cart
    cart = Cart(request)  # create a new cart object passing it the request object
    product = get_object_or_404(Product, id=product_id)   # product is gotten from the database using the product id
    form = CartAddProductForm(request.POST)
    #id = request.POST.get("id")
    #quantity = request.POST.get("quantity")
    print(request)
    print(request.POST)
    if form.is_valid():   #if the form is validated products are added to cart and then updated
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')  # cart redirected to cart detail page


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):  #method to display the cart detail page
    cart = Cart(request)
    pprint(vars(cart))
    products = []
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        products.append(item)
    context = { 'cart': cart }
    context['products'] = products
    return render(request, 'cart/detail.html', context)

#def cart_detail(request):
    #cart = Cart(request)
    #products = []
    #for item in cart:
        #item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        #products.append(item)
    #context = { 'cart': cart }
    #context['products'] = products
    #return render(request, 'cart/detail.html', context)

