from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.urls import reverse


class OrderItemInline(admin.TabularInline): # orderiteminline class created using tabularInline
    model = OrderItem
    raw_id_fields = ['product'] # we use our orderitem model to create a new field for id


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created',
                    'updated', order_detail, order_pdf] # a list display for the customer is created
    list_filter = ['paid', 'created', 'updated'] # a list filter is being created
    inlines = [OrderItemInline] # we include our OrderItemInline class as an inline. An inline allows you to include a model for appearing on the same edit page as the parent model.


admin.site.register(Order, OrderAdmin)