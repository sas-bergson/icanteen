from django.contrib import admin
from django import forms
from .models import Product, Category

# Register your models here.

class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['designation', 'slug', 'created', 'last_updated', 'description', 'packaging', 'price', 'views', 'image']
    readonly_fields = ['created', 'last_updated', 'views']
    prepopulated_fields = {'slug': ('designation',)}

admin.site.register(Product, ProductAdmin)


class CategoryAdminForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'views', 'image']
    readonly_fields = ['created', 'last_updated']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
