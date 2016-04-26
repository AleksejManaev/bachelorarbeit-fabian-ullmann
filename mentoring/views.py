# -*- coding: utf-8 -*-
import os
from thread import start_new_thread

import pypdftk
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *

from mentoring.forms import *
from mentoring.models import Student, Placement


def handle404(request):
    return redirect('login')


class IndexView(RedirectView):
    """
    + prüft ob Tutor oder Student eingeloggt ist und leitet zur entsprechenden Index-Seite weiter
    """
    permanent = False

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'portaluser'):
            if hasattr(request.user.portaluser, 'tutor'):
                self.pattern_name = 'tutor-index'
            elif hasattr(request.user.portaluser, 'student'):
                self.pattern_name = 'student-index'
        else:
            self.pattern_name = 'logout'
        return super(IndexView, self).get(request, *args, **kwargs)


class StudentPlacementFormView(UpdateView):
    template_name = 'student_placement.html'
    model = Placement
    form_class = FormPlacement

    def get_context_placement(self, data=None, files=None):
        placement = self.get_placement()
        return {
            'placement': placement,
            'placement_form': FormPlacement(data, files=files, instance=placement, prefix='placement_form'),
            'placement_contact_formset': FormsetPlacementContactdata(data, instance=placement, prefix='placement_contact_formset'),
        }

    def get_placement(self):
        return self.request.user.portaluser.student.studentactiveplacement.placement

    def post(self, request, *args, **kwargs):
        show_tutor = request.POST.get('show_tutor')
        placement = self.get_placement()

        """
            Werte der disabled Felder werden mit POST nicht mitgesendet.
            Manuelles Hinzufügen der Werte, sonst schlägt Validierung fehl.
        """
        if placement.mentoring_requested:
            post = request.POST.copy()
            post['placement_form-tutor'] = placement.tutor
            post['placement_form-task'] = placement.task
            placement_form_dict = self.get_context_placement(post, files=request.FILES)
        else:
            placement_form_dict = self.get_context_placement(request.POST, files=request.FILES)

        # Alle Formulare validieren und speichern
        target_forms = [i for i, v in placement_form_dict.iteritems()]

        if 'placement' in target_forms:
            target_forms.remove('placement')

        valid = True
        for t in target_forms:
            form = placement_form_dict.get(t)
            is_valid = form.is_valid()

            if is_valid:
                placement_form_dict.get(t).save()
            else:
                valid = False

        # Wenn alle Formulare valide sind auch das Praktikum speichern
        if valid:
            if placement.mentoring_requested is False and show_tutor:
                placement.mentoring_requested = True
                placement.state = PLACEMENT_STATE_CHOICES[1][0]
                placement.sent_on = datetime.now()
                placement.save()

        return redirect('student-placement')

    def get(self, request, status=200, *args, **kwargs):
        student = self.request.user.portaluser.student

        context = {}
        context.update(self.get_context_placement())
        context.update(self.get_denied_placements())
        context.update({'placement_state_subgoals': PLACEMENT_STATE_SUBGOAL_CHOICES})

        if not student:
            return redirect('index')
        else:
            return render(request, self.template_name, context)

    def get_denied_placements(self):
        return {'denied_placements': Placement.objects.filter(Q(student=self.request.user.portaluser.student), Q(mentoring_accepted='MD') | Q(completed='Failed'))}


