from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from ipware.ip import get_ip

from .models import Question, Choice, Ipcheck


def index(request):
    question_list = Question.objects.order_by('-pub_date')
    return render(request, 'voteapp/index.html', {'question_list': question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.active :
        return render(request, 'voteapp/detail.html', {'question': question})
    else :
        return render(request, 'voteapp/results.html', {
            'question': question,
            'message': 'Голосование закрыто.',
            })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'voteapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if question.active :
    #Проверка на повторное голосование по IP
        check = True
        new_ip=Ipcheck(check_ip=get_ip(request),question=question)

        count = Ipcheck.objects.filter(check_ip=new_ip.check_ip,question=new_ip.question).count()

        if count==0 :
            new_ip.save()
        else :
            check = False


        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'voteapp/detail.html', {
                'question': question,
                'error_message': "Вы не проголосовали.",
                })
        else:
            if check :
                selected_choice.votes += 1 #Повторный голос не будет учтен
                selected_choice.save()
                message = 'Спасибо. Ваш голос учтен.'
            else :
                message = 'Вы уже проголосовали.'

    else :
        message = 'Голосование закрыто.'

    return render(request, 'voteapp/results.html', {
        'question': question,
        'message': message,
        })
