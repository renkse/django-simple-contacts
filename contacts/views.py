# coding=utf-8
__author__ = 'renkse'

from forms import FeedbackForm
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Contact, FeedbackMessage
from collections import OrderedDict
import json


def contacts_view(request):
    fbform = FeedbackForm()
    form_url = '/contacts/feedback/'
    contacts = Contact.objects.all()
    breadcrumbs = OrderedDict([
        ('Главная', '/'),
        ('Контакты', '')
    ])
    context = RequestContext(request, {
        'fbform': fbform,
        'contacts': contacts,
        'heading': 'Контакты',
        'breadcrumbs': breadcrumbs,
        'fbform_url': form_url
    })
    template = loader.get_template('contacts.html')
    return HttpResponse(template.render(context))


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('ok')
        else:
            errors = {}
            for key, value in form.errors.items():
                errors[key] = value[0]
            return HttpResponse(json.dumps(errors))