class StudentThesisFormView(UpdateView):
    template_name = 'student_thesis.html'
    model = Thesis
    form_class = FormThesis

    def get_context_thesis(self, data=None, files=None):
        thesis = self.get_thesis()
        return {
            'thesis': thesis,
            'thesis_form': FormThesis(data, files=files, instance=thesis, prefix='thesis_form'),
        }

    def get_thesis(self):
        return self.request.user.portaluser.student.studentactivethesis.thesis

    def post(self, request, *args, **kwargs):
        show_tutor = request.POST.get('show_tutor')
        thesis = self.get_thesis()

        """
            Werte der disabled Felder werden mit POST nicht mitgesendet.
            Manuelles Hinzufügen der Werte, sonst schlägt Validierung fehl.
        """
        if thesis.mentoring_requested:
            post = request.POST.copy()
            post['thesis_form-tutor'] = thesis.tutor
            post['thesis_form-task'] = thesis.task
            thesis_form_dict = self.get_context_thesis(post, files=request.FILES)
        else:
            thesis_form_dict = self.get_context_thesis(request.POST, files=request.FILES)

        # Alle Formulare validieren und speichern
        target_forms = [i for i, v in thesis_form_dict.iteritems()]

        if 'thesis' in target_forms:
            target_forms.remove('thesis')

        valid = True
        for t in target_forms:
            form = thesis_form_dict.get(t)
            is_valid = form.is_valid()

            if is_valid:
                thesis_form_dict.get(t).save()
            else:
                valid = False

        # Wenn alle Formulare valide sind auch das Praktikum speichern
        if valid:
            if thesis.mentoring_requested is False and show_tutor:
                thesis.mentoring_requested = True
                thesis.sent_on = datetime.now()
                thesis.save()

        return redirect('student-thesis')

    def get(self, request, status=200, *args, **kwargs):
        student = self.request.user.portaluser.student

        context = {}
        context.update(self.get_context_thesis())
        context.update(self.get_denied_theses())

        if not student:
            return redirect('index')
        else:
            return render(request, self.template_name, context)

    def get_denied_theses(self):
        return {'denied_theses': Thesis.objects.filter(student=self.request.user.portaluser.student, mentoring_accepted='MD')}


class StudentCompletedThesesView(View):
    model = Thesis
    template_name = 'student_completed_theses.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_completed_theses())

    def get_completed_theses(self):
        return {'completed_theses': Thesis.objects.filter(student=self.request.user.portaluser.student, completed=True)}


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
            theses = Thesis.objects.filter(tutor=request.user.id, mentoring_requested=True)

            help_message_dict = {}

            for placement in placements:
                help_message_dict[placement.id] = []
                if not placement.date_from:
                    help_message_dict[placement.id].append('Praktikumsbeginn fehlt')
                if not placement.date_to:
                    help_message_dict[placement.id].append('Praktikumsende fehlt')
                if not placement.student.user.last_name:
                    help_message_dict[placement.id].append('Studentennachname fehlt')
                if not placement.student.user.first_name:
                    help_message_dict[placement.id].append('Studentenvorname fehlt')
                if not placement.student.matriculation_number:
                    help_message_dict[placement.id].append('Matrikelnummer fehlt')
                if not placement.student.user.email:
                    help_message_dict[placement.id].append('E-Mailadresse fehlt')
                if not placement.tutor:
                    help_message_dict[placement.id].append('Praktikumsbetreuer an der THB fehlt')
                if not placement.company_name:
                    help_message_dict[placement.id].append('Name des Betriebs fehlt')
                if not placement.placementcompanycontactdata.__str__():
                    help_message_dict[placement.id].append('Vor- und Nachname des Betreuers im Betrieb fehlen')
                if not placement.company_address:
                    help_message_dict[placement.id].append('Adresse des Betriebs fehlt')
                if not placement.task:
                    help_message_dict[placement.id].append('Aufgabe fehlt')
                if not placement.report_uploaded_date:
                    help_message_dict[placement.id].append('Datum Vorlage des Praktikumsberichts fehlt')
                if not placement.student.presentation_date:
                    help_message_dict[placement.id].append('Datum Vorstellung im Kolloquium fehlt')

            context = {'placements': placements, 'theses': theses, 'mentoring_states': MENTORING_STATE_CHOICES, 'examination_office_states': EXAMINATION_OFFICE_STATE_CHOICES, 'placement_states': PLACEMENT_STATE_CHOICES, 'placement_completed_states': PLACEMENT_COMPLETED_CHOICES, 'placement_state_subgoals': PLACEMENT_STATE_SUBGOAL_CHOICES, 'help_message_dict': help_message_dict}
            if 'is_thesis' in request.session:
                context['is_thesis'] = request.session['is_thesis']

            return render(request, self.template_name, context)

    def get_object(self, queryset=None):
        st = Tutor.objects.filter(user=self.request.user)
        return st[0] if len(st) > 0 else None


