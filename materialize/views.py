# Create your views here.
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import *

from .forms.forms import *
from .models import *


class MaterialLoginView(TemplateView):
    template_name = 'materialize/material_login.html'


class MaterialFormView(FormView):
    template_name = 'material_form.html'
    form_class = MaterializeTestForm
    model = MaterializeTestModel

    def get_success_url(self):
        return ''


class MaterialFormsetView(FormView):
    template_name = 'material_todo_manual.html'
    form_class = MaterializeForeignForm
    model = MaterializeForeignModel

    def get_success_url(self):
        return ''

    def get_context_data(self, **kwargs):
        cd = super(MaterialFormsetView, self).get_context_data(**kwargs)
        cd['formset'] = MaterializeFormset()
        return cd


class MaterialFormManualView(MaterialFormsetView):
    template_name = 'material_form_manual.html'


class MaterialUpdateView(UpdateView):
    template_name = 'material_form.html'
    success_url = './'

    def form_invalid(self, form):
        return self.render_to_response(context=self.get_context_data(form=form), status=404)

    def form_invalid(self, form):
        return self.render_to_response(context=self.get_context_data(form=form), status=404)


class MaterialCreateView(CreateView):
    template_name = 'material_form.html'

    def get_form_action(self):
        return ''

    def form_valid(self, form):
        self.object = form.save()
        print self.object.pk
        js = serializers.serialize('json', [self.object, ])
        print(js)
        if self.request.is_ajax:
            return HttpResponse(js, content_type='application/json')
        else:
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(context=self.get_context_data(form=form), status=404)

    def get_context_data(self, **kwargs):
        cd = super(MaterialCreateView, self).get_context_data(**kwargs)
        cd['form_action'] = self.get_form_action()
        return cd
