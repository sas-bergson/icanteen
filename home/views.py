
from django.template import loader
from django.conf import settings

# Create your views here.
from django.http import HttpResponse


#home    default view
def index(request):
    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('home/index.html')
    print (settings.BASE_DIR)
    print (settings.STATIC_ROOT)
    print (settings.MEDIA_ROOT)
    #prepare the context
    context = {'request':request}
    return HttpResponse(template.render(context, request))

