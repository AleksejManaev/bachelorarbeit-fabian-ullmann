# -*- coding: utf-8 -*-
import os
from _thread import start_new_thread

from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction, connection
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from docxtpl import DocxTemplate

from mentoring.forms import *
from mentoring.models import Student, Placement


class IndexView(RedirectView):
    """
    + prüft ob Tutor oder Student eingeloggt ist und leitet zur entsprechenden Index-Seite weiter
    """
    permanent = False

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'portaluser'):
            if hasattr(request.user.portaluser, 'tutor'):
                tutor = request.user.portaluser.tutor
                if not tutor.placement_responsible and not tutor.thesis_responsible and tutor.poster_responsible:
                    self.pattern_name = 'posters-index'
                else:
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
        target_forms = [i for i, v in placement_form_dict.items()]

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
            post['thesis_form-type'] = thesis.type
            thesis_form_dict = self.get_context_thesis(post, files=request.FILES)
        else:
            thesis_form_dict = self.get_context_thesis(request.POST, files=request.FILES)

        # Alle Formulare validieren und speichern
        target_forms = [i for i, v in thesis_form_dict.items()]

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

        # Wenn alle Formulare valide sind, dann ggf. den Zustand der Abschlussarbeit anpassen und die Arbeit speichern
        if valid:
            if thesis.mentoring_requested is False and show_tutor:
                thesis.mentoring_requested = True
                thesis.state = 'Requested'
                thesis.sent_on = datetime.now()
                thesis.save()
            else:
                thesis.state = 'Requested'
                if thesis.mentoring_accepted == 'MA':
                    thesis.state = 'Mentoring accepted'
                    if thesis.examination_office_state == '1B':
                        thesis.state = 'Examination office submitted'
                    elif thesis.examination_office_state == '2A':
                        thesis.state = 'Examination office accepted'
                        if thesis.thesis:
                            thesis.state = 'Thesis submitted'
                            if thesis.colloquium_done:
                                thesis.state = 'Colloquium completed'
                                if thesis.type == 'Bachelor' and thesis.student.bachelor_seminar_done:
                                    thesis.state = 'Seminar completed'
                                elif thesis.type == 'Master' and thesis.student.master_seminar_done:
                                    thesis.state = 'Seminar completed'
                                    if thesis.poster_accepted:
                                        thesis.state = 'Poster accepted'
                elif thesis.mentoring_accepted == 'MD':
                    thesis.state = 'Mentoring denied'
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
        return {'completed_theses': Thesis.objects.filter(student=self.request.user.portaluser.student, completed=ABSTRACTWORK_COMPLETED_CHOICES[1][0])}


class StudentSettingsFormView(UpdateView):
    """
    + Studenten können ihre persönlichen Daten hinterlegen
    + Studenten können ihre persönlichen Daten ändern
    """
    model = Student
    form_class = FormSettingsUser
    template_name = 'student_settings.html'

    def get(self, request, *args, **kwargs):
        return super(StudentSettingsFormView, self).get(request, *args, **kwargs)

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
                if not placement.student.placement_seminar_presentation_date:
                    help_message_dict[placement.id].append('Datum Vorstellung im Kolloquium fehlt')

            context = {'placements': placements, 'theses': theses, 'mentoring_states': MENTORING_STATE_CHOICES, 'examination_office_states': EXAMINATION_OFFICE_STATE_CHOICES, 'placement_states': PLACEMENT_STATE_CHOICES,
                       'placement_completed_states': ABSTRACTWORK_COMPLETED_CHOICES, 'placement_state_subgoals': PLACEMENT_STATE_SUBGOAL_CHOICES, 'thesis_state_subgoals': THESIS_STATE_SUBGOAL_CHOICES,
                       'help_message_dict': help_message_dict, 'thesis_choices': THESIS_CHOICES}

            # Dictionary mit den Gesamtnoten zu den Abschlussarbeiten
            thesis_final_grade_dict = {}
            for thesis in theses:
                if thesis.grade_first_examiner and thesis.grade_second_examiner and thesis.grade_presentation:
                    final_grade = thesis.grade_first_examiner * Decimal('0.375') + thesis.grade_second_examiner * Decimal('0.375') + thesis.grade_presentation * Decimal('0.25')
                    final_grade_rounded = round(final_grade, 1)

                    final_grade_valid = None
                    for grade in GRADE_CHOICES:
                        if final_grade_rounded == grade[0]:
                            final_grade_valid = grade
                            break
                        elif final_grade_rounded > grade[0]:
                            continue
                        else:
                            final_grade_valid = grade
                            break

                    thesis_final_grade_dict[thesis.id] = final_grade_valid[0]
            context['thesis_final_grade_dict'] = thesis_final_grade_dict

            # Signalisieren, dass Der Abschlussarbeiten-Tab aktiv sein soll bei der Anzeige
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
        if 'mentoring_accepted' not in request.POST or 'completed' not in request.POST:
            POST = request.POST.copy()
        if 'mentoring_accepted' not in request.POST:
            POST['mentoring_accepted'] = mentoring_accepted_old_value
        if 'completed' not in request.POST:
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

        html_message = '<a href="http://grad-man.th-brandenburg.de/comments/placement/{}">{}</a>'.format(placement.id, _('Show comments'))
        send_comment_email([placement.student.user.email, placement.tutor.user.email], html_message)