class TutorUpdatePlacementView(View):
    def post(self, request, pk, *args, **kwargs):
        instance = Placement.objects.get(id=pk)
        mentoring_accepted_old_value = instance.mentoring_accepted
        completed_old_value = instance.completed
        POST = request.POST

        '''
            Wenn das "Betreuung angenommen"-Feld "disabled" ist, wird der Wert über POST nicht mitgesendet. Dadurch schlägt die Validierung fehl.
            Deshalb wird der alte Wert dem Formular übergeben.
        '''
        if not request.POST.has_key('mentoring_accepted') or not request.POST.has_key('completed'):
            POST = request.POST.copy()
        if not request.POST.has_key('mentoring_accepted'):
            POST['mentoring_accepted'] = mentoring_accepted_old_value
        if not request.POST.has_key('completed'):
            POST['completed'] = completed_old_value
        form = FormTutorPlacement(POST, instance=instance)

        if form.is_valid():
            mentoring_accepted_new_value = form.cleaned_data['mentoring_accepted']
            completed_new_value = form.cleaned_data['completed']
            if mentoring_accepted_new_value == 'MD' and form.instance.state == 'Requested':
                form.instance.state = 'Mentoring denied'
            elif mentoring_accepted_new_value == 'MA' and form.instance.state == 'Requested':
                form.instance.state = 'Mentoring accepted'

            # Wenn der Praktikumsverantwortliche das Seminar für einen Studenten als Bestanden bestätigt bevor der Tutor die Betreuung annimmt.
            if form.instance.student.placement_seminar_done and form.instance.state == 'Mentoring accepted':
                form.instance.state = 'Seminar completed'

            if form.instance.state == 'Certificate accepted' and form.cleaned_data['completed'] == 'Completed':
                form.instance.state = 'Placement completed'
                self.notify(request.user, instance, _('You completed your placement.'))
            elif form.cleaned_data['completed'] == 'Failed':
                form.instance.state = 'Placement failed'
            elif form.instance.state != 'Placement completed':
                # TODO: Toast-Nachricht, Praktikum kann nicht absolviert werden, wenn der Status nicht "Certificate accepted" ist oder die Option "Absolviert" ausblenden
                form.instance.completed = '-'

            form.save()

            '''
                1. Falls eine Betreuungsanfrage abgelehnt wurde, wird dem Studenten ein neues aktives Praktikum zugewiesen.
                    Das aktive Praktikum wird über "post_save_placement" in "signals.py" zugewiesen.
                2. Wenn eine Betreuungsanfrage abgelehnt oder angenommen wurde, wird ein Kommentar und E-Mail an Student und Tutor versendet.
            '''
            if mentoring_accepted_old_value != mentoring_accepted_new_value:
                if mentoring_accepted_new_value == 'MD':
                    active_placement = Placement(student=instance.student)
                    active_placement.save()
                    self.notify(request.user, instance, _('Your mentoring request was denied.'))

                elif mentoring_accepted_new_value == 'MA':
                    self.notify(request.user, instance, _('Your mentoring request was accepted.'))
            if completed_new_value != completed_old_value:
                if completed_new_value == 'Failed':
                    active_placement = Placement(student=instance.student)
                    active_placement.save()
                    self.notify(request.user, instance, _('You failed your placement.'))

        request.session['is_thesis'] = False
        return redirect('tutor-index')

    def notify(self, tutor, placement, comment_message):
        comment = Comment(author=tutor, abstractwork=placement, message=comment_message)
        comment.save()
        Placement.objects.filter(id=placement.id).update(comment_unread_by_student=True, comment_unread_by_tutor=True)

        html_message = '<a href="http://127.0.0.1:8000/comments/placement/{}">{}</a>'.format(placement.id, _('Show comments'))
        send_comment_email([placement.student.user.email, placement.tutor.user.email], html_message)


