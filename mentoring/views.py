# -*- coding: utf-8 -*-
from datetime import datetime

from django import http
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import *
from fdfgen import forge_fdf
from mentoring.forms import *
from mentoring.models import Student, Placement


class IndexView(RedirectView):
    permanent = True

    def get(self, request, *args, **kwargs):
        if (hasattr(request.user, 'portaluser')):
            if (hasattr(request.user.portaluser, 'tutor')):
                self.pattern_name = 'tutor-overview'
            elif (hasattr(request.user.portaluser, 'student')):
                self.pattern_name = 'student-overview'
        else:
            self.pattern_name = 'logout'
        return super(IndexView, self).get(request, *args, **kwargs)


class PlacementUpdateView(UpdateView):
    model = Placement
    form_class = FormPlacement
    template_name = 'student/placement/placement_form.html'

    def get_context_placement(self, data=None, files=None, **kwargs):
        placement = self.get_placement()
        return {
            'placement': placement,
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
        if 'placement' in form_target:
            form_target.remove('placement')

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

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.placement


class PlacementPreviewView(DetailView):
    model = Placement
    template_name = 'student/placement/placement_index.html'

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.placement


class ThesisMentoringrequestUpdateView(UpdateView):
    model = Thesis
    form_class = FormThesis
    template_name = 'student/thesis/mentoringrequest/mentoringrequest_form.html'

    def get_context_thesis(self, data=None, files=None, **kwargs):
        thesis = self.get_thesis()
        return {
            'thesis': thesis,
            'thesis_form': FormThesis(data, files=files, instance=thesis, prefix='thesis_form'),
            'thesis_company_form': FormCompany(data, parent=thesis.workcompany, instance=thesis.workcompany.company,
                                               prefix='thesis_company_form'),
            'thesis_company_formset': FormsetWorkCompany(data, instance=thesis, prefix='thesis_company_formset'),
            'thesis_contact_formset': FormsetWorkCompanyContactdata(data, instance=thesis.workcompany,
                                                                    prefix='thesis_contact_formset'),
            'thesis_mentoringrequest_form': FormMentoringrequestStudent(data, instance=thesis.mentoringrequest,
                                                                        prefix='thesis_mentoringrequest_form'), }

    def get(self, request, status=200, *args, **kwargs):
        self.object = self.get_object()

        if (request.GET.has_key('editMode') and not self.object.mentoringrequest.status == 'AC'):
            self.object.mentoringrequest.status = 'NR'
            self.object.mentoringrequest.save()
            return redirect('./')

        cd = self.get_context_data()
        cd.update(self.get_context_thesis())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        if self.object.finished or self.object.mentoringrequest.status in ['RE', 'AC']:
            return self.get(request, status=405)
        else:
            self.thesis = self.get_context_thesis(request.POST, files=request.FILES)

        form_target = request.POST.get('target_form').split(',') if request.POST.has_key('target_form') else [i for i, v
                                                                                                              in
                                                                                                              self.thesis.iteritems()]

        if 'thesis' in form_target:
            form_target.remove('thesis')

        status = 200

        for t in form_target:
            if self.thesis.has_key(t) and self.thesis.get(t).is_valid():
                self.thesis.get(t).save()
            else:
                status = 400

        if status == 200:
            self.thesis = self.get_context_thesis()
            if request.POST.has_key('finalize'):
                self.object.mentoringrequest.status = 'RE'
                self.object.mentoringrequest.requested_on = timezone.now()
                self.object.mentoringrequest.answer = ''
                self.object.mentoringrequest.save()
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

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.thesis


class ThesisRegistrationUpdateView(UpdateView):
    model = Registration
    form_class = FormRegistration
    template_name = 'student/thesis/registration/registration_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_registration()
        cd = self.get_context_data()
        cd.update(self.get_context_registration())
        return self.render_to_response(cd)

    def post(self, request, *args, **kwargs):
        self.object = self.get_registration()
        reg = self.get_context_registration(data=request.POST)
        if (reg['thesis_registration_form'].is_valid()):
            return self.form_valid(reg['thesis_registration_form'])
        else:
            return self.form_invalid(reg['thesis_registration_form'])

    def get_context_registration(self, data=None):
        registration = self.get_registration()
        return {
            'registration': registration,
            'thesis_registration_form': FormRegistration(data=data, instance=registration, prefix='registration_form')
        }

    def get_registration(self):
        return self.get_object()

    def get_object(self, queryset=None):
        return Registration.objects.get_or_create(
            mentoring=self.request.user.portaluser.student.thesis.mentoringrequest.mentoring)[0]

    def get_success_url(self):
        return ''


class ThesisRegistrationPDF(View):
    target = 'attachment'

    def get(self, request, *args, **kwargs):
        student = self.request.user.portaluser.student

        """
        Eingabefelder von 'files/docs/_2014-FBI-Anmeldung-Abschlussarbeit-Formular'
        """

        fields = [
            ('Strasse', student.address.street),
            ('PLZ_Ort', '{} {}'.format(student.address.zip_code, student.address.city)),
            ('email_extern', student.extern_email),
            ('Absolventendatei', 0 if student.thesis.registration.permission_contact else 'Off'),
            ('Check Box4', 'Off'),
            ('Check Box4a', 'Off'),
            ('Studiengang', student.course),
            ('Student_Name', student.user.get_full_name()),
            ('Matrikelnummer', student.matriculation_number),
            ('p2_Strasse', student.address.street),
            ('p2_PLZ_Ort', '{} {}'.format(student.address.zip_code, student.address.city)),
            ('p2_email', student.user.email),
            ('Alumniarbeit', 'Ja' if student.thesis.registration.permission_contact else 'Off'),
            ('Infocus', 'Ja' if student.thesis.registration.permission_infocus else 'Off'),
            ('Bibliothek', 'Ja' if student.thesis.registration.permission_library else 'Off'),
            ('PubServer', 'Ja' if student.thesis.registration.permission_public else 'Off'),
            ('PubServer_EG', 'Ja' if student.thesis.registration.permission_library_tutor else 'Off'),
            ('Bearbeitungszeit', student.course.get_editing_time_display()),
            ('Thema der Abschlussarbeit', student.thesis.registration.subject),
            ('Gutachter_1', student.thesis.mentoring.tutor_1),
            ('Gutachter_2', student.thesis.mentoring.tutor_2),
            ('Datum_Antrag', datetime.now().strftime("%d.%m.%Y"))
        ]
        """
        Where to save the registration-pdf
        """
        print(settings.MEDIA_ROOT)
        directory = "{}/{}/thesis/registration/".format(settings.MEDIA_ROOT, request.user)
        print(directory)
        filename = 'Anmeldung-Abschlussarbeit-{firstn}-{lastn}.pdf'.format(directory=directory,
                                                                           firstn=request.user.first_name,
                                                                           lastn=request.user.last_name)
        print(os.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        """
        write formular data to file
        """
        fdf = forge_fdf("", fields, [], [], [])
        fdf_file = open("{}/data.fdf".format(directory), "wb")
        fdf_file.write(fdf)
        fdf_file.close()

        """
        call command line
        """
        os.system(
            'pdftk {mediaroot}/docs/_2014-FBI-Anmeldung-Abschlussarbeit-Formular.pdf fill_form {directory}/data.fdf output {directory}/{file}'.format(
                mediaroot=settings.MEDIA_ROOT, directory=directory, file=filename))

        with open('{}{}'.format(directory, filename), 'r') as pdf:
            response = http.HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = '{}; filename="{}"'.format(self.target, filename)
            return response
        pdf.closed


class ThesisRegistrationPDFPreview(ThesisRegistrationPDF):
    target = 'inline'


class ThesisPreviewView(DetailView):
    model = Thesis
    template_name = 'student/thesis/thesis_index.html'

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.thesis


class StudentUpdateView(ThesisMentoringrequestUpdateView, PlacementUpdateView, ThesisRegistrationUpdateView):
    template_name = 'student/student_index.html'
    model = Student

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        context.update(self.get_context_thesis())
        context.update(self.get_context_placement())
        context.update(self.get_context_registration())
        return context

    def get_thesis(self):
        return self.get_object().thesis

    def get_placement(self):
        return self.get_object().placement

    def get_registration(self):
        return self.get_object().thesis.registration

    def get_object(self, queryset=None):
        return Student.objects.get(user=self.request.user)


class TutorView(DetailView):
    model = Tutor
    template_name = 'tutor/tutor_index.html'

    def get_object(self, queryset=None):

        return Tutor.objects.get(user=self.request.user)


class TutorMentoringrequestView(UpdateView):
    model = MentoringRequest
    template_name = 'tutor/tutor_mentoringrequest.html'
    form_class = FormMentoringrequestTutor

    def get_context_mentoringrequest(self, data=None, files=None, **kwargs):
        mentoringrequest = self.get_object()
        return {
            'mentoringrequest': mentoringrequest,
            'mentoringrequest_form': FormMentoringrequestTutor(data, instance=mentoringrequest,
                                                               prefix='mentoringrequest_form'),
            'mentoringrequest_tutor2_form': FormContactData(data, prefix='mentoringrequest_tutor2_form'),
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cd = self.get_context_data()
        cd.update(self.get_context_mentoringrequest())
        return self.render_to_response(cd)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        fmrt = FormMentoringrequestTutor(data=request.POST, instance=self.object, prefix='mentoringrequest_form')

        if (request.POST.has_key('deny')):
            if (fmrt.is_valid()):
                fmrt.instance.status = 'DE'
                self.object = fmrt.save()
                status = 200
            else:
                status = 400
            cd = self.get_context_data()
            cmr = self.get_context_mentoringrequest()
            cmr['mentoringrequest_form'] = fmrt
            cd.update(cmr)
            return self.render_to_response(cd, status=status)

        elif (request.POST.has_key('accept')):
            forms = self.get_context_mentoringrequest(data=request.POST)
            if (forms['mentoringrequest_form'].is_valid()
                and forms['mentoringrequest_tutor2_form'].is_valid()):
                status = 200
                self.object = forms['mentoringrequest_form'].save()
                mentoring = Mentoring.objects.get_or_create(request=self.object, tutor_1=request.user.portaluser.tutor)[
                    0]
                contact = forms['mentoringrequest_tutor2_form'].save()
                tutor2contactdata = Tutor2ContactData(contact=contact, mentoring=mentoring)
                tutor2contactdata.save()
                self.object.status = 'AC'
                self.object.save()

                if request.POST.has_key('mentoringrequest_form-permission') and request.POST.get(
                        'mentoringrequest_form-permission') == 'on':
                    print "has permission"
                    reg = Registration.objects.get_or_create(mentoring=mentoring)[0]
                    reg.permission_library_tutor = True
                    reg.save()
            else:
                status = 400

        cd = self.get_context_data()
        cd.update(forms)
        return self.render_to_response(cd, status=status)


class StudentSettingsView(UpdateView):
    model = Student
    form_class = FormSettings
    template_name = 'student/student_settings.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        cd = self.get_context_data(request.POST)

        if (cd.get('user_form').is_valid()
            and cd.get('student_user_formset').is_valid()
            and cd.get('student_address_formset').is_valid()):
            cd.get('user_form').save()
            cd.get('student_user_formset').save()
            cd.get('student_address_formset').save()
            return self.render_to_response(cd, status=200)
        else:
            return self.render_to_response(cd, status=400)

    def get_context_data(self, data=None, **kwargs):
        return super(StudentSettingsView, self).get_context_data(
            user_form=FormSettings(data=data, instance=self.get_object().user),
            student_user_formset=FormsetUserPortaluser(data=data, instance=self.get_object().user),
            student_address_formset=FormsetStudentAddress(data=data, instance=self.get_object())
        )

    def get_object(self, queryset=None):
        return Student.objects.get(user=self.request.user)


class TutorSettingsView(UpdateView):
    model = Tutor
    form_class = FormSettings
    template_name = 'tutor/tutor_settings.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        cd = self.get_context_data(request.POST)
        if (cd.get('user_form').is_valid()
            and cd.get('tutor_user_formset').is_valid()):
            cd.get('user_form').save()
            cd.get('tutor_user_formset').save()
            return self.render_to_response(cd, status=200)
        else:
            return self.render_to_response(cd, status=400)

    def get_context_data(self, data=None, **kwargs):
        return super(TutorSettingsView, self).get_context_data(
            user_form=FormSettings(data=data, instance=self.get_object().user),
            tutor_user_formset=FormsetUserPortaluser(data=data, instance=self.get_object().user)
        )

    def get_object(self, queryset=None):
        return Tutor.objects.get(user=self.request.user)
