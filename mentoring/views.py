# -*- coding: utf-8 -*-
from django.shortcuts import redirect

from django.views.generic import UpdateView, DetailView

from mentoring.forms import *
from mentoring.models import Student, Placement

class PlacementUpdateView(UpdateView):
    model = Placement
    form_class = FormPlacement
    template_name = 'placement_todo_form.html'

    def get_context_placement(self, data=None, files=None, **kwargs):
        placement = self.get_placement()
        return {
            'placement_form': FormPlacement(data, files=files, instance=placement, prefix='placement_form'),
            'placement_company_form': FormCompany(data, parent=placement.workcompany,
                                                  instance=placement.workcompany.company,
                                                  prefix='placement_company_form'),
            'placement_company_formset': FormsetWorkCompany(data, instance=placement,
                                                            prefix='placement_company_formset'),
            'placement_contact_formset': FormsetWorkCompanyContactdata(data, instance=placement.workcompany,
                                                                       prefix='placement_contact_formset'),
        }

    def get(self, request, status=200, *args, **kwargs):
        self.object = self.get_object()

        if (request.GET.has_key('editMode')):
            self.object.finished = False
            self.object.save()
            return redirect('./')

        cd = self.get_context_data()
        cd.update(self.get_context_placement())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        if self.object.finished:
            return self.get(request, status=405)

        else:
            self.placement = self.get_context_placement(request.POST, files=request.FILES)

        form_target = request.POST.get('target_form').split(',') if request.POST.has_key('target_form') else [i for i, v
                                                                                                              in
                                                                                                              self.placement.iteritems()]
        status = 200

        for t in form_target:
            if self.placement.has_key(t) and self.placement.get(t).is_valid():
                self.placement.get(t).save()
            else:
                status = 400

        if status == 200:
            self.placement = self.get_context_placement()
        else:
            self.object.finished = False
            self.object.save()

        cd = self.get_context_data()
        cd.update(self.placement)
        return self.render_to_response(cd, status=status)

    def get_placement(self):
        return self.get_object()

    def get_success_url(self):
        return ''


class PlacementPreviewView(DetailView):
    model = Placement
    template_name = 'placement_preview.html'


class ThesisUpdateView(UpdateView):
    model = Thesis
    form_class = FormThesis
    template_name = 'thesis_todo_form.html'

    def get_context_thesis(self, data=None, files=None, **kwargs):
        thesis = self.get_thesis()
        return {
            'thesis_form': FormThesis(data, files=files, instance=thesis, prefix='thesis_form'),
            'thesis_company_form': FormCompany(data, parent=thesis.workcompany, instance=thesis.workcompany.company,
                                               prefix='thesis_company_form'),
            'thesis_company_formset': FormsetWorkCompany(data, instance=thesis, prefix='thesis_company_formset'),
            'thesis_contact_formset': FormsetWorkCompanyContactdata(data, instance=thesis.workcompany,
                                                                    prefix='thesis_contact_formset'),
            'thesis_mentoringrequest_form': FormMentoringRequest(data, instance=thesis.mentoring.tutor_1,
                                                                 prefix='thesis_mentoringrequest_form'), }

    def get(self, request, status=200, *args, **kwargs):
        self.object = self.get_object()

        if (request.GET.has_key('editMode')):
            self.object.finished = False
            self.object.save()
            return redirect('./')

        cd = self.get_context_data()
        cd.update(self.get_context_thesis())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        if self.object.finished:
            return self.get(request, status=405)

        else:
            self.thesis = self.get_context_thesis(request.POST, files=request.FILES)

        form_target = request.POST.get('target_form').split(',') if request.POST.has_key('target_form') else [i for i, v
                                                                                                              in
                                                                                                              self.thesis.iteritems()]
        status = 200

        for t in form_target:
            if self.thesis.has_key(t) and self.thesis.get(t).is_valid():
                self.thesis.get(t).save()
            else:
                status = 400

        if status == 200:
            self.thesis = self.get_context_thesis()
        else:
            self.object.finished = False
            self.object.save()

        cd = self.get_context_data()
        cd.update(self.thesis)
        return self.render_to_response(cd, status=status)

    def get_thesis(self):
        return self.get_object()

    def get_success_url(self):
        return ''


