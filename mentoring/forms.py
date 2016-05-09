# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.forms.widgets import DateInput

from mentoring.models import *
from mentoring.widgets import ClearableFileInput

__author__ = 'ullmanfa'


class FormPlacement(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormPlacement, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.mentoring_requested:
            self.fields['task'].widget.attrs['disabled'] = True
            self.fields['tutor'].widget.attrs['disabled'] = True
        if instance.state == 'Placement completed' or instance.state == 'Placement failed':
            self.fields['task'].widget.attrs['disabled'] = True
            self.fields['tutor'].widget.attrs['disabled'] = True
            self.fields['date_from'].widget.attrs['disabled'] = True
            self.fields['date_to'].widget.attrs['disabled'] = True
            self.fields['report'].widget.attrs['disabled'] = True
            self.fields['certificate'].widget.attrs['disabled'] = True
            self.fields['company_name'].widget.attrs['disabled'] = True
            self.fields['company_address'].widget.attrs['disabled'] = True

    def is_valid(self):
        is_valid = super(FormPlacement, self).is_valid()

        if is_valid:
            # Wenn ein neuer Bericht hochgeladen wird, wird ein Zeitestempel gesetzt. Beim Löschen des Berichts wird der Zeitstempel gelöscht.
            if 'report' in self.changed_data:
                if self.cleaned_data['report']:
                    self.instance.report_uploaded_date = datetime.now()
                else:
                    self.instance.report_uploaded_date = None

            self.instance.save()

        return is_valid

    class Meta:
        model = Placement
        exclude = ['student', 'finished', 'sent_on']
        fields = ['tutor', 'task', 'date_from', 'date_to', 'report', 'certificate', 'company_name', 'company_address']
        widgets = {
            'date_from': DateInput(attrs={'class': 'datepicker'}),
            'date_to': DateInput(attrs={'class': 'datepicker'}),
            'report': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class FormThesis(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormThesis, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.mentoring_requested:
            self.fields['type'].widget.attrs['disabled'] = True
            self.fields['task'].widget.attrs['disabled'] = True
            self.fields['tutor'].widget.attrs['disabled'] = True

    def is_valid(self):
        is_valid = super(FormThesis, self).is_valid()

        if is_valid:
            # Wenn ein neuer Bericht hochgeladen wird, wird ein Zeitestempel gesetzt. Beim Löschen des Berichts wird der Zeitstempel gelöscht.
            # if 'report' in self.changed_data:
            #     if self.cleaned_data['report']:
            #         self.instance.report_uploaded_date = datetime.now()
            #     else:
            #         self.instance.report_uploaded_date = None

            self.instance.save()

        return is_valid

    class Meta:
        model = Thesis
        exclude = ['student', 'finished', 'sent_on', 'deadline']
        fields = ['tutor', 'task', 'type', 'second_examiner_first_name', 'second_examiner_last_name', 'second_examiner_organisation', 'second_examiner_title', 'expose', 'thesis', 'poster', 'presentation', 'other']
        widgets = {
            'expose': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'thesis': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'poster': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'presentation': ClearableFileInput(),
            'other': ClearableFileInput(),
        }


class FormTutorPlacement(forms.ModelForm):
    class Meta:
        model = Placement
        exclude = ['student', 'mentoring_requested', 'sent_on', 'tutor', 'task', 'date_from', 'date_to', 'report', 'certificate', 'company_name', 'company_address']
        fields = ['archived', 'mentoring_accepted', 'completed']


class FormTutorThesis(forms.ModelForm):
    class Meta:
        model = Thesis
        exclude = ['student', 'mentoring_requested', 'sent_on', 'tutor', 'task', 'thesis', 'poster', 'presentation', 'other', 'grade_first_examiner', 'grade_second_examiner', 'grade_presentation']
        fields = ['mentoring_accepted', 'examination_office_state', 'deadline', 'archived']
        widgets = {
            'deadline': DateInput(attrs={'class': 'datepicker'}),
        }


FormsetPlacementContactdata = forms.inlineformset_factory(Placement, PlacementCompanyContactData, fields='__all__', extra=1, can_delete=False)


class FormTutorPlacementDetails(forms.ModelForm):
    def is_valid(self):
        is_valid = super(FormTutorPlacementDetails, self).is_valid()

        if is_valid:
            # Wenn ein neuer Bericht hochgeladen wird, wird ein Zeitestempel gesetzt. Beim Löschen des Berichts wird der Zeitstempel gelöscht.
            if 'report' in self.changed_data:
                if self.cleaned_data['report']:
                    self.instance.report_uploaded_date = datetime.now()
                else:
                    self.instance.report_uploaded_date = None

            self.instance.save()

        return is_valid

    class Meta:
        model = Placement
        exclude = ['student', 'tutor', 'number_seminars_present', 'presentation_done', 'mentoring_requested', 'mentoring_accepted', 'archived']
        fields = ['task', 'date_from', 'date_to', 'report', 'certificate', 'company_name', 'company_address', 'report_accepted', 'certificate_accepted']
        widgets = {
            'date_from': DateInput(attrs={'class': 'datepicker'}),
            'date_to': DateInput(attrs={'class': 'datepicker'}),
            'report': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


# Todo FormStudent alternative E-Mail anpassen
class FormSettingsUser(forms.ModelForm):
    class Meta:
        model = MentoringUser
        fields = ['first_name', 'last_name', 'email']


FormsetUserTutor = forms.inlineformset_factory(MentoringUser, Tutor,
                                               fields=['user', 'title', 'phone', 'portaluser_ptr'],
                                               extra=1, can_delete=False)
FormsetUserStudent = forms.inlineformset_factory(MentoringUser, Student,
                                                 fields='__all__',
                                                 extra=1, can_delete=False)
FormsetStudentAddress = forms.inlineformset_factory(Student, Address, fields='__all__', extra=1, can_delete=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
