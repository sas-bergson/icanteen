from django.template import loader

# Create your views here.
from django.http import HttpResponse


#slideshow    default view
def index(request):
    #prepare the models
    #        empty
    #prepare the template
    template = loader.get_template('slideshow/index.html')
    #prepare the context
    context = {}
    return HttpResponse(template.render(context, request))