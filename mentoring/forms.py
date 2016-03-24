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
            self.fields['course'].widget.attrs['disabled'] = True
            self.fields['task'].widget.attrs['disabled'] = True
            self.fields['tutor'].widget.attrs['disabled'] = True

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
        fields = ['course', 'tutor', 'task', 'date_from', 'date_to', 'report', 'certificate', 'company_name',
                  'company_address']
        widgets = {
            'date_from': DateInput(attrs={'class': 'datepicker'}),
            'date_to': DateInput(attrs={'class': 'datepicker'}),
            'report': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class FormTutorPlacement(forms.ModelForm):
    def is_valid(self):
        is_valid = super(FormTutorPlacement, self).is_valid()
        return is_valid

    class Meta:
        model = Placement
        exclude = ['student', 'finished', 'mentoring_requested', 'sent_on', 'course', 'tutor', 'task', 'date_form', 'date_to',
                   'report', 'certificate', 'company_name', 'company_address']
        fields = ['placement_completed', 'mentoring_accepted']


FormsetPlacementContactdata = forms.inlineformset_factory(Placement, PlacementCompanyContactData, fields='__all__',
                                                          extra=1, can_delete=False)


# Todo FormStudent alternative E-Mail anpassen
class FormSettingsUser(forms.ModelForm):
    class Meta:
        model = MentoringUser
        fields = ['first_name', 'last_name', 'email']


FormsetUserTutor = forms.inlineformset_factory(MentoringUser, Tutor,
                                               fields=['user', 'title', 'phone', 'placement_courses', 'portaluser_ptr'],
                                               extra=1, can_delete=False,
                                               widgets={'placement_courses': forms.CheckboxSelectMultiple()})
FormsetUserStudent = forms.inlineformset_factory(MentoringUser, Student,
                                                 fields='__all__',
                                                 extra=1, can_delete=False)
FormsetStudentAddress = forms.inlineformset_factory(Student, Address, fields='__all__', extra=1, can_delete=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
