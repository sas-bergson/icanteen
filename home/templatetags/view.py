from django.template import Library, Node, TemplateSyntaxError, Variable
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.urls import resolve

register = Library()

def do_view(parser, token):
    print ('\n Parsing ViewNode Tenplate tag for parameters')	
    args = []
    kwargs = {}
    try:
    	# split the template tags
    	tokens = token.split_contents()
    except ValueError:
        raise (TemplateSyntaxError, ("%r tag requires one or more arguments" %
                                    token.contents.split()[0]))
    tag_name = tokens.pop(0) # remove the tag_name
    url_or_view = tokens.pop(0) # remove the url_or_view
    print ('\ntag_name = '+tag_name)
    print ('\nurl_or_view = '+url_or_view)
    # extract args as list or kwargs as a dictionnary
    for token in tokens:
        equals = token.find("=")
        if equals == -1:
            args.append(token)
        else:
            kwargs[str(token[:equals])] = token[equals+1:]
    print ("\n args = ")
    print (', '.join(args))
    print ("\n kwargs = ")
    print ("%s" % str (kwargs))
    
    return ViewNode(url_or_view[1:-1], args, kwargs)

register.tag('view', do_view)

class ViewNode(Node):

	def __init__(self, url_or_view, args, kwargs):
		print ('\n Initialising ViewNode Tenplate tag with parameters')
		self.url_or_view = url_or_view
		self.args = args
		self.kwargs = kwargs

	def render(self, context):
		print ('\n Rendering ViewNode Template tag')
		
		try: 
			view, args, kwargs = resolve(self.url_or_view)
		except Http404:		
			view = self.url_or_view
			args = [Variable(arg).resolve(context) for arg in self.args]
			kwargs = {}
			for key, value in self.kwargs.items():
				kwargs[key] = Variable(value).resolve(context)
		
		print ("\n args = ")
		print (', '.join(args))
		print ("\n kwargs = ")
		print ("%s" % str (kwargs))
		
		try:
			response = view(context['request'], *args, **kwargs)
			#print (response.content.decode())
			return response.content.decode()
		except Http404:
			raise (TemplateSyntaxError, ("%r is not callable" % view))
			