class TutorUpdateThesisView(View):
    def post(self, request, pk, *args, **kwargs):
        instance = Thesis.objects.get(id=pk)
        mentoring_accepted_old_value = instance.mentoring_accepted
        examination_office_state_old_value = instance.examination_office_state
        POST = request.POST

        '''
            Wenn das "Betreuung angenommen"-Feld "disabled" ist, wird der Wert über POST nicht mitgesendet. Dadurch schlägt die Validierung fehl.
            Deshalb wird der alte Wert dem Formular übergeben.
        '''
        if 'mentoring_accepted' not in request.POST or 'completed' not in request.POST:
            POST = request.POST.copy()
        if 'mentoring_accepted' not in request.POST:
            POST['mentoring_accepted'] = mentoring_accepted_old_value
        if 'examination_office_state' not in request.POST:
            POST['examination_office_state'] = examination_office_state_old_value
        form = FormTutorThesis(POST, instance=instance)

        if form.is_valid():
            mentoring_accepted_new_value = form.cleaned_data['mentoring_accepted']
            if mentoring_accepted_new_value == 'MD' and form.instance.state == 'Requested':
                form.instance.state = 'Mentoring denied'
            elif mentoring_accepted_new_value == 'MA' and form.instance.state == 'Requested':
                form.instance.state = 'Mentoring accepted'

            examination_office_state_new_value = form.cleaned_data['examination_office_state']
            if mentoring_accepted_new_value == 'MA':
                if examination_office_state_new_value == '1A':
                    form.instance.state = 'Mentoring accepted'
                elif examination_office_state_new_value == '1B':
                    form.instance.state = 'Examination office submitted'
                elif examination_office_state_new_value == '2A':
                    form.instance.state = 'Examination office accepted'
                    if form.instance.thesis:
                        form.instance.state = 'Thesis submitted'
                    if form.instance.state == 'Thesis submitted' and form.instance.colloquium_done:
                        form.instance.state = 'Colloquium completed'
                    if form.instance.state == 'Colloquium completed':
                        if form.instance.type == 'Bachelor' and form.instance.student.bachelor_seminar_done:
                            form.instance.state = 'Seminar completed'
                        elif form.instance.type == 'Master' and form.instance.student.master_seminar_done:
                            form.instance.state = 'Seminar completed'
                        if form.instance.state == 'Seminar completed' and form.instance.poster_accepted:
                            form.instance.state = 'Poster accepted'

                elif examination_office_state_new_value == '2B':
                    form.instance.state = 'Mentoring accepted'

            form.save()

            '''
                1. Falls eine Betreuungsanfrage abgelehnt wurde, wird dem Studenten eine neue aktive Abschlussarbeit zugewiesen.
                    Die aktive Abschlussarbeit wird über "post_save_thesis" in "signals.py" zugewiesen.
                2. Wenn eine Betreuungsanfrage abgelehnt oder angenommen wurde, wird ein Kommentar und E-Mail an Student und Tutor versendet.
            '''
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

        html_message = '<a href="http://grad-man.th-brandenburg.de/comments/abstractwork/{}">{}</a>'.format(thesis.id, _('Show comments'))
        send_comment_email([thesis.student.user.email, thesis.tutor.user.email], html_message)


