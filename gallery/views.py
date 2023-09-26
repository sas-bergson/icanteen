
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import (
    Paginator, 
    EmptyPage, 
    PageNotAnInteger
)
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import (
    DetailView, 
    ListView, 
    UpdateView, 
    CreateView
)
from django.views.generic.base import TemplateView
import os
from PIL import Image
import re

from .forms import ProductForm, CategoryForm
from .models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.

#gallery    default view
def index(request):
    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/index.html')
    #prepare the context
    return HttpResponse(template.render(context, request))

def search(request):
    query = request.GET.get('q')
    if query:
        object_list = Product.objects.filter(Q(designation__icontains = query) | Q(description__icontains = query))

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 8)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return render(request,'gallery/product_list.html',
                              {'object_list' : object_list,
                              'query' : query})

#gallery/wall/   view
def wall(request):
    # build data from the model
    object_list = Category.objects.order_by('-created')
    #prepare the template
    template = template = loader.get_template('gallery/wall.html')
    #prepare the context
    context = {'object_list':object_list}
    return HttpResponse(template.render(context, request))

#gallery/thumbnail/   view
def get_thumb_size(t_size='sm'):
    if (t_size == 'sm'):
        return 200
    if (t_size == 'md'):
        return 400
    if (t_size == 'lg'):
        return 500
    if (t_size == 'xl'):
        return 600
    return 300

def get_thumbnail(img_url, thumb_bg, t_size='sm'):
    url_split = img_url.split('/')
    img_url = 'product/'+url_split[len(url_split) - 1]
    #build the thumbnail if it does not exist
    url_split = img_url.split('.')
    thumb_url = url_split[0] + '_thumb.'+ url_split[1]
    thumb_size = get_thumb_size(t_size)
    print(f"thumb_url_ = {thumb_url} | thumb_size = {thumb_size}")
    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb file was Found'
    except FileNotFoundError:
        try:
            url_split = re.split('_'+t_size+'.',img_url)
            print(f"url_split = {url_split}")
            if (len(url_split) > 1):
                img_url = url_split[0]+'.'+url_split[1]
            print(f"img_source = {img_url}")
            fd_back = open(os.path.join(settings.MEDIA_ROOT, thumb_bg), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT, img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([thumb_size, thumb_size])
            if (img_thumb.size[0]<thumb_size) or (img_thumb.size[1]<thumb_size):
                offsetH = (thumb_size - img_thumb.size[0])//2
                offsetW = (thumb_size - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,thumb_url), img_thumb.format)
            thumb_status = 'Thumb file was not found and built was successful'
        except FileNotFoundError:
            thumb_status = 'Thumb file was not found and built failed'
    #prepare the context
    thumbnail_data = {
        'img_url':img_url,
        'alt_url':'no-img.jpg', 
        'thumb_url':thumb_url,
        'thumb_size':thumb_size,
        'thumb_status':thumb_status,
    }

    return thumbnail_data


def CartProduct_detail(request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        cart_product_form = CartAddProductForm()
        context = {
            'product': product,
            'cart_product_form': cart_product_form
        }
        return render(request, 'gallery/product_detail.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request,
                  'shop/product/detail.html',
                  context)
                  #{'product': product}


class ThumbnailView(TemplateView):
    template_name = 'gallery/thumbnail.html'
    thumb_bg_template = 'transparent_thumb.jpg'
    t_size = 'default'

    def get(self, *args, **kwargs):
        if "img_url" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'img_url' parameter."
            )
        img_url = kwargs.get('img_url', None)
        print(f"img_url = {img_url}")
        thumb_data = get_thumbnail(img_url, self.thumb_bg_template, self.t_size)
        self.extra_context = {
            'img_url':thumb_data['img_url'],
            'alt_url':thumb_data['alt_url'],
            'thumb_url':thumb_data['thumb_url'],
            'thumb_size':thumb_data['thumb_size'],
            'thumb_status':thumb_data['thumb_status'],
            'media_root':settings.MEDIA_ROOT,
            'media_url':settings.MEDIA_URL
        }

        return super().get(*args, **kwargs)


class SmallThumbnailView(ThumbnailView):
    thumb_bg_template = 'transparent_sm_thumb.jpg'
    t_size = 'sm'


class MediumThumbnailView(ThumbnailView):
    thumb_bg_template = 'transparent_md_thumb.jpg'
    t_size = 'md'


class LargeThumbnailView(ThumbnailView):
    thumb_bg_template = 'transparent_lg_thumb.jpg'
    t_size = 'lg'


class ExtraLargeThumbnailView(ThumbnailView):
    thumb_bg_template = 'transparent_xl_thumb.jpg'
    t_size = 'xl'


class ProductListView(TemplateView):
    template_name = 'gallery/product_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 8)

    def get(self, *args, **kwargs):
        
        category = None
        categories = Category.objects.all()
        cart_product_form = CartAddProductForm()

        page = self.request.GET.get('page', 1)
        try:
            object_list = self.paginator.page(page)
        except PageNotAnInteger:
            object_list = self.paginator.page(1)
        except EmptyPage:
            object_list = self.paginator.page(self.paginator.num_pages)

        category_slug = kwargs.get('category_slug', None)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

        self.extra_context = {
            'category': category,
            'categories': categories,
            'cart_product_form': cart_product_form,
            'object_list':object_list
        }
        return super().get(*args, **kwargs)


# display list with small-size thumbnails allowing for pagination of 12 items per page
class ProductListSmallView(ProductListView):
    template_name = 'gallery/product_small_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 12)


# display list with medium-size thumbnails allowing for pagination of 06 items per page
class ProductListMediumView(ProductListView):
    template_name = 'gallery/product_medium_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 6)


# display list with large-size thumbnails allowing for pagination of 04 items per page
class ProductListLargeView(ProductListView):
    template_name = 'gallery/product_large_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 4)


# display list with extra-large-size thumbnails allowing for pagination of 02 items per page
class ProductListExtraLargeView(ProductListView):
    template_name = 'gallery/product_extralarge_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 2)


# display list with large-size thumbnails and extra few details 
# allowing for pagination of 04 items per page
class ProductListListView(ProductListView):
    template_name = 'gallery/product_list_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 4)


class ProductListDetailView(ProductListView):
    template_name = 'gallery/product_list_detail.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 4)


class ProductListTileView(ProductListView):
    template_name = 'gallery/product_tile_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 4)


class ProductListContentView(ProductListView):
    template_name = 'gallery/product_content_list.html'
    object_list = Product.objects.order_by('-created')
    paginator = Paginator(object_list, 4)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context


class ProductDetailView(DetailView):
    model = Product
    # paginate_by = 4


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm


class CategoryListView(ListView):
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm


class CategoryDetailView(DetailView):
    model = Category


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
