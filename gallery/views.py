import os
from PIL import Image
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from cart.forms import CartAddProductForm
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.template import loader
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.http import HttpResponse


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
def thumbnail(request, img_url):

    print("Hello")
    print(img_url)

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail.html')
    url_raw_split = img_url.split('/')
    own_img_url = 'product/' + url_raw_split[1]

    #build the thumbnail if it does not exist
    url_split = own_img_url.split('.')
    img_thumb_url = url_split[0] + '_thumb.'+ url_split[1]

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([300, 300])
            if (img_thumb.size[0]<300) or (img_thumb.size[1]<300):
                offsetH = (300 - img_thumb.size[0])//2
                offsetW = (300 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_url':img_url, 'url_raw_0':url_raw_split[0],'url_raw_1':url_raw_split[1],
              'own_img_url':own_img_url,'img_thumb_url':img_thumb_url,'thumb_status':thumb_status,
              'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))


def CartProduct_detail(request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug, available=True)
        cart_product_form = CartAddProductForm()
        context = {
            'product': product,
            'cart_product_form': cart_product_form
        }
        return render(request, 'gallery/product_detail.html', context)


#class ProductListView(ListView):
#    model = Product
#    paginate_by = 10



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context



class ProductDetailView(DetailView):
    model = Product
    paginate_by = 4



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



def ExtraLargeThumb(request, img_extralarge):

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail_extra_large.html')

    #creating image thumbnail
    print("Hello")
    print(img_extralarge)

    url_raw_split = img_extralarge.split('_')
    own_img_url = url_raw_split[0] + '.jpg'

    img_extralarge = img_extralarge.split('/')
    img_extralarge_thumb_url1 = img_extralarge[0] + '/' + img_extralarge[2]

    #print(own_img_url)
    #img_extralarge_split = own_img_url.split('.')
    #img_extralarge_thumb_url = img_extralarge_split[0] + '_extralargethumb.' + img_extralarge_split[1]
    #img_extralarge_thumb_url_split = img_extralarge_thumb_url.split('/')
    #img_extralarge_thumb_url1 = img_extralarge_thumb_url_split[0] + '/' + img_extralarge_thumb_url_split[2]
    #print("helloooo2")
    #print(img_extralarge_thumb_url1)

    #print("helloooooooooooo3")
    #print(img_extralarge_thumb_url)

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_extralarge_thumb_url1),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb_extralarge5.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,own_img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([500, 500])
            if (img_thumb.size[0]<500) or (img_thumb.size[1]<500):
                offsetH = (500 - img_thumb.size[0])//2
                offsetW = (500 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_extralarge_thumb_url1), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_extralarge':img_extralarge,'img_extralarge_thumb_url1':img_extralarge_thumb_url1,'own_img_url':own_img_url,
               'thumb_status':thumb_status,'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))