class TutorUpdateThesisView(View):
    def post(self, request, pk, *args, **kwargs):
        instance = Thesis.objects.get(id=pk)
        mentoring_accepted_old_value = instance.mentoring_accepted
        POST = request.POST

        '''
            Wenn das "Betreuung angenommen"-Feld "disabled" ist, wird der Wert über POST nicht mitgesendet. Dadurch schlägt die Validierung fehl.
            Deshalb wird der alte Wert dem Formular übergeben.
        '''
        if not request.POST.has_key('mentoring_accepted'):
            POST = request.POST.copy()
            POST['mentoring_accepted'] = mentoring_accepted_old_value
        form = FormTutorThesis(POST, instance=instance)

        if form.is_valid():
            form.save()

            '''
                1. Falls eine Betreuungsanfrage abgelehnt wurde, wird dem Studenten eine neue aktive Abschlussarbeit zugewiesen.
                    Die aktive Abschlussarbeit wird über "post_save_thesis" in "signals.py" zugewiesen.
                2. Wenn eine Betreuungsanfrage abgelehnt oder angenommen wurde, wird ein Kommentar und E-Mail an Student und Tutor versendet.
            '''
            mentoring_accepted_new_value = form.cleaned_data['mentoring_accepted']
            if mentoring_accepted_old_value != mentoring_accepted_new_value:
                if mentoring_accepted_new_value == 'MD':
                    active_thesis = Thesis(student=instance.student)
                    active_thesis.save()
                    self.notify(request.user, instance, _('Your mentoring request was denied.'))

                elif mentoring_accepted_new_value == 'MA':
                    self.notify(request.user, instance, _('Your mentoring request was accepted.'))

            '''
                Wenn eine Abschlussarbeit absolviert wurde, wird dem Studenten eine neue aktive Abschlussarbeit zugewiesen.
            '''
            instance_is_activethesis = StudentActiveThesis.objects.filter(thesis=instance)
            if form.cleaned_data['archived'] and instance_is_activethesis:
                active_thesis = Thesis(student=instance.student)
                active_thesis.save()

        request.session['is_thesis'] = True
        return redirect('tutor-index')

    def notify(self, tutor, thesis, comment_message):
        comment = Comment(author=tutor, abstractwork=thesis, message=comment_message)
        comment.save()
        Thesis.objects.filter(id=thesis.id).update(comment_unread_by_student=True, comment_unread_by_tutor=True)

        html_message = '<a href="http://127.0.0.1:8000/comments/abstractwork/{}">{}</a>'.format(thesis.id, _('Show comments'))
        send_comment_email([thesis.student.user.email, thesis.tutor.user.email], html_message)


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
                tutor_user_formset=FormsetUserTutor(data=data, instance=self.get_object().user,
                                                    prefix='tutor_user_formset')
        )

    def get_object(self, queryset=None):
        return self.request.user.portaluser.tutor


class TutorPlacementView(UpdateView):
    model = Placement
    form_class = FormTutorPlacementDetails
    template_name = 'tutor_placement_details.html'

    def get_context_placement(self, data=None, files=None):
        placement = self.get_object()
        return {
            'placement_form': FormTutorPlacementDetails(data, files=files, instance=placement, prefix='placement_form'),
            'placement_contact_formset': FormsetPlacementContactdata(data, instance=placement, prefix='placement_contact_formset'),
        }

    def get(self, request, status=200, *args, **kwargs):
        self.request.session['is_thesis'] = False
        context = {}
        context.update(self.get_context_placement())

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        placement_form_dict = self.get_context_placement(request.POST, files=request.FILES)

        # Alle Formulare validieren und speichern
        for k, v in placement_form_dict.iteritems():
            if v.is_valid():
                if k == 'placement_form':
                    if not v.cleaned_data['report_accepted'] and v.cleaned_data['certificate_accepted']:
                        v.instance.state = 'Seminar completed'
                    elif v.cleaned_data['report_accepted'] and not v.cleaned_data['certificate_accepted']:
                        v.instance.state = 'Report accepted'
                    elif v.cleaned_data['report_accepted'] and v.cleaned_data['certificate_accepted']:
                        v.instance.state = 'Certificate accepted'
                    elif not v.cleaned_data['report_accepted'] and not v.cleaned_data['certificate_accepted']:
                        v.instance.state = 'Seminar completed'
                v.save()

        return redirect('placement-details', pk=placement_form_dict['placement_form'].instance.id)


