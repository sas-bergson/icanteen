from django.shortcuts import render, get_object_or_404  #this will assist in rendering the template

# Create your views here.
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from .tasks import order_created

def order_create(request):   #this method is created to process the order
    cart = Cart(request)   # to obtain the cart from the current session using Cart
    if request.method == 'POST':   #to check wether the form is submitted using Post
        form = OrderCreateForm(request.POST)  #we create an instance of the form using Post
        if form.is_valid():
            order = form.save()  #create a variable order and save
            for item in cart:  # a loop is created inorder to looop through all items in the cart
                OrderItem.objects.create( #here we use the OrdelItem in the model to save items in the cart
                    order=order, #access the order instance
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear() #after saving the cart is cleared
            #tasks.order_created(order.id)
        return render(request, 'orders/order/created.html', {'order': order}) # a success page is rendered to show orders was received
    else:
        form = OrderCreateForm()  #if the request was a get we create the order form
    return render(request, 'orders/order/create.html', {'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order':order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response








