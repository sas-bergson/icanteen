from django.template import loader
from .models import Question

# Create your views here.
from django.http import HttpResponse


#polls    default view
def index(Request):
    # build data from the model
    question_list = Question.objects.order_by('-publication_date')
    #load the template
    template = loader.get_template('polls/index.html')
    #prepare the context
    context = {'question_list':question_list}
    #render the template
    return HttpResponse(template.render(context, Request))

#polls/detail  view showing details about a question
def detail(Request, question_id):
    question = Question.objects.get(pk = question_id)
    choice_list = question.choice_set.all()
    template = loader.get_template('polls/details.html')
    context = {'question':question, 'choice_list':choice_list }
    return HttpResponse(template.render(context, Request))

#polls/detail  view showing a question's results
def results(Request, question_id):
    return HttpResponse("<p>"\
                            "You're looking at the results of question %s."\
                        "</p>" % question_id)

#polls/detail  view showing a question's vote
def vote(Request, question_id):
    return HttpResponse("<p>"\
                            "You're voting on question %s."\
                        "</p>" % question_id)