class TutorThesisView(UpdateView):
    model = Thesis
    fields = ['type', 'task', 'poster', 'thesis', 'presentation', 'other', 'second_examiner_title', 'second_examiner_first_name', 'second_examiner_last_name',
              'second_examiner_organisation', 'colloquium_done', 'deadline_extended', 'deadline', 'grade_first_examiner', 'grade_second_examiner', 'grade_presentation']
    template_name = 'tutor_thesis_details.html'
    exclude = ['student', 'tutor', 'mentoring_requested', 'mentoring_accepted']

    def get(self, request, *args, **kwargs):
        self.request.session['is_thesis'] = True
        return super(TutorThesisView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        self.request.session['is_thesis'] = True
        return reverse('thesis-details', args=[self.object.id])


class CommentsView(View):
    template_name = 'comments.html'
    form_class = CommentForm

    def get(self, request, pk):
        # Nur der beteiligte Student und Tutor dürfen die Kommentare einsehen
        if self.is_abstractwork_allowed(pk):
            # Kommentar als gelesen für den anderen Gesprächspartner markieren
            if (hasattr(request.user, 'portaluser')):
                if (hasattr(request.user.portaluser, 'tutor')):
                    AbstractWork.objects.filter(id=pk).update(comment_unread_by_tutor=False)
                elif (hasattr(request.user.portaluser, 'student')):
                    AbstractWork.objects.filter(id=pk).update(comment_unread_by_student=False)

            comments = Comment.objects.filter(abstractwork=pk).order_by('timestamp')
            comment_form = self.form_class()
            return render(request, self.template_name, {'comments': comments, 'comment_form': comment_form})
        else:
            return HttpResponseNotFound()

    def post(self, request, pk):
        # Nur der beteiligte Student und Tutor dürfen Kommentare schreiben
        if self.is_abstractwork_allowed(pk):
            comment = Comment()
            comment.author = self.request.user.portaluser.user
            comment.abstractwork = AbstractWork.objects.get(id=pk)
            comment.message = request.POST.get('message')

            private = request.POST.get('private')
            if private is None:
                private = False
            comment.private = private

            comment.save()

            # Kommentar als ungelesen für den anderen Gesprächspartner markieren (aber nicht bei privaten) und E-Mail versenden
            if (hasattr(request.user, 'portaluser')):
                message = '<a href="http://127.0.0.1:8000/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
                abstractwork = comment.abstractwork

                if (hasattr(request.user.portaluser, 'tutor')):
                    if not private and abstractwork.student:
                        AbstractWork.objects.filter(id=pk).update(comment_unread_by_student=True)
                        send_comment_email([abstractwork.student.user.email], message)
                elif (hasattr(request.user.portaluser, 'student')):
                    if not private and abstractwork.tutor:
                        AbstractWork.objects.filter(id=pk).update(comment_unread_by_tutor=True)
                        send_comment_email([abstractwork.tutor.user.email], message)

            return redirect('comments', pk=pk)
        else:
            return HttpResponseNotFound()

    def is_abstractwork_allowed(self, pk):
        return AbstractWork.objects.filter(Q(id=pk), Q(student=self.request.user.portaluser) | Q(tutor=self.request.user.portaluser)).exists()


def togglePrivacy(request):
    # Kommentar speichern
    comment_id = request.POST.get('id')
    comment = Comment.objects.get(pk=comment_id)
    private_text = ''

    if comment.private:
        comment.private = False
        private_text = 'Not private'
    else:
        comment.private = True
        private_text = 'Private'

    comment.save()

    # Kommentar als ungelesen oder gelesen markieren (private Kommentare sind immer als gelesen markiert)
    if (hasattr(request.user, 'portaluser')):
        if (hasattr(request.user.portaluser, 'tutor')):
            if comment.private:
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_student=False)
            else:
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_student=True)
                message = '<a href="http://127.0.0.1:8000/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
                send_comment_email([comment.abstractwork.student.user.email], message)
        elif (hasattr(request.user.portaluser, 'student')):
            if comment.private:
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_tutor=False)
            else:
                email = comment.abstractwork.tutor.user.email
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_tutor=True)
                message = '<a href="http://127.0.0.1:8000/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
                # send_comment_email([comment.abstractwork.tutor.user.email], message)

    return JsonResponse({'private_state': comment.private, 'private_text': str(_(private_text))})


