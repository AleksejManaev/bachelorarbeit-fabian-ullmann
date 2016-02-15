# -*- coding: utf-8 -*-

from django import http
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *

from mentoring.forms import *
from mentoring.models import Student, Placement


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


class DownloadView(View):
    def get(self, request, pk, documenttype):
        placement = Placement.objects.get(student=pk)
        student_name = placement.student

        # Tutor darf nur die Dokumente von seinen Studenten runterladen
        if not (placement.tutor.user == request.user):
            return http.HttpResponseNotFound()

        if documenttype == 'certificate':
            filepath = placement.certificate
        elif documenttype == 'report':
            filepath = placement.report
        else:
            return http.HttpResponseNotFound()

        with open(settings.MEDIA_ROOT + '/' + filepath.__str__(), 'rb') as pdf:
            response = http.HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{student_name}-{documenttype}.pdf"' \
                .format(student_name=student_name, documenttype=_(documenttype))
            return response
        pdf.closed


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

    def get_context_placement(self, data=None, files=None):
        """
        enthält all nötigen Formulare, die an Template übergeben werden und validiert werden müssen

        wird auch von erbenden Klassen genutzt
        """
        placement = self.get_placement()
        return {
            'placement': placement,
            'placement_form': FormPlacement(data, files=files, instance=placement, prefix='placement_form'),
            # 'placement_event_form': FormPlacementEventRegistration(data,
            #                                                        instance=placement.placementeventregistration,
            #                                                        prefix='placement_event_form'),
            'placement_contact_formset': FormsetPlacementContactdata(data, instance=placement,
                                                                     prefix='placement_contact_formset'),
        }

    def get_placement(self):
        """
        muss von erbender Klasse überschrieben werden
        """
        return self.request.user.portaluser.student.studentactiveplacement.placement

    # def get(self, request, status=200, *args, **kwargs):
    #     if request.GET.has_key('fancy'):
    #         request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    #     self.object = self.get_placement()
    #
    #     cd = self.get_context_data()
    #     cd.update(self.get_context_placement())
    #     return self.render_to_response(cd, status=status)

    def post(self, request, *args, **kwargs):
        show_tutor = request.POST.get('show_tutor')
        self.object = self.get_placement()

        placement_form_dict = self.get_context_placement(request.POST, files=request.FILES)

        form_target = [i for i, v in placement_form_dict.iteritems()]

        if 'placement' in form_target:
            form_target.remove('placement')

        valid = True
        for t in form_target:
            in_placement_form_dict = t in placement_form_dict
            form = placement_form_dict.get(t)
            is_valid = form.is_valid()

            if in_placement_form_dict and is_valid:
                placement_form_dict.get(t).save()
            else:
                valid = False

        if valid:
            placement_form_dict = self.get_context_placement()

            if self.object.mentoring_requested is False and show_tutor:
                self.object.mentoring_requested = True
                self.object.sent_on = datetime.now()
                self.object.save()

        cd = self.get_context_data()
        cd.update(placement_form_dict)
        return redirect('student-placement')


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
                                                                                prefix='thesis_mentoringrequest_student_form'),}

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


class StudentFormView(StudentThesisMentoringrequestFormView, StudentPlacementFormView):
    """
    Zeigt alle Studenten-Formulare in einer Seite an
    """
    template_name = 'student_placement.html'
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
            # context.update(self.get_context_thesis_mentoringrequest())
            context.update(self.get_context_placement())
            context.update(self.get_denied_placements())
            return context
        else:
            return None

    def get_denied_placements(self):
        return {'denied_placements': Placement.objects.filter(student=self.request.user.portaluser.student,
                                                              mentoring_accepted='MD')}

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student


class TutorView(View):
    """
    Startseite der Professoren
    """
    model = Tutor
    template_name = 'tutor_index.html'

    def get(self, request, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            placements = Placement.objects.filter(tutor=request.user.id, mentoring_requested=True)
            return render(request, self.template_name, {'placements': placements, 'states': STATUS_CHOICES})

    def get_object(self, queryset=None):
        st = Tutor.objects.filter(user=self.request.user)
        return st[0] if len(st) > 0 else None


class TutorUpdatePlacementView(View):
    def post(self, request, pk, *args, **kwargs):
        instance = Placement.objects.get(id=pk)
        form = FormTutorPlacement(request.POST or None, instance=instance)

        if form.is_valid():
            form.save()

            '''
                Falls eine Betreuungsanfrage abgelehnt wurde, wird dem Studenten ein neues aktives Praktikum zugewiesen.
                Das aktive Praktikum wird über wird über "post_save_placement" in "signals.py" zugewiesen.
            '''
            if form.cleaned_data['mentoring_accepted'] == 'MD':
                active_placement = Placement(student=instance.student)
                active_placement.save()

        return redirect('tutor-index')


class StudentIndexView(View):
    template_name = 'student_index.html'

    def get(self, request, status=200, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            return render(request, self.template_name)

    def get_object(self, queryset=None):
        return self.request.user.portaluser.student


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


class TutorPlacementView(DetailView):
    model = Placement


class PlacementCommentsView(View):
    template_name = 'comments.html'
    form_class = CommentForm

    def get(self, request, pk):
        # Nur der beteiligte Student und Tutor dürfen die Kommentare einsehen
        if self.is_placement_allowed(pk):
            comments = Comment.objects.filter(abstract_work=pk).order_by('timestamp')
            comment_form = self.form_class()
            return render(request, self.template_name, {'comments': comments, 'comment_form': comment_form})
        else:
            return http.HttpResponseNotFound()

    def post(self, request, pk):
        # Nur der beteiligte Student und Tutor dürfen Kommentare schreiben
        if self.is_placement_allowed(pk):
            comment = Comment()
            comment.author = self.request.user.portaluser.user
            comment.abstract_work = AbstractWork.objects.get(id=pk)
            comment.message = request.POST.get('message')
            comment.save()

            return redirect('placements-comments', pk=pk)
        else:
            return http.HttpResponseNotFound()

    def is_placement_allowed(self, pk):
        return Placement.objects.filter(Q(id=pk), Q(student=self.request.user.portaluser) | Q(
            tutor=self.request.user.portaluser)).exists()
