# -*- coding: utf-8 -*-
from datetime import datetime

from django import http
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
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


class StudentFormView(StudentPlacementFormView):
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

            return render(request, self.template_name, self.get_context_data())
            # return super(UpdateView, self).get(request, *args, **kwargs)

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
            tutor_user_formset=FormsetUserTutor(data=data, instance=self.get_object().user,
                                                prefix='tutor_user_formset')
        )

    def get_object(self, queryset=None):
        return self.request.user.portaluser.tutor


class TutorPlacementView(UpdateView):
    model = Placement
    fields = ['student', 'course', 'task', 'date_from', 'date_to', 'report', 'certificate', 'company_name',
              'company_address']
    template_name = 'tutor_placement_details.html'
    exclude = ['tutor', 'number_seminars_present', 'presentation_done', 'mentoring_requested', 'mentoring_accepted',
               'placement_completed']

    def get_success_url(self):
        return reverse('placement-details', args=[self.object.id])


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
            return HttpResponseNotFound()

    def post(self, request, pk):
        # Nur der beteiligte Student und Tutor dürfen Kommentare schreiben
        if self.is_placement_allowed(pk):
            comment = Comment()
            comment.author = self.request.user.portaluser.user
            comment.abstract_work = AbstractWork.objects.get(id=pk)
            comment.message = request.POST.get('message')

            private = request.POST.get('private')
            if private is None:
                private = False
            comment.private = private

            comment.save()

            return redirect('placements-comments', pk=pk)
        else:
            return HttpResponseNotFound()

    def is_placement_allowed(self, pk):
        return Placement.objects.filter(Q(id=pk), Q(student=self.request.user.portaluser) | Q(tutor=self.request.user.portaluser)).exists()


def togglePrivacy(request):
    id = request.POST.get('id')
    comment = Comment.objects.get(pk=id)
    private_text = ''

    if comment.private:
        comment.private = False
        private_text = 'Not private'
    else:
        comment.private = True
        private_text = 'Private'

    comment.save()

    return JsonResponse({'private_state': comment.private, 'private_text': str(_(private_text))})


class PlacementSeminarListView(ListView):
    model = PlacementSeminar
    template_name = 'placement_seminar_list.html'


class PlacementSeminarCreateView(CreateView):
    model = PlacementSeminar
    template_name = 'placement_seminar_create.html'
    fields = '__all__'

    # def form_valid(self, form):

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
            for student_presentation in presentation_done_student_list:
                if student.id == student_presentation[0]:
                    presentation_date_id = student_presentation[1]
                    if presentation_date_id:
                        student.presentation_date = PlacementSeminarEntry.objects.get(id=int(presentation_date_id))
                    else:
                        student.presentation_date = None

            if student.id in checked_student_placement_seminar_list:
                student.placement_seminar_done = True
            else:
                student.placement_seminar_done = False
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