def send_comment_email(recipient_list, html_message):
    def run_in_new_thread():
        try:
            send_mail(_('You have unread comments.'), '', from_email='placement_thesis_service@gmx.de', recipient_list=recipient_list,
                      html_message=html_message)
        except:
            pass

    start_new_thread(run_in_new_thread, ())


class PlacementSeminarListView(ListView):
    model = PlacementSeminar
    template_name = 'placement_seminar_list.html'


class PlacementSeminarCreateView(CreateView):
    model = PlacementSeminar
    template_name = 'placement_seminar_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('placement-seminar-list')


class PlacementSeminarUpdateView(UpdateView):
    model = PlacementSeminar
    template_name = 'placement_seminar_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('placement-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(PlacementSeminarUpdateView, self).get_context_data(**kwargs)
        students = Student.objects.filter(placement_year=self.get_object().placement_year).order_by('matriculation_number')
        entrys = PlacementSeminarEntry.objects.filter(placement_seminar=self.get_object().id).order_by('date')
        numbers_present_dict = {}

        for student in students:
            numbers_present_dict[student.id] = 0

        for student in students:
            for entry in student.placement_seminar_entries.all():
                if student.id in numbers_present_dict:
                    numbers_present = numbers_present_dict[student.id]
                    numbers_present_dict[student.id] = numbers_present + 1

        context['students'] = students
        context['entrys'] = entrys
        context['numbers_present_dict'] = numbers_present_dict
        return context


class PlacementSeminarEntryCreateView(CreateView):
    model = PlacementSeminarEntry
    template_name = 'placement_seminar_entry_create.html'
    fields = ['date', 'placement_seminar']

    def get_success_url(self):
        return reverse('placement-seminar-update', args=[self.object.placement_seminar.id])

    def get_context_data(self, **kwargs):
        context = super(PlacementSeminarEntryCreateView, self).get_context_data(**kwargs)
        context['placement_seminar_id'] = self.request.GET.get('placement_seminar')
        return context


class SeminarEntryProcessView(View):
    @transaction.atomic
    def post(self, request):
        checked_student_entry_list = []
        presentation_done_student_list = []
        checked_student_placement_seminar_list = []
        placement_seminar_id = int(request.POST.get('placement_seminar'))
        placement_seminar = PlacementSeminar.objects.get(pk=placement_seminar_id)
        all_seminar_students = Student.objects.filter(placement_year=placement_seminar.placement_year)
        all_seminar_entrys = PlacementSeminarEntry.objects.filter(placement_seminar=placement_seminar_id)

        for key in request.POST:
            splitted_key = key.split('_')
            if key != 'csrfmiddlewaretoken' and not key.startswith('presentation_done') and key != 'placement_seminar' and not key.startswith(
                    'placement_seminar_done'):
                entry_id = int(splitted_key[0])
                student_id = int(splitted_key[1])
                checked_student_entry_list.append([student_id, entry_id])
            if key.startswith('presentation_done'):
                student_id = int(splitted_key[2])
                presentation_date_id = request.POST.get(key)
                presentation_done_student_list.append([student_id, presentation_date_id])
            if key.startswith('placement_seminar_done'):
                student_id = int(splitted_key[3])
                checked_student_placement_seminar_list.append(student_id)

        for student in all_seminar_students:
            placement = student.studentactiveplacement.placement
            for student_presentation in presentation_done_student_list:
                if student.id == student_presentation[0]:
                    presentation_date_id = student_presentation[1]
                    if presentation_date_id:
                        student.presentation_date = PlacementSeminarEntry.objects.get(id=int(presentation_date_id))
                    else:
                        student.presentation_date = None

            if student.id in checked_student_placement_seminar_list:
                student.placement_seminar_done = True
                if placement.state == 'Mentoring accepted':
                    if not placement.report_accepted and placement.certificate_accepted:
                        placement.state = 'Seminar completed'
                    elif placement.report_accepted and not placement.certificate_accepted:
                        placement.state = 'Report accepted'
                    elif placement.report_accepted and placement.certificate_accepted:
                        placement.state = 'Certificate accepted'
                    elif not placement.report_accepted and not placement.certificate_accepted:
                        placement.state = 'Seminar completed'
                    placement.save()
            else:
                student.placement_seminar_done = False
                state = student.studentactiveplacement.placement.state
                if state == 'Seminar completed' or state == 'Report accepted' or state == 'Certificate accepted':
                    student.studentactiveplacement.placement.state = 'Mentoring accepted'
                    student.studentactiveplacement.placement.save()
            student.save()

            for entry in all_seminar_entrys:
                student_entry = [student.id, entry.id]
                if student_entry in checked_student_entry_list:
                    entry.seminar_students.add(student)
                else:
                    entry.seminar_students.remove(student)
                entry.save()
        return redirect('placement-seminar-update', pk=placement_seminar_id)


