from django.shortcuts import render,redirect
from django.db.models import Q
from orders.models import Order
from payments.models import Payment
from django.core.mail import send_mail
from django.conf import settings
from payments.forms import SubmitForm



#payments view
def makepayment(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')

        if query is not None:
            print('valid loop')
            form = SubmitForm(request.POST)
            results = Order.objects.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query) & Q(paid=False))
            print(results)
            context={'results': results,
                     'submitbutton':submitbutton,'form':form}
            print(context)
            return render(request, 'payments/makepayment.html', context)
        else:
            return render(request, 'payments/makepayment.html')
    else:
        if request.method == 'POST':
            form = SubmitForm(request.POST)

            if form is not None:
                post=Payment()
                post.first_name= request.POST.get('first_name')
                post.last_name= request.POST.get('last_name')
                post.email= request.POST.get('email')
                post.amount= request.POST.get('total')
                post.tel= request.POST.get('tel')
                post.delivery_date=request.POST.get('datepicker')
                post.save()
                subject = 'New Payment'
                message  = 'A validation request has been sent with the following information.Follow this link to validate it. "http://djangodevelopers.pythonanywhere.com/admin/payments/payment/?processed__exact=0"'+'  '+'Name:'+ post.first_name +' ' + post.last_name +'  '+ 'Email: '+ post.email +'  '+ 'Amount: ' + post.amount +'  ' + 'MoMo Contact: '+ post.tel +'  ' +'Delivery Date: ' + post.delivery_date
                from_email = settings.EMAIL_HOST_USER
                to_list = ['tcourage.tc@gmail.com']
                send_mail(
                           subject,message,from_email,to_list,fail_silently = True,
                           )
                return redirect('/payment/sucess/')
            else:
                form = SubmitForm()
        return render(request, 'payments/makepayment.html')


def payment(request):
    return render (request,'payments/paymentStatus.html',{})
def paymentStatus(request):
    payment_list = Payment.objects.all()
    return render (request,'payments/paymentStatus.html', {'payment':payment_list})

def sucess(request):
    return render (request,'payments/sucess.html')

# Create your views here.
