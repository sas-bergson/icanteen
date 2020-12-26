from django.contrib import admin
from .models import Payment
import csv
from django.http import HttpResponse

def validate(modeladmin, request, queryset): #this function provides the possibility of validating multiple payments at a time.
    from django.core.mail import send_mail
    for payment in queryset:
        payment.processed = True
        if payment.email:
            send_mail('Payment Status for ' + payment.first_name + payment.last_name, 'Dear Customer, Your payment has been validated. Please send a reply indicating how you will want your products to be delivered.   THANK YOU', 'tamunang.courage@ictuniversity.org',[payment.email], fail_silently=False)
        else:
            modeladmin.message_user(request, "Mail sent successfully")
    payment.save() #payment is saved with its new status
validate.short_description = 'Validate selected payments'

def export_payments(modeladmin, request, queryset): #this function provides the possibility of exporting all/selected payments to an excel sheet
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Amount', 'Tel', 'Date Of Payment', 'Validated'])
    payments = queryset.values_list('id', 'first_name', 'last_name', 'email', 'amount', 'tel','payment_date', 'processed')
    for payment in payments:
        writer.writerow(payment)
    return response
export_payments.short_description = 'Export to csv'

class PaymentAdmin(admin.ModelAdmin):
        list_display = ['id', 'first_name', 'last_name', 'email', 'amount', 'tel', 'payment_date', 'processed']
        list_filter = ['first_name', 'processed', 'payment_date']
        ordering = ['-payment_date',]
        search_fields = ['email',]
        actions = [validate,export_payments,]

admin.site.register(Payment, PaymentAdmin,)
# Register your models here.