class SeminarEntryDeleteView(DeleteView):
    model = PlacementSeminarEntry
    template = ''

    def get_success_url(self):
        return reverse('placement-seminar-update', args=[self.get_object().placement_seminar.id])

    def delete(self, request, *args, **kwargs):
        entry = self.get_object()
        success_url = self.get_success_url()
        Student.objects.filter(presentation_date=entry).update(presentation_date=None)
        entry.seminar_students.remove()
        entry.delete()
        return HttpResponseRedirect(success_url)


def generate_placement_pdf(self, pk):
    placement = Placement.objects.get(id=pk)
    student = placement.student

    # Felder füllen
    fields = {
        'BeginnDatum': placement.date_from.strftime('%d.%m.%Y') if placement.date_from else '',
        'EndeDatum': placement.date_to.strftime('%d.%m.%Y') if placement.date_to else '',
        'StudentName': u"%s, %s" % (student.user.last_name, student.user.first_name),
        'MatrNr': student.matriculation_number,
        'Telefon': student.phone,
        'Email': student.user.email,
        'THBBetreuer': u'%s' % placement.tutor,
        'BetriebName': u'%s' % placement.company_name,
        'BetriebBetreuerName': u"%s" % placement.placementcompanycontactdata if placement.placementcompanycontactdata else '',
        'BetriebAnschrift': u"%s" % placement.company_address.replace('\r', ''),
        'Aufgabe': u"%s" % placement.task.replace('\r', ''),
        'BerichtDatum': u"%s" % placement.report_uploaded_date.strftime('%d.%m.%Y') if placement.report_uploaded_date else '',
        'KolloquiumDatum': student.presentation_date.date.strftime('%d.%m.%Y') if student.presentation_date else '',
        'AktuellesDatum': datetime.now().strftime("%d.%m.%Y")
    }

    # XFDF-Datei erzeugen
    directory = "{}/{}/placement/".format(settings.MEDIA_ROOT, student.matriculation_number)
    filename = '{}-Praktikumsanerkennung.pdf'.format(student.matriculation_number)
    filepath = '{directory}/{file}'.format(directory=directory, file=filename)
    pypdftk.fill_form('{mediaroot}/docs/_Anerkennung_Praktikum_2014.pdf'.format(mediaroot=settings.MEDIA_ROOT), fields, out_file=filepath, flatten=False)

    # PDF-Datei senden, wenn diese erfolgreich erzeugt wurde
    if os.path.exists(filepath):
        with open(filepath, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(student_name=student, filename=filename)
            return response
        pdf.closed

    return redirect('index')


class StudentPlacementSeminarEntryListView(TemplateView):
    # model = PlacementSeminarEntry
    template_name = 'student_placement_seminar_entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentPlacementSeminarEntryListView, self).get_context_data(**kwargs)
        entries_list = []

        if hasattr(self.request.user, 'portaluser') and hasattr(self.request.user.portaluser, 'student'):
            student = self.request.user.portaluser.student
            entries_all = PlacementSeminarEntry.objects.filter(placement_seminar__placement_year=student.placement_year)
            entries_present_ids = student.placement_seminar_entries.values_list('id', flat=True)

            # Alle Termine und ob der Student an diesem anwesend war in einer Liste zusammenfassen
            for entry in entries_all:
                entries_list.append((entry, entry.id in entries_present_ids))

            # Kontextvariablen setzen
            context['entries_list'] = entries_list
            context['presentation_date'] = student.presentation_date
            context['placement_seminar_done'] = student.placement_seminar_done

        return context
