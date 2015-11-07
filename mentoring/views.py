# -*- coding: utf-8 -*-
from datetime import datetime
import os
from django import http
import django
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import *
from fdfgen import forge_fdf
from mentoring.forms import *
from mentoring.models import Student, Placement
from django.utils.translation import ugettext_lazy as _


class DetailView(django.views.generic.DetailView):
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(DetailView, self).get(request, *args, **kwargs)


class ListView(django.views.generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(ListView, self).get(request, *args, **kwargs)


class UpdateView(django.views.generic.UpdateView):
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(UpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return '?fancy=true' if self.request.GET.has_key('fancy') else ''


class CreateView(django.views.generic.CreateView):
    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(CreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(CreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return '?fancy=true' if self.request.GET.has_key('fancy') else ''


class IndexView(RedirectView):
    """
    + prüft ob Tutor oder Student eingeloggt ist und leitet zur entsprechenden Index-Seite weiter

    """
    permanent = False

    def get(self, request, *args, **kwargs):
        if (hasattr(request.user, 'portaluser')):
            if (hasattr(request.user.portaluser, 'tutor')):
                self.pattern_name = 'tutor-index'
            elif (hasattr(request.user.portaluser, 'student')):
                self.pattern_name = 'student-index'
        else:
            self.pattern_name = 'logout'
        return super(IndexView, self).get(request, *args, **kwargs)


class BothThesisRegistrationPDFDownload(DetailView):
    """
    Download des erstellten Anmeldeformulars
    """
    model = Registration
    target = 'attachment'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        sup = super(BothThesisRegistrationPDFDownload, self).get(request, *args, **kwargs)
        if (hasattr(request.user.portaluser,
                    'student')) and not self.object.pk == request.user.portaluser.student.thesis.registration.pk:
            return http.HttpResponseForbidden()

        if self.object.pdf_file:

            with open(settings.MEDIA_ROOT + '/' + self.object.pdf_file, 'r') as pdf:
                response = http.HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = '{}; filename="Anmeldung_Abschlussarbeit.pdf"'.format(self.target)
                return response
            pdf.closed
        else:
            return http.HttpResponseNotFound()


class BothThesisRegistrationPDFDownloadPreview(BothThesisRegistrationPDFDownload):
    target = 'inline'


class BothThesisExaminationboardFormView(UpdateView):
    """
    Erhaltene Antwort vom Prüfungsausschuss kann im System hinterlegt werden
    """
    # TODO Sicherheit: Nur eigene Mentorings aufrufen mit pk
    model = ResponseExaminationBoard
    template_name = 'both_thesis_examinationboard_form.html'
    form_class = FormRegistrationExamination

    def get_context_examinationboard(self, data=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        examinationboard = self.get_examinationboard()
        print("examinationboard = %s (%s)" % (examinationboard, type(examinationboard)))
        return {
            'examinationboard': examinationboard,
            'thesis_registration_examinationboard_form': FormRegistrationExamination(data=data,
                                                                                     instance=examinationboard,
                                                                                     prefix='examinationboard_form'),
        }

    def get_examinationboard(self, queryset=None):
        """
        muss von erbender Klasse überschrieben werden
        """
        if (hasattr(self.request.user.portaluser, 'tutor')):
            pk = self.kwargs.get(self.pk_url_kwarg, None)
            return ResponseExaminationBoard.objects.get_or_create(registration_id=pk)[0]
        else:
            th = self.request.user.portaluser.student.studentactivethesis.thesis
            if hasattr(th, 'registration') and hasattr(th.registration, 'responseexaminationboard'):
                return self.request.user.portaluser.student.studentactivethesis.thesis.registration.responseexaminationboard
            else:
                return None

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_examinationboard()

        if (request.GET.has_key('editMode')):
            self.object.finished = False
            self.object.save()
            return redirect('./?fancy=true' if request.GET.has_key('fancy') else './')

        c = self.get_context_examinationboard()
        return self.render_to_response(c)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_examinationboard()
        c = self.get_context_examinationboard(data=request.POST)
        form = c['thesis_registration_examinationboard_form']
        status = 200

        if c['thesis_registration_examinationboard_form'].is_valid():
            self.object = c['thesis_registration_examinationboard_form'].save()
            if self.object.start_editing and self.object.stop_editing:
                self.object.finished = True
                self.object.save()
        else:
            status = 400

        cd = self.get_context_data()
        cd.update(c)

        return self.render_to_response(cd, status=status)


class StudentThesisIndexView(DetailView):
    """
    Gesamtübersicht der erstellten Abschlussarbeit-Informationen
    """
    model = Thesis
    template_name = 'student_thesis_index.html'

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.studentactivethesis.thesis


class StudentPlacementListView(ListView):
    model = Placement
    template_name = 'student_placement_list.html'

    def get_queryset(self):
        return self.request.user.portaluser.student.placement_set.all()


class StudentPlacementFormView(UpdateView):
    """
    + Absolventen können Praktikumsarbeit anlegen
    + Absolventen können Praktikum beschreiben
    + Absolventen können Informationen zum Unternehmen erfassen, bei welchem das Praktikum durchgeführt wurde.
    + Absolventen können ihren Praktikumsbericht im System hochladen.
    + Absolventen können ihr Praktikumszeugnis im System hochladen.
    + Absolventen können ihre Praktikumspräsentation im System hochladen.
    """

    model = Placement
    form_class = FormPlacement
    # template_name = 'student_placement_form.html'

    def get_context_placement(self, data=None, files=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        placement = self.get_placement()
        workcompany = placement.workcompany
        return {
            'placement': placement,
            'placement_form': FormPlacement(data, files=files, instance=placement, prefix='placement_form'),
            # 'placement_event_form': FormPlacementEventRegistration(data, instance=placement.placementeventregistration,
            #                                                        prefix='placement_event_form'),
            'placement_company_form': FormCompany(data, parent=workcompany,
                                                  instance=workcompany.company,
                                                  prefix='placement_company_form'),
            'placement_company_formset': FormsetWorkCompany(data, instance=placement,
                                                            prefix='placement_company_formset'),
            'placement_contact_formset': FormsetWorkCompanyContactdata(data, instance=workcompany,
                                                                       prefix='placement_contact_formset'),
        }

    def get_placement(self):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.request.user.portaluser.student.studentactiveplacement.placement

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_placement()

        cd = self.get_context_data()
        cd.update(self.get_context_placement())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_placement()
        # if self.object.finished:
        #     return self.get(request, status=405)
        # else:
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
        return redirect('student-index')
            # self.render_to_response(cd, status=status)


class StudentPlacementIndexView(DetailView):
    """
    + Web-Ansicht des erstellten Praktikums

    """
    model = Placement
    template_name = 'both_placement_index.html'

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.placement_set.get(pk=self.kwargs.get('pk'))


def studentPlacementCreate(request):
    if (not request.user.portaluser.student.studentactiveplacement.placement.state == 'NR'):
        pl = Placement(student=request.user.portaluser.student)
        pl.save()
    return http.HttpResponseRedirect(reverse('student-index'))


def studentPlacementDelete(request, pk):
    pl = request.user.portaluser.student.placement_set.get(pk=pk)
    if (pl.state == 'NR' and len(pl.student.placement_set.all()) > 1):
        pl.delete()
        return http.HttpResponseRedirect(reverse('student-index'))


def studentPlacementEditable(request, pk):
    if (request.user.portaluser.student.studentactiveplacement.placement.state == 'NR'):
        request.user.portaluser.student.studentactiveplacement.placement.state = 'CD'
        request.user.portaluser.student.studentactiveplacement.placement.save()
    pl = request.user.portaluser.student.placement_set.get(pk=pk)
    pl.finished = False
    pl.save()
    request.user.portaluser.student.studentactiveplacement.placement = pl
    request.user.portaluser.student.studentactiveplacement.save()
    return http.HttpResponseRedirect(
        request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') else reverse('student-placement-update'))


def studentThesisCreate(request):
    if (not request.user.portaluser.student.studentactivethesis.thesis.mentoringrequest.state == 'NR'):
        th = Thesis(student=request.user.portaluser.student)
        th.save()
    return http.HttpResponseRedirect(reverse('student-index'))


def studentThesisDelete(request, pk):
    th = request.user.portaluser.student.thesis_set.get(pk=pk)
    if (th.state == 'NR' and len(th.student.thesis_set.all()) > 1):
        th.delete()
        return http.HttpResponseRedirect(reverse('student-index'))


def studentThesisEditable(request, pk):
    if (request.user.portaluser.student.studentactivethesis.thesis.mentoringrequest.state == 'NR'):
        request.user.portaluser.student.studentactivethesis.thesis.mentoringrequest.state = 'CD'
        request.user.portaluser.student.studentactivethesis.thesis.mentoringrequest.save()
    th = request.user.portaluser.student.thesis_set.get(pk=pk)
    if (th == request.user.portaluser.student.studentactivethesis.thesis and th.mentoringrequest.state == 'RE'):
        th.mentoringrequest.state = 'NR'
        th.mentoringrequest.save()
    th.save()
    request.user.portaluser.student.studentactivethesis.thesis = th
    request.user.portaluser.student.studentactivethesis.save()
    return http.HttpResponseRedirect(
        request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') else reverse('student-thesis-update'))


class StudentThesisListView(ListView):
    model = Thesis
    template_name = 'student_thesis_list.html'

    def get_queryset(self):
        return self.request.user.portaluser.student.studentactivethesis.thesis_set.all()


class StudentThesisMentoringrequestFormView(UpdateView):
    """
    + Absolventen können Abschlussarbeit anlegen
    + Absolventen können die Abschlussarbeit beschreiben
    + Absolventen können Informationen zum Unternehmen erfassen, für welches die Abschlussarbeit durchgeführt wurde.
    + Absolventen können das erfasste Thema einem Dozenten zur Betreuung vorschlagen
    + Absolventen können den Status der Betreuungsanfrage verfolgen
    + Absolventen können ein vorausgefülltes Anmeldeformular herunterladen

    """
    model = Thesis
    form_class = FormThesisMentoringrequest
    template_name = 'student_thesis_mentoringrequest_form.html'

    def get_context_thesis_mentoringrequest(self, data=None, files=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        mentoringrequest = self.get_thesis_mentoringrequest()
        thesis = mentoringrequest.thesis
        workcompany = thesis.workcompany
        return {
            'thesis': thesis,
            'thesis_mentoringrequest_form': FormThesisMentoringrequest(data, files=files, instance=thesis,
                                                                       prefix='thesis_mentoringrequest_form'),
            'thesis_mentoringrequest_company_form': FormCompany(data, parent=workcompany,
                                                                instance=workcompany.company,
                                                                prefix='thesis_mentoringrequest_company_form'),
            'thesis_mentoringrequest_company_formset': FormsetWorkCompany(data, instance=thesis,
                                                                          prefix='thesis_mentoringrequest_company_formset'),
            'thesis_mentoringrequest_contact_formset': FormsetWorkCompanyContactdata(data, instance=workcompany,
                                                                                     prefix='thesis_mentoringrequest_contact_formset'),
            'thesis_mentoringrequest_student_form': FormMentoringrequestStudent(data, instance=mentoringrequest,
                                                                                prefix='thesis_mentoringrequest_student_form'), }

    def get_thesis_mentoringrequest(self):
        if not hasattr(self.request.user.portaluser.student, 'studentactivethesis'):
            StudentActiveThesis.objects.get_or_create(student=self.request.user.portaluser.student,
                                                      thesis=self.request.user.portaluser.student.thesis_set.last())
        th = self.request.user.portaluser.student.studentactivethesis.thesis
        return th.mentoringrequest

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_thesis_mentoringrequest().thesis
        cd = self.get_context_data()
        cd.update(self.get_context_thesis_mentoringrequest())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        self.object = self.get_thesis_mentoringrequest()

        if self.object.thesis.finished or self.object.state in ['RE', 'AC']:
            return self.get(request, status=405)
        else:
            self.thesis_cd = self.get_context_thesis_mentoringrequest(request.POST, files=request.FILES)

        form_target = request.POST.get('target_form').split(',') if request.POST.has_key('target_form') else [i for i, v
                                                                                                              in
                                                                                                              self.thesis_cd.iteritems()]

        if 'thesis' in form_target:
            form_target.remove('thesis')

        status = 200

        for t in form_target:
            if self.thesis_cd.has_key(t) and self.thesis_cd.get(t).is_valid():
                self.thesis_cd.get(t).save()
            else:
                status = 400

        if status == 200:
            self.thesis_cd = self.get_context_thesis_mentoringrequest()
            if request.POST.has_key('finalize'):
                self.object.state = 'RE'
                self.object.requested_on = timezone.now()
                self.object.answer = ''
                self.object.save()
        else:
            self.object.thesis.finished = False
            self.object.thesis.save()

        cd = self.get_context_data()
        cd.update(self.thesis_cd)
        return self.render_to_response(cd, status=status)


class StudentThesisMentoringrequestView(DetailView):
    """
    + Web-Ansicht der erstellten Anfrage
    """
    model = MentoringRequest
    template_name = 'student_thesis_mentoringrequest_index.html'

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student.studentactivethesis.thesis.mentoringrequest


class StudentThesisRegistrationFormView(UpdateView):
    model = Registration
    form_class = FormRegistration
    template_name = 'student_thesis_registration_form.html'
    target = 'attachment'

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_registration()
        if (request.GET.has_key('editMode')):
            self.object.finished = False
            self.object.save()
            return redirect('./')

        cd = self.get_context_data()
        cd.update(self.get_context_registration())
        return self.render_to_response(cd)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_registration()
        reg = self.get_context_registration(data=request.POST)
        if (reg['thesis_registration_form'].is_valid()):
            return self.form_valid(reg['thesis_registration_form'])
        else:
            return self.form_invalid(reg)

    def form_invalid(self, form):
        cd = self.get_context_data()
        cd.update(form)
        return self.render_to_response(cd, status=400)

    def form_valid(self, form):
        self.object = form.save()
        self.save_pdf()
        examinationboard = ResponseExaminationBoard.objects.get_or_create(registration=self.object)[0]
        examinationboard.save()

        with open(settings.MEDIA_ROOT + "/" + self.object.pdf_file, 'r') as pdf:
            response = http.HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = '{}; filename="Anmeldung_Abschlussarbeit.pdf"'.format(self.target)
            self.object.finished = True
            self.object.save();

            return response
        pdf.closed

    def get_context_registration(self, data=None):
        registration = self.get_registration()
        return {
            'registration': registration,
            'thesis_registration_form': FormRegistration(data=data, instance=registration, prefix='registration_form')
        }

    def get_registration(self):
        return self.request.user.portaluser.student.studentactivethesis.thesis.registration

    def save_pdf(self):
        """
        Erstellt das Anmeldeformular
        """
        student = self.request.user.portaluser.student

        # Eingabefelder von 'files/docs/_2014-FBI-Anmeldung-Abschlussarbeit-Formular'

        fields = [
            ('Strasse', "%s" % (student.address.street)),
            ('PLZ_Ort', "%s %s" % (student.address.zip_code, student.address.city)),
            ('email_extern', student.extern_email),
            ('Absolventendatei', 0 if student.thesis.registration.permission_contact else 'Off'),
            ('Check Box4', 'Off'),
            ('Check Box4a', 'Off'),
            ('Studiengang', student.thesis.course),
            ('Student_Name', "%s %s" % (student.user.first_name, student.user.last_name)),
            ('Matrikelnummer', student.matriculation_number),
            ('p2_Strasse', "%s" % (student.address.street)),
            ('p2_PLZ_Ort', "%s %s" % (student.address.zip_code, student.address.city)),
            ('p2_email', student.user.email),
            ('Alumniarbeit', 'Ja' if student.thesis.registration.permission_contact else 'Off'),
            ('Infocus', 'Ja' if student.thesis.registration.permission_infocus else 'Off'),
            ('Bibliothek', 'Ja' if student.thesis.registration.permission_library else 'Off'),
            ('PubServer', 'Ja' if student.thesis.registration.permission_public else 'Off'),
            ('PubServer_EG', 'Ja' if student.thesis.registration.permission_library_tutor else 'Off'),
            ('Bearbeitungszeit', student.thesis.course.get_editing_time_display()),
            ('Thema der Abschlussarbeit', "%s" % (student.thesis.registration.subject)),
            ('Gutachter_1', "%s %s %s" % (
                student.thesis.mentoring.tutor_1.title, student.thesis.mentoring.tutor_1.user.first_name,
                student.thesis.mentoring.tutor_1.user.last_name)),
            ('Gutachter_2', "%s %s %s" % (
                student.thesis.mentoring.tutor_2.contact.title, student.thesis.mentoring.tutor_2.contact.first_name,
                student.thesis.mentoring.tutor_2.contact.last_name)),
            ('Datum_Antrag', datetime.now().strftime("%d.%m.%Y"))
        ]

        directory = "{}/{}/thesis/registration/".format(settings.MEDIA_ROOT, self.request.user)
        filename = 'Anmeldung-Abschlussarbeit.pdf'

        if not os.path.exists(directory):
            os.makedirs(directory)

        fdf = forge_fdf("", fields, [], [], [])
        fdf_file = open("{}/data.fdf".format(directory), "wb")
        fdf_file.write(fdf)
        fdf_file.close()

        os.system(
            'pdftk {mediaroot}/docs/_2014-FBI-Anmeldung-Abschlussarbeit-Formular.pdf fill_form {directory}/data.fdf '
            'output {directory}{file} flatten'.format(
                mediaroot=settings.MEDIA_ROOT, directory=directory, file=filename))

        self.object.pdf_file = "{user}/thesis/registration/{file}".format(user=self.request.user, file=filename)
        self.object.save()


class StudentSettingsFormView(UpdateView):
    """
    + Studenten können ihre persönlichen Daten hinterlegen
    + Studenten können ihre persönlichen Daten ändern
    """
    model = Student
    form_class = FormSettingsUser
    template_name = 'student_settings.html'

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(StudentSettingsFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
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
        return super(StudentSettingsFormView, self).get_context_data(
            user_form=FormSettingsUser(data=data, instance=self.get_object().user, prefix='user_form'),
            student_user_formset=FormsetUserStudent(data=data, instance=self.get_object().user,
                                                    prefix='student_user_formset'),
            student_address_formset=FormsetStudentAddress(data=data, instance=self.get_object(),
                                                          prefix='student_address_formset')
        )

    def get_object(self, queryset=None):
        return Student.objects.get(user=self.request.user)


class StudentThesisDocumentsFormView(UpdateView):
    """
    + Absolventen können ihre Abschlussarbeit im System hochladen.
    + Absolventen können ihr Poster im System hochladen.
    """

    model = Thesis
    form_class = FormThesisDocuments
    template_name = 'student_thesis_documents_form.html'

    def get_context_thesis_documents(self, data=None, files=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        thesis = self.get_thesis_documents()
        return {
            'thesis': thesis,
            'thesis_documents_form': FormThesisDocuments(data, files=files, instance=thesis,
                                                         prefix='thesis_documents_form'),
        }

    def get_thesis_documents(self):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.request.user.portaluser.student.studentactivethesis.thesis

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        self.object = self.get_thesis_documents()

        if (request.GET.has_key('editMode')):
            self.object.documents_finished = False
            self.object.save()

            return redirect('./?fancy=true' if request.GET.has_key('fancy') else './')

        cd = self.get_context_data()
        cd.update(self.get_context_thesis_documents())
        return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_thesis_documents()

        if self.object.documents_finished:
            return self.get(request, status=405)
        else:
            self.thesis = self.get_context_thesis_documents(request.POST, files=request.FILES)

        form_target = request.POST.get('target_form').split(',') if request.POST.has_key('target_form') else [i for i, v
                                                                                                              in
                                                                                                              self.thesis.iteritems()]
        status = 200
        if 'thesis' in form_target:
            form_target.remove('thesis')

        for t in form_target:
            if self.thesis.has_key(t) and self.thesis.get(t).is_valid():
                self.thesis.get(t).save()
            else:
                status = 400

        if status == 200:
            self.thesis = self.get_context_thesis_documents()
        else:
            self.object.documents_finished = False
            self.object.save()

        cd = self.get_context_data()
        cd.update(self.thesis)
        return self.render_to_response(cd, status=status)


class StudentFormView(StudentThesisDocumentsFormView, StudentThesisMentoringrequestFormView, StudentPlacementFormView,
                      StudentThesisRegistrationFormView):
    """
    Zeigt alle Studenten-Formulare in einer Seite an
    """
    template_name = 'student_index.html'
    model = Student

    def get(self, request, status=200, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            self.object = self.get_object()
            return super(UpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Alle Context-Data zusammenführen.
        Wichtig, dass die get_OBJECT Methoden korrekt überschrieben wurden
        """
        context = {}
        if self.get_object():
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            context.update(kwargs)
            context.update(self.get_context_thesis_mentoringrequest())
            context.update(self.get_context_thesis_documents())
            context.update(self.get_context_registration())
            context.update(self.get_context_placement())
            return context
        else:
            return None

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student


class TutorView(DetailView):
    """
    Startseite der Professoren
    """
    model = Tutor
    template_name = 'tutor_index.html'

    def get(self, request, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            return super(TutorView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        st = Tutor.objects.filter(user=self.request.user)
        return st[0] if len(st) > 0 else None


class TutorPlacementListView(ListView):
    model = Course
    template_name = 'tutor_placements.html'

    def get_queryset(self):
        return self.request.user.portaluser.tutor.placement_courses.all()


class TutorPlacementView(DetailView):
    model = Placement
    template_name = 'both_placement_index.html'


def tutorPlacementConfirm(request, pk):
    pl = PlacementEventRegistration.objects.get(pk=pk)
    if request.POST.get('submit') == _('Accept placement'):
        pl.confirmed = True
        pl.placement.state = 'AC'
    else:
        pl.confirmed = False
    pl.save()

    return http.HttpResponseRedirect(reverse('tutor-placement-course-registrations', kwargs={'pk': pl.event_id}))


class TutorPlacementCourseView(DetailView):
    model = Course
    template_name = 'tutor_placement_course.html'


class TutorPlacementCourseRegistrationView(ListView):
    model = PlacementEventRegistration
    template_name = 'tutor_placement_course_registration.html'

    def get_queryset(self):
        self.confirmed = self.kwargs.get('confirmed', None)
        if self.confirmed == None:
            return PlacementEventRegistration.objects.filter(event_id=self.kwargs.get('pk'))
        else:
            return PlacementEventRegistration.objects.filter(event_id=self.kwargs.get('pk'), confirmed=self)


class TutorPlacementCourseEventView(CreateView):
    model = PlacementEvent
    form_class = FormEvent
    template_name = 'tutor_placement_course_addevent.html'

    def form_valid(self, form):
        form.instance.tutor = self.request.user.portaluser.tutor
        form.instance.course_id = self.kwargs.get('pk')
        super(TutorPlacementCourseEventView, self).form_valid(form)
        return http.HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse('tutor-placement-course', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return super(TutorPlacementCourseEventView, self).get_queryset().order_by('date')


class TutorPlacementCourseEventFormView(UpdateView):
    model = PlacementEvent
    form_class = FormEvent
    template_name = 'tutor_placement_course_addevent.html'


def tutorPlacementCourseEventDelete(request, pk, ev):
    if (request.user.portaluser.tutor.placementevent_set.filter(pk=ev)):
        event = request.user.portaluser.tutor.placementevent_set.get(pk=ev)
        if not len(event.placementeventregistration_set.all()) > 0:
            event.delete()
            return http.HttpResponseRedirect(reverse('tutor-placement-course', kwargs={'pk': pk}))
    return http.HttpResponseRedirect(reverse('tutor-placement-course', kwargs={'pk': pk}))


class TutorMentoringListView(ListView):
    """
    Liste alle Arbeiten auf die betreut werden
    """
    model = Mentoring
    template_name = 'tutor_mentoring_list.html'

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(TutorMentoringListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Mentoring.objects.filter(tutor_1__user=self.request.user)


class TutorMentoringColloquiumFormView(UpdateView):
    """
    + Gutachter können Kolloquiumstermin und Uhrzeit festlegen
    + Gutachter können Raum eintragen
    """
    # TODO Gutachter können an E-Mail-Verteiler Einladungen zur Teilnhame versenden
    # TODO Gutachter können einen vorausgefüllten Begleitbogen für das Kolloquium ausdrucken
    # TODO Gutachten können nach gehaltenem Kolloquium die Note eingeben und die Abschlussarbeit abschließen

    model = Colloquium
    template_name = 'tutor_mentoring_colloquium.html'
    form_class = FormColloquium

    def get_context_colloquium(self, data=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        colloquium = self.get_colloquium()
        return {
            'colloquium': colloquium,
            'thesis_colloquium_form': FormColloquium(data=data, instance=colloquium, prefix='colloquium_form'),
        }

    def get_colloquium(self, queryset=None):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.get_object()

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_colloquium()
        c = self.get_context_colloquium()
        return self.render_to_response(c)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_colloquium()
        c = self.get_context_colloquium(data=request.POST)
        form = c['thesis_colloquium_form']

        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            cd = self.get_context_data()
            cd.update(c)
            return self.render_to_response(cd)

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return Colloquium.objects.get_or_create(mentoring_id=pk)[0]


class TutorMentoringRequestListView(ListView):
    """
    Listet alle Betreuungsanfragen auf, die an Professor gerichtet sind
    """
    model = MentoringRequest
    template_name = 'tutor_mentoring_request_list.html'

    def get(self, request, status=200, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(TutorMentoringRequestListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return MentoringRequest.objects.filter(tutor_email=self.request.user.email)


class TutorMentoringRequestFormView(UpdateView):
    """
    + Gutachter können Anfragen ablehnen
    + Gutachter können Anfragen annehmen
    + Gutachter können Zweit-Gutachter erfassen
    + Gutachter können Abgabetermin festlegen
    """
    model = MentoringRequest
    template_name = 'tutor_mentoring_request.html'
    form_class = FormMentoringrequestTutor

    def get_context_mentoringrequest(self, data=None, files=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        mentoringrequest = self.get_mentoringrequest()
        return {
            'mentoringrequest': mentoringrequest,
            'mentoringrequest_form': FormMentoringrequestTutor(data, instance=mentoringrequest,
                                                               prefix='mentoringrequest_form'),
            'mentoringrequest_tutor2_form': FormContactData(data, prefix='mentoringrequest_tutor2_form'),
        }

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_object()
        cd = self.get_context_data()
        cd.update(self.get_context_mentoringrequest())
        return self.render_to_response(cd)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_object()
        fmrt = FormMentoringrequestTutor(data=request.POST, instance=self.object, prefix='mentoringrequest_form')
        if (request.POST.get('submit') == _("Deny")):
            if (fmrt.is_valid()):
                fmrt.instance.state = 'DE'
                self.object = fmrt.save()
                status = 200
            else:
                status = 400
            cd = self.get_context_data()
            cmr = self.get_context_mentoringrequest()
            cmr['mentoringrequest_form'] = fmrt
            cd.update(cmr)
            return self.render_to_response(cd, status=status)
        elif (request.POST.get('submit') == _("Accept")):
            forms = self.get_context_mentoringrequest(data=request.POST)
            if (forms['mentoringrequest_form'].is_valid()
                and forms['mentoringrequest_tutor2_form'].is_valid()):
                status = 200
                self.object = forms['mentoringrequest_form'].save()
                mentoring = Mentoring.objects.get_or_create(request=self.object, tutor_1=request.user.portaluser.tutor,
                                                            thesis_id=self.object.thesis.pk)[
                    0]
                contact = forms['mentoringrequest_tutor2_form'].save()
                mentoring.tutor2contactdata.contact = contact
                mentoring.tutor2contactdata.save()
                self.object.state = 'AC'
                self.object.save()

                if request.POST.has_key('mentoringrequest_form-permission') and request.POST.get(
                        'mentoringrequest_form-permission') == 'on':
                    reg = Registration.objects.get_or_create(mentoring=mentoring)[0]
                    reg.permission_library_tutor = True
                    reg.save()
            else:
                status = 400

        cd = self.get_context_data()
        cd.update(forms)
        return self.render_to_response(cd, status=status)

    def get_mentoringrequest(self):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.get_object()


class TutorMentoringReportFormView(UpdateView):
    """
    + Gutachter können Erstgespräch festhalten
    + Gutachter können Verlaufsprotokoll pflegen
    """
    model = MentoringReport
    template_name = 'tutor_mentoring_report.html'
    form_class = FormMentoringReport

    def get_context_mentoringreport(self, data=None, **kwargs):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        mentoringreport = self.get_mentoringreport()
        return {
            'mentoringreport': mentoringreport,
            'thesis_mentoringreport_form': FormMentoringReport(data=data, instance=mentoringreport,
                                                               prefix='mentoringreport_form'),
            'thesis_mentoringreport_formset': FormsetReportItems(data=data, instance=mentoringreport,
                                                                 prefix='mentoringreport_formset'),
        }

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_mentoringreport()
        c = self.get_context_mentoringreport()
        return self.render_to_response(c)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        self.object = self.get_mentoringreport()
        c = self.get_context_mentoringreport(data=request.POST)

        if c['thesis_mentoringreport_form'].is_valid() and c['thesis_mentoringreport_formset'].is_valid():
            c['thesis_mentoringreport_form'].save()
            c['thesis_mentoringreport_formset'].save()
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            cd = self.get_context_data()
            cd.update(c)
            return self.render_to_response(cd)

    def get_mentoringreport(self, queryset=None):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.get_object()

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return MentoringReport.objects.get_or_create(mentoring_id=pk)[0]


class TutorMentoringFormView(TutorMentoringReportFormView, TutorMentoringColloquiumFormView):
    """
    Zeigt alle Betreuungs-Formulare in einer Seite an
    """
    model = Mentoring
    template_name = 'tutor_mentoring.html'
    form_class = FormMentoringTutor

    def get_context_mentoring(self, data=None, **kwargs):
        """
        Alle Context-Data zusammenführen.
        Wichtig, dass die get_OBJECT Methoden korrekt überschrieben wurden
        """
        mentoring = self.get_mentoring()

        c = {
            'mentoring': mentoring,
        }
        c.update(self.get_context_examinationboard(data))
        c.update(self.get_context_colloquium(data))
        c.update(self.get_context_mentoringreport(data))
        return c

    def get_mentoring(self):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return Mentoring.objects.get(pk=pk, tutor_1__user=self.request.user)

    def get_examinationboard(self, queryset=None):
        return ResponseExaminationBoard.objects.get_or_create(registration=self.object.thesis.registration)[0]

    def get_colloquium(self, queryset=None):
        return Colloquium.objects.get_or_create(mentoring=self.object)[0]

    def get_mentoringreport(self, queryset=None):
        return MentoringReport.objects.get_or_create(mentoring=self.object)[0]

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        self.object = self.get_mentoring()
        cd = self.get_context_data(form=self.get_form())
        cd.update(self.get_context_mentoring())
        return self.render_to_response(cd, status=200)

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        return Mentoring.objects.get(pk=pk, tutor_1__user=self.request.user)

    def get_success_url(self):
        return ''


class TutorSettingsFormView(UpdateView):
    """
    + Nutzer können ihre persönlichen Daten hinterlegen
    + Nutzer können ihre persönlichen Daten ändern
    """
    model = Tutor
    form_class = FormSettingsUser
    template_name = 'tutor_settings.html'

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        return super(TutorSettingsFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.GET.has_key('fancy'):
            request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
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
        return super(TutorSettingsFormView, self).get_context_data(
            user_form=FormSettingsUser(data=data, instance=self.get_object().user, prefix='user_form'),
            tutor_user_formset=FormsetUserTutor(data=data, instance=self.get_object().user, prefix='tutor_user_formset')
        )

    def get_object(self, queryset=None):
        return self.request.user.portaluser.tutor
