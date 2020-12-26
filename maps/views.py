from django.http import HttpResponse
from django.shortcuts import render
from .forms import CustomerForm
from .models import Customer
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def Customer_details(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()

    form = CustomerForm()
    return render(request,'Customer_details.html', {'form':form})
def searchmenu(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')

        if query is not None:
            print('valid loop')
            form = SubmitForm(request.POST)
            results = Customer.objects.filter(Q(name__icontains = query) | Q(address__icontains = query))
            print(results)
            context={'results': results,
                     'submitbutton':submitbutton,'form':form}
            print(context)
            return render(request, 'maps/searchmenu.html', context)
        else:
            return render(request, 'maps/searchmenu.html')