# class ThesisUpdateView(UpdateView):
#     model = Thesis
#     template_name = 'thesis_todo_form.html'
#     form_class = FormThesis
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         thesis = self.get_context_data_thesis(request.POST, files=request.FILES)
#         all_valid = True
#         if (thesis.get('thesis_form').is_valid()):
#             thesis.get('thesis_form').save()
#         else:
#             all_valid = False
#
#         if (thesis.get('thesis_contact_formset').is_valid()):
#             thesis.get('thesis_contact_formset').save()
#         else:
#             all_valid = False
#
#         if (thesis.get('thesis_company_formset').is_valid()):
#             thesis.get('thesis_company_formset').save()
#         else:
#             all_valid = False
#
#         if (thesis.get('thesis_mentoringrequest_form').is_valid()):
#             thesis.get('thesis_mentoringrequest_form').save()
#         else:
#             all_valid = False
#
#         company = thesis.get('thesis_company_form')
#         companywork = WorkCompany.objects.get(work=self.object)
#         company.instance = Company.objects.get_or_create(name=company['name'].value())[0]
#         companywork.company = company.instance
#         companywork.save()
#         """
#         Set mentoring request status to 'requested'
#         """
#         if (request.POST.has_key('finish') and all_valid):
#             self.object = self.get_object()
#             self.object.mentoring.tutor_1.status = 'RE'
#             self.object.mentoring.tutor_1.save()
#
#         return self.render_to_response(thesis)
#
#     def get_context_data_thesis(self, data=None, files=None, **kwargs):
#         thesis = self.get_thesis()
#         companywork = WorkCompany.objects.get(work=thesis)
#         thesis_form = FormThesis(data, files=files, instance=thesis, prefix='thesis_form')
#         thesis_company_form = FormCompany(data, instance=companywork.company, prefix='thesis_company_form')
#         thesis_company_formset = FormsetWorkCompany(data, instance=thesis, prefix='thesis_company_formset')
#         thesis_contact_formset = FormsetWorkCompanyContactdata(data, instance=companywork,
#                                                                prefix='thesis_contact_formset')
#         thesis_mentoringrequest_form = FormMentoringRequest(data, instance=thesis.mentoring.tutor_1,
#                                                             prefix='thesis_mentoringrequest_form')
#
#         return {
#             'thesis_form': thesis_form,
#             'thesis_company_form': thesis_company_form,
#             'thesis_company_formset': thesis_company_formset,
#             'thesis_contact_formset': thesis_contact_formset,
#             'thesis_mentoringrequest_form': thesis_mentoringrequest_form,
#         }
#
#     def get_context_data(self, **kwargs):
#         return self.get_context_data_thesis()
#
#     def get_thesis(self):
#         return self.get_object()
#
#     def get_success_url(self):
#         return ''


class StudentView(PlacementUpdateView, ThesisUpdateView):
    template_name = 'student_detail.html'
    model = Student

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        context.update(self.get_context_data_thesis())
        context.update(self.get_context_placement())
        return context

    def get_thesis(self):
        return self.get_object().thesis

    def get_placement(self):
        return self.get_object().placement

    def get_object(self, queryset=None):
        return Student.objects.get(user=self.request.user)


class TutorView(DetailView):
    model = Tutor
    template_name = 'tutor_detail.html'

    def get_object(self, queryset=None):
        return Tutor.objects.get(user=self.request.user)


class TutorRequestView(UpdateView):
    model = MentoringRequest
    template_name = 'tutor_request.html'
    form_class = FormTutorRequest

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.has_key('accept'):
            self.object.status = 'AC'
        elif request.POST.has_key('deny'):
            self.object.status = 'DE'
        else:
            self.form_invalid(self.get_form())
        self.object.save()
        return self.get(request)