def LargeThumb(request, img_large):

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail_large.html')

    #creating image thumbnail
    print("Hello")
    print(img_large)

    url_raw_split = img_large.split('_')

    own_img_url = url_raw_split[0] + '.jpg'
    print("Hello2")
    print(own_img_url)

    #img_large = img_large.split('/')
    #img_large_thumb_url1 = img_large[0] + '/' + img_large[2]



    img_large_split = own_img_url.split('.')
    img_large_thumb_url = img_large_split[0] + '_largethumb.' + img_large_split[1]

    print("helloooooooooooo3")
    print(img_large_thumb_url)

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_large_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb_extralarge4.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,own_img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([400, 400])
            if (img_thumb.size[0]<400) or (img_thumb.size[1]<400):
                offsetH = (400 - img_thumb.size[0])//2
                offsetW = (400 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_large_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_large':img_large,'img_large_thumb_url':img_large_thumb_url,'own_img_url':own_img_url,
               'thumb_status':thumb_status,'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))




def MediumThumb(request, img_medium):

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail_medium.html')

    #creating image thumbnail
    print("Hello")
    print(img_medium)

    url_raw_split = img_medium.split('_')
    own_img_url = url_raw_split[0] + '.jpg'

    img_medium = img_medium.split('/')
    img_medium_thumb_url1 = img_medium[0] + '/' + img_medium[2]

    #print(own_img_url)
    #img_extralarge_split = own_img_url.split('.')
    #img_extralarge_thumb_url = img_extralarge_split[0] + '_extralargethumb.' + img_extralarge_split[1]
    #img_extralarge_thumb_url_split = img_extralarge_thumb_url.split('/')
    #img_extralarge_thumb_url1 = img_extralarge_thumb_url_split[0] + '/' + img_extralarge_thumb_url_split[2]
    #print("helloooo2")
    #print(img_extralarge_thumb_url1)

    #print("helloooooooooooo3")
    #print(img_extralarge_thumb_url)

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_medium_thumb_url1),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb_extralarge5.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,own_img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([500, 500])
            if (img_thumb.size[0]<500) or (img_thumb.size[1]<500):
                offsetH = (500 - img_thumb.size[0])//2
                offsetW = (500 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_medium_thumb_url1), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_medium':img_medium,'img_medium_thumb_url1':img_medium_thumb_url1,'own_img_url':own_img_url,
               'thumb_status':thumb_status,'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))


def SmallThumb(request, img_small):

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail_small.html')

    #creating image thumbnail
    print("Hello")
    print(img_small)

    url_raw_split = img_small.split('_')
    own_img_url = url_raw_split[0] + '.jpg'

    img_small = img_small.split('/')
    img_small_thumb_url1 = img_small[0] + '/' + img_small[2]

    #print(own_img_url)
    #img_extralarge_split = own_img_url.split('.')
    #img_extralarge_thumb_url = img_extralarge_split[0] + '_extralargethumb.' + img_extralarge_split[1]
    #img_extralarge_thumb_url_split = img_extralarge_thumb_url.split('/')
    #img_extralarge_thumb_url1 = img_extralarge_thumb_url_split[0] + '/' + img_extralarge_thumb_url_split[2]
    #print("helloooo2")
    #print(img_extralarge_thumb_url1)

    #print("helloooooooooooo3")
    #print(img_extralarge_thumb_url)

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_small_thumb_url1),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb_extralarge5.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,own_img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([500, 500])
            if (img_thumb.size[0]<500) or (img_thumb.size[1]<500):
                offsetH = (500 - img_thumb.size[0])//2
                offsetW = (500 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_small_thumb_url1), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_small':img_small,'img_small_thumb_url1':img_small_thumb_url1,'own_img_url':own_img_url,
               'thumb_status':thumb_status,'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))


