from __future__ import unicode_literals

from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db import models
from decimal import Decimal
from .utils import unique_slug_factory

# Create your models here.

class Category(models.Model):
    # Fields
    # the id field is created by default as a surrogate key
    name = models.CharField(max_length=1024, null=False, unique=True, db_index=True)
    slug = models.SlugField(null=True, db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to= 'category/', max_length=1024,
        default = 'no-img.jpg')
    class Meta:
        ordering = ('-created', 'name')
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def title(self):
        return self.name

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
            #self.slug = slugify(self.name)
        # Creates a unique slug
        self.slug = slugify(unique_slug_factory(self))
        # call the mother class method to save the category
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery_category_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('gallery_category_update', args=(self.slug,))

    def __unicode__(self):
        return u'%s' % self.slug

    def __str__(self):
        return self.name

class Product(models.Model):
    # Fields
    designation = models.CharField(max_length=1024, null=False, db_index=True, unique=True)
    slug = models.SlugField(null=True, db_index=True, unique=True)
    description = models.TextField(blank=False, null=False)
    packaging = models.CharField(max_length=4096, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to= 'product/', max_length=1024,
        default = 'no-img.jpg')
    category = models.ForeignKey(Category, related_name= 'product', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created', 'designation')
        index_together = (('id', 'slug'),)

    @property
    def title(self):
        return self.designation

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
            #self.slug = slugify(self.name)
        self.slug = slugify(unique_slug_factory(self))
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery_product_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('gallery_product_update', args=(self.slug,))

    def __unicode__(self):
        return u'%s' % self.slug

    def __str__(self):
        return self.designation


class OrderItem(models.Model):
    # Fields
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    #order    = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    @property
    def product_name(self):
        return self.product

    #@property
    #def customer_name(self):
            #return self.customer
    @property
    #def order_code(self):
            #return self.order

    def get_absolute_url(self):
        return reverse('gallery_order_item_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('gallery_order_item_update', args=(self.slug,))

    def __unicode__(self):
        return u'%s' % self.slug

    def __str__(self):
        return self.designation