class StudentIndexView(View):
    template_name = 'student_index.html'

    def get(self, request, status=200, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            return render(request, self.template_name)

    def get_object(self, queryset=None):
        student = Student.objects.filter(user=self.request.user)
        return student[0] if len(student) > 0 else None


class TutorSettingsFormView(UpdateView):
    """
    + Nutzer können ihre persönlichen Daten hinterlegen
    + Nutzer können ihre persönlichen Daten ändern
    """
    model = Tutor
    form_class = FormSettingsUser
    template_name = 'tutor_settings.html'

    def get(self, request, *args, **kwargs):
        return super(TutorSettingsFormView, self).get(request, *args, **kwargs)

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
        all_forms_valid = False
        for k, v in placement_form_dict.items():
            all_forms_valid = v.is_valid()
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
            else:
                break

        # Django-Message hinzufügen
        if all_forms_valid:
            messages.add_message(request, messages.SUCCESS, _('Placement successfully updated.'))
        else:
            messages.add_message(request, messages.ERROR, _('Placement update failed.'))

        return redirect('placement-details', pk=placement_form_dict['placement_form'].instance.id)


class TutorThesisView(UpdateView):
    model = Thesis
    form_class = FormTutorThesisDetails
    template_name = 'tutor_thesis_details.html'

    def get_context_thesis(self, data=None, files=None):
        thesis = self.get_object()
        return FormTutorThesisDetails(data, files=files, instance=thesis)

    def get(self, request, *args, **kwargs):
        self.request.session['is_thesis'] = True
        return super(TutorThesisView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_context_thesis(request.POST, files=request.FILES)

        # Formular validieren und speichern, Django-Message hinzufügen
        if form.is_valid():
            if form.instance.state == 'Thesis submitted' and form.cleaned_data['colloquium_done']:
                form.instance.state = 'Colloquium completed'

                if form.instance.state == 'Colloquium completed':
                    if form.instance.type == 'Bachelor' and form.instance.student.bachelor_seminar_done:
                        form.instance.state = 'Seminar completed'
                    elif form.instance.type == 'Master' and form.instance.student.master_seminar_done:
                        form.instance.state = 'Seminar completed'
                    if form.instance.state == 'Seminar completed' and form.instance.poster_accepted:
                        form.instance.state = 'Poster accepted'

            if not form.cleaned_data['colloquium_done']:
                if form.instance.state == 'Colloquium completed' or form.instance.state == 'Seminar completed' or form.instance.state == 'Poster accepted':
                    if form.instance.mentoring_accepted == 'MA':
                        form.instance.state = 'Mentoring accepted'
                        if form.instance.examination_office_state == '1B':
                            form.instance.state = 'Examination office submitted'
                        elif form.instance.examination_office_state == '2A':
                            form.instance.state = 'Examination office accepted'
                            if form.instance.thesis:
                                form.instance.state = 'Thesis submitted'
                    else:
                        if form.instance.mentoring_accepted == 'MD':
                            form.instance.state = 'Mentoring Denied'
                        elif form.instance.mentoring_accepted == 'ND':
                            form.instance.state = 'Requested'

            form.save()
            messages.add_message(request, messages.SUCCESS, _('Thesis successfully updated.'))
        else:
            messages.add_message(request, messages.ERROR, _('Thesis update failed.'))

        return redirect('thesis-details', pk=form.instance.id)


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
                message = '<a href="http://grad-man.th-brandenburg.de/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
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
                message = '<a href="http://grad-man.th-brandenburg.de/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
                send_comment_email([comment.abstractwork.student.user.email], message)
        elif (hasattr(request.user.portaluser, 'student')):
            if comment.private:
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_tutor=False)
            else:
                AbstractWork.objects.filter(id=comment.abstractwork.id).update(comment_unread_by_tutor=True)
                message = '<a href="http://grad-man.th-brandenburg.de/comments/abstractwork/{}">{}</a>'.format(comment.abstractwork.id, _('Show comments'))
                send_comment_email([comment.abstractwork.tutor.user.email], message)

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
    context_object_name = 'placement_seminar_list'
    queryset = Seminar.objects.filter(type=SEMINAR_TYPE_CHOICES[0][0])
    template_name = 'placement_seminar_list.html'


class PlacementSeminarCreateView(CreateView):
    model = Seminar
    template_name = 'seminar_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('placement-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(PlacementSeminarCreateView, self).get_context_data(**kwargs)
        context['seminar_type'] = SEMINAR_TYPE_CHOICES[0][0]
        return context


class PlacementSeminarUpdateView(UpdateView):
    model = Seminar
    template_name = 'placement_seminar_update.html'
    fields = ['year']

    def get_success_url(self):
        return reverse('placement-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(PlacementSeminarUpdateView, self).get_context_data(**kwargs)
        students = Student.objects.filter(placement_year=self.get_object().year).order_by('matriculation_number')
        entrys = SeminarEntry.objects.filter(seminar=self.get_object().id, seminar__type=SEMINAR_TYPE_CHOICES[0][0]).order_by('date')
        numbers_present_dict = {}

        for student in students:
            numbers_present_dict[student.id] = 0

        for student in students:
            student_entrys = student.seminar_entries.all().filter(seminar__type=SEMINAR_TYPE_CHOICES[0][0])
            for entry in student_entrys:
                if student.id in numbers_present_dict:
                    numbers_present = numbers_present_dict[student.id]
                    numbers_present_dict[student.id] = numbers_present + 1

        context['students'] = students
        context['entrys'] = entrys
        context['numbers_present_dict'] = numbers_present_dict
        return context


class PlacementSeminarEntryCreateView(CreateView):
    model = SeminarEntry
    template_name = 'placement_seminar_entry_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('placement-seminar-update', args=[self.object.seminar.id])

    def get_context_data(self, **kwargs):
        context = super(PlacementSeminarEntryCreateView, self).get_context_data(**kwargs)
        context['placement_seminar_id'] = self.request.GET.get('placement_seminar')
        return context


class PlacementSeminarEntryProcessView(View):
    @transaction.atomic
    def post(self, request):
        checked_student_entry_list = []
        presentation_done_student_list = []
        checked_student_placement_seminar_list = []
        placement_seminar_id = int(request.POST.get('placement_seminar'))
        placement_seminar = Seminar.objects.get(pk=placement_seminar_id)
        all_seminar_students = Student.objects.filter(placement_year=placement_seminar.year)
        all_seminar_entrys = SeminarEntry.objects.filter(seminar=placement_seminar_id)

        for key in request.POST:
            splitted_key = key.split('_')
            if key != 'csrfmiddlewaretoken' and not key.startswith('presentation_done') and key != 'placement_seminar' and not key.startswith('placement_seminar_done'):
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
                        student.placement_seminar_presentation_date = SeminarEntry.objects.get(id=int(presentation_date_id))
                    else:
                        student.placement_seminar_presentation_date = None

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


class PlacementSeminarEntryDeleteView(DeleteView):
    model = SeminarEntry

    def get_success_url(self):
        return reverse('placement-seminar-update', args=[self.get_object().seminar.id])

    def delete(self, request, *args, **kwargs):
        entry = self.get_object()
        success_url = self.get_success_url()
        Student.objects.filter(placement_seminar_presentation_date=entry).update(placement_seminar_presentation_date=None)
        Student.seminar_entries.through.objects.filter(seminarentry_id=entry.id).delete()
        connection.cursor().execute("DELETE FROM mentoring_seminarentry WHERE id = %s", [entry.id])
        return HttpResponseRedirect(success_url)


class ThesisSeminarView(View):
    template_name = 'thesis_seminar_list.html'

    def get(self, request):
        context = {'bachelor_seminar_list': Seminar.objects.filter(type=SEMINAR_TYPE_CHOICES[1][0]),
                   'master_seminar_list': Seminar.objects.filter(type=SEMINAR_TYPE_CHOICES[2][0])
                   }
        return render(request, self.template_name, context)


class BachelorSeminarCreateView(CreateView):
    model = Seminar
    template_name = 'seminar_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('thesis-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(BachelorSeminarCreateView, self).get_context_data(**kwargs)
        context['seminar_type'] = SEMINAR_TYPE_CHOICES[1][0]
        return context


class BachelorSeminarUpdateView(UpdateView):
    model = Seminar
    template_name = 'thesis_bachelor_seminar_update.html'
    fields = ['year']

    def get_success_url(self):
        return reverse('thesis-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(BachelorSeminarUpdateView, self).get_context_data(**kwargs)
        students = Student.objects.filter(bachelor_year=self.get_object().year).order_by('matriculation_number')
        entrys = SeminarEntry.objects.filter(seminar=self.get_object().id, seminar__type=SEMINAR_TYPE_CHOICES[1][0]).order_by('date')
        numbers_present_dict = {}

        for student in students:
            numbers_present_dict[student.id] = 0

        for student in students:
            student_entrys = student.seminar_entries.all().filter(seminar__type=SEMINAR_TYPE_CHOICES[1][0])
            for entry in student_entrys:
                if student.id in numbers_present_dict:
                    numbers_present = numbers_present_dict[student.id]
                    numbers_present_dict[student.id] = numbers_present + 1

        context['students'] = students
        context['entrys'] = entrys
        context['numbers_present_dict'] = numbers_present_dict
        return context


class BachelorSeminarEntryProcessView(View):
    @transaction.atomic
    def post(self, request):
        checked_student_entry_list = []
        presentation_done_student_list = []
        checked_student_bachelor_seminar_list = []
        thesis_seminar_id = int(request.POST.get('bachelor_seminar'))
        thesis_seminar = Seminar.objects.get(pk=thesis_seminar_id)
        all_seminar_students = Student.objects.filter(bachelor_year=thesis_seminar.year)
        all_seminar_entrys = SeminarEntry.objects.filter(seminar=thesis_seminar_id)

        for key in request.POST:
            splitted_key = key.split('_')
            if key != 'csrfmiddlewaretoken' and not key.startswith('presentation_done') and key != 'bachelor_seminar' and not key.startswith('bachelor_seminar_done'):
                entry_id = int(splitted_key[0])
                student_id = int(splitted_key[1])
                checked_student_entry_list.append([student_id, entry_id])
            if key.startswith('presentation_done'):
                student_id = int(splitted_key[2])
                presentation_date_id = request.POST.get(key)
                presentation_done_student_list.append([student_id, presentation_date_id])
            if key.startswith('bachelor_seminar_done'):
                student_id = int(splitted_key[3])
                checked_student_bachelor_seminar_list.append(student_id)

        for student in all_seminar_students:
            thesis = student.studentactivethesis.thesis
            for student_presentation in presentation_done_student_list:
                if student.id == student_presentation[0]:
                    presentation_date_id = student_presentation[1]
                    if presentation_date_id:
                        student.bachelor_seminar_presentation_date = SeminarEntry.objects.get(id=int(presentation_date_id))
                    else:
                        student.bachelor_seminar_presentatiton_date = None

            if student.id in checked_student_bachelor_seminar_list:
                student.bachelor_seminar_done = True
                if thesis.state == 'Colloquium completed':
                    thesis.state = 'Seminar completed'
                    if thesis.poster_accepted:
                        thesis.state = 'Poster accepted'
                    thesis.save()
            else:
                student.bachelor_seminar_done = False
                if thesis.mentoring_requested:
                    thesis.state = 'Requested'
                    if thesis.mentoring_accepted == 'MA':
                        thesis.state = 'Mentoring accepted'
                        if thesis.examination_office_state == '1B':
                            thesis.state = 'Examination office submitted'
                        elif thesis.examination_office_state == '2A':
                            thesis.state = 'Examination office accepted'
                            if thesis.thesis:
                                thesis.state = 'Thesis submitted'
                                if thesis.colloquium_done:
                                    thesis.state = 'Colloquium completed'
                    elif thesis.mentoring_accepted == 'MD':
                        thesis.state = 'Mentoring denied'
                else:
                    thesis.state = 'Not requested'
                thesis.save()

            student.save()

            for entry in all_seminar_entrys:
                student_entry = [student.id, entry.id]
                if student_entry in checked_student_entry_list:
                    entry.seminar_students.add(student)
                else:
                    entry.seminar_students.remove(student)
                entry.save()
        return redirect('bachelor-seminar-update', pk=thesis_seminar_id)


class BachelorSeminarEntryCreateView(CreateView):
    model = SeminarEntry
    template_name = 'seminar_entry_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('bachelor-seminar-update', args=[self.object.seminar.id])

    def get_context_data(self, **kwargs):
        context = super(BachelorSeminarEntryCreateView, self).get_context_data(**kwargs)
        context['seminar_id'] = self.request.GET.get('bachelor_seminar')
        return context


class BachelorSeminarEntryDeleteView(DeleteView):
    model = SeminarEntry

    def get_success_url(self):
        return reverse('bachelor-seminar-update', args=[self.get_object().seminar.id])

    def delete(self, request, *args, **kwargs):
        entry = self.get_object()
        success_url = self.get_success_url()
        Student.objects.filter(bachelor_seminar_presentation_date=entry).update(bachelor_seminar_presentation_date=None)
        Student.seminar_entries.through.objects.filter(seminarentry_id=entry.id).delete()
        connection.cursor().execute("DELETE FROM mentoring_seminarentry WHERE id = %s", [entry.id])
        return HttpResponseRedirect(success_url)


class MasterSeminarUpdateView(UpdateView):
    model = Seminar
    template_name = 'thesis_master_seminar_update.html'
    fields = ['year']

    def get_success_url(self):
        return reverse('thesis-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(MasterSeminarUpdateView, self).get_context_data(**kwargs)
        students = Student.objects.filter(master_year=self.get_object().year).order_by('matriculation_number')
        entrys = SeminarEntry.objects.filter(seminar=self.get_object().id, seminar__type=SEMINAR_TYPE_CHOICES[2][0]).order_by('date')
        numbers_present_dict = {}

        for student in students:
            numbers_present_dict[student.id] = 0

        for student in students:
            student_entrys = student.seminar_entries.all().filter(seminar__type=SEMINAR_TYPE_CHOICES[2][0])
            for entry in student_entrys:
                if student.id in numbers_present_dict:
                    numbers_present = numbers_present_dict[student.id]
                    numbers_present_dict[student.id] = numbers_present + 1

        context['students'] = students
        context['entrys'] = entrys
        context['numbers_present_dict'] = numbers_present_dict
        return context


class MasterSeminarCreateView(CreateView):
    model = Seminar
    template_name = 'seminar_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('thesis-seminar-list')

    def get_context_data(self, **kwargs):
        context = super(MasterSeminarCreateView, self).get_context_data(**kwargs)
        context['seminar_type'] = SEMINAR_TYPE_CHOICES[2][0]
        return context


class MasterSeminarEntryProcessView(View):
    @transaction.atomic
    def post(self, request):
        checked_student_entry_list = []
        presentation_done_student_list = []
        checked_student_placement_seminar_list = []
        thesis_seminar_id = int(request.POST.get('master_seminar'))
        thesis_seminar = Seminar.objects.get(pk=thesis_seminar_id)
        all_seminar_students = Student.objects.filter(master_year=thesis_seminar.year)
        all_seminar_entrys = SeminarEntry.objects.filter(seminar=thesis_seminar_id)

        for key in request.POST:
            splitted_key = key.split('_')
            if key != 'csrfmiddlewaretoken' and not key.startswith('presentation_done') and key != 'master_seminar' and not key.startswith('master_seminar_done'):
                entry_id = int(splitted_key[0])
                student_id = int(splitted_key[1])
                checked_student_entry_list.append([student_id, entry_id])
            if key.startswith('presentation_done'):
                student_id = int(splitted_key[2])
                presentation_date_id = request.POST.get(key)
                presentation_done_student_list.append([student_id, presentation_date_id])
            if key.startswith('master_seminar_done'):
                student_id = int(splitted_key[3])
                checked_student_placement_seminar_list.append(student_id)

        for student in all_seminar_students:
            thesis = student.studentactivethesis.thesis
            for student_presentation in presentation_done_student_list:
                if student.id == student_presentation[0]:
                    presentation_date_id = student_presentation[1]
                    if presentation_date_id:
                        student.master_seminar_presentation_date = SeminarEntry.objects.get(id=int(presentation_date_id))
                    else:
                        student.master_seminar_presentation_date = None

            if student.id in checked_student_placement_seminar_list:
                student.master_seminar_done = True
                if thesis.state == 'Colloquium completed':
                    thesis.state = 'Seminar completed'
                    if thesis.poster_accepted:
                        thesis.state = 'Poster accepted'
                    thesis.save()
            else:
                student.master_seminar_done = False
                if thesis.mentoring_requested:
                    thesis.state = 'Requested'
                    if thesis.mentoring_accepted == 'MA':
                        thesis.state = 'Mentoring accepted'
                        if thesis.examination_office_state == '1B':
                            thesis.state = 'Examination office submitted'
                        elif thesis.examination_office_state == '2A':
                            thesis.state = 'Examination office accepted'
                            if thesis.thesis:
                                thesis.state = 'Thesis submitted'
                                if thesis.colloquium_done:
                                    thesis.state = 'Colloquium completed'
                    elif thesis.mentoring_accepted == 'MD':
                        thesis.state = 'Mentoring denied'
                else:
                    thesis.state = 'Not requested'
                thesis.save()
            student.save()

            for entry in all_seminar_entrys:
                student_entry = [student.id, entry.id]
                if student_entry in checked_student_entry_list:
                    entry.seminar_students.add(student)
                else:
                    entry.seminar_students.remove(student)
                entry.save()
        return redirect('master-seminar-update', pk=thesis_seminar_id)


class MasterSeminarEntryCreateView(CreateView):
    model = SeminarEntry
    template_name = 'seminar_entry_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('master-seminar-update', args=[self.object.seminar.id])

    def get_context_data(self, **kwargs):
        context = super(MasterSeminarEntryCreateView, self).get_context_data(**kwargs)
        context['seminar_id'] = self.request.GET.get('master_seminar')
        return context


class MasterSeminarEntryDeleteView(DeleteView):
    model = SeminarEntry

    def get_success_url(self):
        return reverse('master-seminar-update', args=[self.get_object().seminar.id])

    def delete(self, request, *args, **kwargs):
        entry = self.get_object()
        success_url = self.get_success_url()
        Student.objects.filter(master_seminar_presentation_date=entry).update(master_seminar_presentation_date=None)
        entry.seminar_students.remove()
        entry.delete()
        return HttpResponseRedirect(success_url)


def generate_placement_pdf(self, pk):
    placement = Placement.objects.get(id=pk)
    student = placement.student

    context = {
        'BeginnDatum': placement.date_from.strftime('%d.%m.%Y') if placement.date_from else '',
        'EndeDatum': placement.date_to.strftime('%d.%m.%Y') if placement.date_to else '',
        'StudentName': u"%s, %s" % (student.user.last_name, student.user.first_name),
        'MatrNr': student.matriculation_number,
        'Telefon': student.phone,
        'Email': student.user.email,
        'THBBetreuer': u'%s' % placement.tutor,
        'BetriebName': u'%s' % placement.company_name,
        'BetriebBetreuerName': u"%s" % placement.placementcompanycontactdata if placement.placementcompanycontactdata else '',
        'BetriebAnschrift': u"%s" % placement.company_address.replace('\r\n', '<w:br/>'),
        'Aufgabe': u"%s" % placement.task.replace('\r\n', '<w:br/>'),
        'BerichtDatum': u"%s" % placement.report_uploaded_date.strftime('%d.%m.%Y') if placement.report_uploaded_date else '',
        'KollDatum': student.placement_seminar_presentation_date.date.strftime('%d.%m.%Y') if student.placement_seminar_presentation_date else '',
        'AktuellesDatum': datetime.now().strftime("%d.%m.%Y")
    }

    # Pfade zusammensetzen
    template_file = '{mediaroot}/docs/_Anerkennung_Praktikum_2014.docx'.format(mediaroot=settings.MEDIA_ROOT)
    directory = "{}/{}/placement/".format(settings.MEDIA_ROOT, student.matriculation_number)
    filename = '{}-Praktikumsanerkennung.docx'.format(student.matriculation_number)
    output_file = '{directory}/{file}'.format(directory=directory, file=filename)

    # Docx-Datei füllen
    doc = DocxTemplate(template_file)
    doc.render(context)
    doc.save(output_file)

    # Docx-Datei senden, wenn diese erfolgreich erzeugt wurde
    if os.path.exists(output_file):
        with open(output_file, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/docx')
            response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(student_name=student, filename=filename)
            return response
        pdf.closed

    return redirect('index')


class StudentPlacementSeminarEntryView(TemplateView):
    template_name = 'student_placement_seminar_entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentPlacementSeminarEntryView, self).get_context_data(**kwargs)
        entries_list = []

        if hasattr(self.request.user, 'portaluser') and hasattr(self.request.user.portaluser, 'student'):
            student = self.request.user.portaluser.student
            entries_all = SeminarEntry.objects.filter(seminar__year=student.placement_year, seminar__type=SEMINAR_TYPE_CHOICES[0][0])
            entries_present_ids = student.seminar_entries.values_list('id', flat=True)

            # Alle Termine und ob der Student an diesen anwesend war in einer Liste zusammenfassen
            for entry in entries_all:
                entries_list.append((entry, entry.id in entries_present_ids))

            # Kontextvariablen setzen
            context['entries_list'] = entries_list
            context['presentation_date'] = student.placement_seminar_presentation_date
            context['placement_seminar_done'] = student.placement_seminar_done

        return context


class StudentThesisSeminarEntryView(TemplateView):
    template_name = 'student_thesis_seminar_entry_list.html'

    def get_context_data(self, **kwargs):
        context = super(StudentThesisSeminarEntryView, self).get_context_data(**kwargs)

        if hasattr(self.request.user, 'portaluser') and hasattr(self.request.user.portaluser, 'student'):
            student = self.request.user.portaluser.student
            studentactivethesis = student.studentactivethesis.thesis

            # Es werden entweder die Bachelorseminartermine oder die Masterseminartermine aufgelistet, je nachdem was für den Studenten gerade aktuell ist
            if studentactivethesis:
                entries_list = []

                if studentactivethesis.type == THESIS_CHOICES[0][0]:
                    entries_all = SeminarEntry.objects.filter(seminar__year=student.bachelor_year, seminar__type=SEMINAR_TYPE_CHOICES[1][0])
                    context['presentation_date'] = student.bachelor_seminar_presentation_date
                    context['seminar_done'] = student.bachelor_seminar_done
                elif studentactivethesis.type == THESIS_CHOICES[1][0]:
                    entries_all = SeminarEntry.objects.filter(seminar__year=student.master_year, seminar__type=SEMINAR_TYPE_CHOICES[2][0])
                    context['presentation_date'] = student.master_seminar_presentation_date
                    context['seminar_done'] = student.master_seminar_done

                # Alle Termine und ob der Student an diesen anwesend war in einer Liste zusammenfassen
                entries_present_ids = student.seminar_entries.values_list('id', flat=True)
                for entry in entries_all:
                    entries_list.append((entry, entry.id in entries_present_ids))
                context['entries_list'] = entries_list

                # Ob Expose eingereicht
                context['expose'] = studentactivethesis.expose

        return context


class PostersView(View):
    template_name = 'posters_index.html'

    def get(self, request, *args, **kwargs):
        if not self.get_object():
            return redirect('index')
        else:
            theses = Thesis.objects.filter(mentoring_requested=True)
            context = {'theses': theses}
            return render(request, self.template_name, context)

    def get_object(self, queryset=None):
        st = Tutor.objects.filter(user=self.request.user)
        return st[0] if len(st) > 0 else None


class PosterUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        thesis = Thesis.objects.get(id=pk)
        POST = request.POST

        form = FormTutorPoster(POST, instance=thesis)

        if form.is_valid():
            poster_accepted_new_value = form.cleaned_data['poster_accepted']
            if poster_accepted_new_value and form.instance.state == 'Seminar completed':
                form.instance.state = 'Poster accepted'
            else:
                if thesis.mentoring_requested:
                    thesis.state = 'Requested'
                    if thesis.mentoring_accepted == 'MA':
                        thesis.state = 'Mentoring accepted'
                        if thesis.examination_office_state == '1B':
                            thesis.state = 'Examination office submitted'
                        elif thesis.examination_office_state == '2A':
                            thesis.state = 'Examination office accepted'
                            if thesis.thesis:
                                thesis.state = 'Thesis submitted'
                                if thesis.colloquium_done:
                                    thesis.state = 'Colloquium completed'
                                    if thesis.type == 'Bachelor' and thesis.student.bachelor_seminar_done:
                                        form.instance.state = 'Seminar completed'
                                    elif thesis.type == 'Master' and thesis.student.master_seminar_done:
                                        form.instance.state = 'Seminar completed'
                    elif thesis.mentoring_accepted == 'MD':
                        thesis.state = 'Mentoring denied'
                else:
                    thesis.state = 'Not requested'
                thesis.save()
            form.save()
        return redirect('posters-index')


def handler500(request):
    return redirect('login')