def ListThumb(request, img_url):

    print("Hello")
    print(img_url)

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail.html')
    url_raw_split = img_url.split('/')
    own_img_url = 'product/' + url_raw_split[1]

    #build the thumbnail if it does not exist
    url_split = own_img_url.split('.')
    img_thumb_url = url_split[0] + '_thumb.'+ url_split[1]

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([300, 300])
            if (img_thumb.size[0]<300) or (img_thumb.size[1]<300):
                offsetH = (300 - img_thumb.size[0])//2
                offsetW = (300 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_url':img_url, 'url_raw_0':url_raw_split[0],'url_raw_1':url_raw_split[1],
              'own_img_url':own_img_url,'img_thumb_url':img_thumb_url,'thumb_status':thumb_status,
              'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))



def DetailThumb(request, img_url):

    print("Hello")
    print(img_url)

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail.html')
    url_raw_split = img_url.split('/')
    own_img_url = 'product/' + url_raw_split[1]

    #build the thumbnail if it does not exist
    url_split = own_img_url.split('.')
    img_thumb_url = url_split[0] + '_thumb.'+ url_split[1]

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([300, 300])
            if (img_thumb.size[0]<300) or (img_thumb.size[1]<300):
                offsetH = (300 - img_thumb.size[0])//2
                offsetW = (300 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_url':img_url, 'url_raw_0':url_raw_split[0],'url_raw_1':url_raw_split[1],
              'own_img_url':own_img_url,'img_thumb_url':img_thumb_url,'thumb_status':thumb_status,
              'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))



def TileThumb(request, img_url):

    print("Hello")
    print(img_url)

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail.html')
    url_raw_split = img_url.split('/')
    own_img_url = 'product/' + url_raw_split[1]

    #build the thumbnail if it does not exist
    url_split = own_img_url.split('.')
    img_thumb_url = url_split[0] + '_thumb.'+ url_split[1]

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([300, 300])
            if (img_thumb.size[0]<300) or (img_thumb.size[1]<300):
                offsetH = (300 - img_thumb.size[0])//2
                offsetW = (300 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_url':img_url, 'url_raw_0':url_raw_split[0],'url_raw_1':url_raw_split[1],
              'own_img_url':own_img_url,'img_thumb_url':img_thumb_url,'thumb_status':thumb_status,
              'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))



def ContentThumb(request, img_url):

    print("Hello")
    print(img_url)

    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('gallery/thumbnail.html')
    url_raw_split = img_url.split('/')
    own_img_url = 'product/' + url_raw_split[1]

    #build the thumbnail if it does not exist
    url_split = own_img_url.split('.')
    img_thumb_url = url_split[0] + '_thumb.'+ url_split[1]

    try:
        fd_img = open(os.path.join(settings.MEDIA_ROOT,img_thumb_url),'rb')
        fd_img.close()
        thumb_status = 'Thumb File was Found'
    except FileNotFoundError:
        try:
            fd_back = open(os.path.join(settings.MEDIA_ROOT,'transparent_thumb.jpg'), 'rb')
            fd_img = open(os.path.join(settings.MEDIA_ROOT,img_url),'rb')
            img_thumb = Image.open(fd_img)
            back_thumb = Image.open(fd_back)
            img_thumb.thumbnail([300, 300])
            if (img_thumb.size[0]<300) or (img_thumb.size[1]<300):
                offsetH = (300 - img_thumb.size[0])//2
                offsetW = (300 - img_thumb.size[1])//2
                box = (offsetH, offsetW, img_thumb.size[0]+offsetH, img_thumb.size[1]+offsetW)
                back_thumb.paste(img_thumb, box)
                img_thumb = back_thumb
            img_thumb.save(os.path.join(settings.MEDIA_ROOT,img_thumb_url), img_thumb.format)
            thumb_status = 'Thumb File was not Found but built'
        except FileNotFoundError:
            thumb_status = 'Thumb File was not Found but built lead to failure'

        #prepare the context
    context = {'request':request,'img_url':img_url, 'url_raw_0':url_raw_split[0],'url_raw_1':url_raw_split[1],
              'own_img_url':own_img_url,'img_thumb_url':img_thumb_url,'thumb_status':thumb_status,
              'media_root':settings.MEDIA_ROOT,'media_url':settings.MEDIA_URL}

    return HttpResponse(template.render(context, request))


def ExtraLargeView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_extralarge_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})



def LargeView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_large_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})

def MediumView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 6)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_medium_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})

def SmallView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 8)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_small_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})


def ListView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_list_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})


def DetailView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_detail_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})


def TileView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_tile_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})


def ContentView(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Product.objects.order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 4)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

    return render(request,'gallery/product_content_list.html',
                              {'category': category,
                               'categories': categories,
                               'object_list':object_list})



def ProductList(request, category_slug=None):

        category = None
        categories = Category.objects.all()
        object_list = Product.objects.order_by('-created')
        cart_product_form = CartAddProductForm()


        page = request.GET.get('page', 1)
        paginator = Paginator(object_list, 8)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)


        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            object_list = Product.objects.filter(category=category)

        return render(request,'gallery/product_list.html',
                              {'category': category,
                               'categories': categories,
                               'cart_product_form': cart_product_form,
                               'object_list':object_list})


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
