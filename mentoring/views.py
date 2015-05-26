# Create your views here.

from django.views.generic import TemplateView, UpdateView, DetailView

from mentoring.forms import *
from mentoring.models import Student, Placement


class StudentOverviewView(TemplateView):
    template_name = 'student_overview.html'

    def get_context_data(self, **kwargs):
        cd = super(StudentOverviewView, self).get_context_data()
        cd['form_thesis_registration'] = FormThesisInvitation()
        cd['form_thesis_finalization'] = FormThesisFinalization()
        cd['form_placement'] = FormPlacement()

        return cd


class PlacementUpdateView(UpdateView):
    model = Placement
    form_class = FormPlacement
    template_name = 'placement_todo_form.html'

    def get_context_data_placement(self, data=None, files=None, **kwargs):
        placement = self.get_placement()
        companywork = WorkCompany.objects.get(work=placement)
        self.get_form(self.form_class)
        placement_form = FormPlacement(data, files=files, instance=placement, prefix='placement_form')
        placement_company_form = FormCompany(data, instance=companywork.company, prefix='placement_company_form')
        placement_company_formset = FormsetWorkCompany(data, instance=placement, prefix='placement_company_formset')
        placement_contact_formset = FormsetWorkCompanyContactdata(data, instance=companywork,
                                                                  prefix='placement_contact_formset')

        return {
            'placement_form': placement_form,
            'placement_company_form': placement_company_form,
            'placement_company_formset': placement_company_formset,
            'placement_contact_formset': placement_contact_formset,
        }

    def get_context_data(self, **kwargs):
        return self.get_context_data_placement()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        placement = self.get_context_data_placement(request.POST, files=request.FILES)
        all_valid = True

        if (placement.get('placement_form').is_valid()):
            placement.get('placement_form').save()
        else:
            all_valid = False

        if (placement.get('placement_contact_formset').is_valid()):
            placement.get('placement_contact_formset').save()
        else:
            all_valid = False

        if (placement.get('placement_company_formset').is_valid()):
            placement.get('placement_company_formset').save()
        else:
            all_valid = False

        company = placement.get('placement_company_form')
        companywork = WorkCompany.objects.get(work=self.object)
        company.instance = Company.objects.get_or_create(name=company['name'].value())[0]
        companywork.company = company.instance
        companywork.save()

        print(request.POST.get('placement_form-finish'))

        if (request.POST.get('placement_form-finish')):
            pl = self.get_placement()
            pl.finished = all_valid
            pl.save()

        return self.render_to_response(placement)

    def get_placement(self):
        return self.get_object()

    def get_success_url(self):
        return ''


class ThesisUpdateView(UpdateView):
    model = Thesis
    template_name = 'thesis_todo_form.html'
    form_class = FormThesis

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        thesis = self.get_context_data_thesis(request.POST, files=request.FILES)
        all_valid = True
        if (thesis.get('thesis_form').is_valid()):
            thesis.get('thesis_form').save()
        else:
            all_valid = False

        if (thesis.get('thesis_contact_formset').is_valid()):
            thesis.get('thesis_contact_formset').save()
        else:
            all_valid = False

        if (thesis.get('thesis_company_formset').is_valid()):
            thesis.get('thesis_company_formset').save()
        else:
            all_valid = False

        if (thesis.get('thesis_mentoringrequest_form').is_valid()):
            thesis.get('thesis_mentoringrequest_form').save()
        else:
            all_valid = False

        company = thesis.get('thesis_company_form')
        companywork = WorkCompany.objects.get(work=self.object)
        company.instance = Company.objects.get_or_create(name=company['name'].value())[0]
        companywork.company = company.instance
        companywork.save()
        """
        Set mentoring request status to 'requested'
        """
        if (request.POST.has_key('finish') and all_valid):
            self.object = self.get_object()
            self.object.mentoring.tutor_1.status = 'RE'
            self.object.mentoring.tutor_1.save()

        return self.render_to_response(thesis)

    def get_context_data_thesis(self, data=None, files=None, **kwargs):
        thesis = self.get_thesis()
        companywork = WorkCompany.objects.get(work=thesis)
        thesis_form = FormThesis(data, files=files, instance=thesis, prefix='thesis_form')
        thesis_company_form = FormCompany(data, instance=companywork.company, prefix='thesis_company_form')
        thesis_company_formset = FormsetWorkCompany(data, instance=thesis, prefix='thesis_company_formset')
        thesis_contact_formset = FormsetWorkCompanyContactdata(data, instance=companywork,
                                                               prefix='thesis_contact_formset')
        thesis_mentoringrequest_form = FormMentoringRequest(data, instance=thesis.mentoring.tutor_1,
                                                            prefix='thesis_mentoringrequest_form')

        return {
            'thesis_form': thesis_form,
            'thesis_company_form': thesis_company_form,
            'thesis_company_formset': thesis_company_formset,
            'thesis_contact_formset': thesis_contact_formset,
            'thesis_mentoringrequest_form': thesis_mentoringrequest_form,
        }

    def get_context_data(self, **kwargs):
        return self.get_context_data_thesis()

    def get_thesis(self):
        return self.get_object()

    def get_success_url(self):
        return ''


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
        context.update(self.get_context_data_placement())
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
