from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice, Earphone

# Create views through generic views here.
class ListEarphonesView(generic.ListView):
    template_name = 'firstapp/list_earphones.html'
    model = Earphone

def SearchForEarphones(request, earphone_feature):
    query_string = request.GET.get("query-string", False)
    earphone_type = request.GET.get("earphone-type", False)
    earphones_list = Earphone.objects.all()

    # search for names, brands
    if query_string:
        earphones_list = Earphone.objects.filter(earphone_name__search=query_string)

    # search for types
    if earphone_type:
        earphones_list = earphones_list.filter(earphone_type__search=earphone_type)

    # search for features
    if earphone_feature:
        earphones_list = earphones_list.filter(earphone_features__contains=[earphone_feature])

    context = {
        'query_string': query_string,
        'earphone_type': earphone_type,
        'earphone_feature': earphone_feature,
        'earphones_list': earphones_list,
    }

    return render(request, 'firstapp/search_for_earphones.html', context)

class IndexView(generic.ListView):
    template_name = 'firstapp/index.html'
    model = Question

    # change the object name of context
    # from default 'object_list' to 'latest_question_list'
    # context_object_name = 'latest_question_list'

    # By default, get_queryset() returns the value of the 'queryset' attribute
    # if it is set, otherwise it constructs a QuerySet
    # by calling the all() method on the model attribute's default manager.
    #
    # 'queryset': A QuerySet that represents the objects. If provided,
    # the value of queryset supersedes the value provided for model.
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'firstapp/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'firstapp/results.html'

# Create your views here.

# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return render(request, 'firstapp/index.html', context)

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'firstapp/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'firstapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # choice_set: choice_set is a RelatedManager which can create querysets of Choice objects which relate to the Question instance, e.g. q.choice_set.all()
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'firstapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        # save() when INSERT or UPDATE the database
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('firstapp:results', args=(question.id,)))
