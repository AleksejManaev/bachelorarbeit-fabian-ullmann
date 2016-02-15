# -*- coding: utf-8 -*-
from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import DateInput

from mentoring.models import *
from mentoring.widgets import ClearableFileInput

__author__ = 'ullmanfa'


class FormCompany(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, parent=None):
        self.parent = parent
        super(FormCompany, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                                          initial=initial, error_class=error_class, label_suffix=label_suffix,
                                          empty_permitted=empty_permitted, instance=instance)

    def is_valid(self):
        # TODO Validierung implementieren
        return True

        # if not self['name'].value():
        #     return False
        # else:
        #     self.instance = Company.objects.get_or_create(name=self['name'].value())[0]
        #     self.instance.save()
        #     if self.parent:
        #         self.parent.company = self.instance
        #         self.parent.save()
        #     return super(FormCompany, self).is_valid()

    class Meta:
        model = Company
        fields = '__all__'


class FormPlacement(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormPlacement, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.mentoring_accepted == 'MA':
            self.fields['task'].widget.attrs['disabled'] = True
            self.fields['tutor'].widget.attrs['disabled'] = True

    def is_valid(self):
        # """
        # Falls das Objekt bereits finalisiert wurde -> invalid
        # """
        # if (self.instance.finished):
        #     return False
        #
        # """
        # Falls Placement finalisiert werden soll, setze all Felder 'required'
        # """
        #
        # req = True if self.data.has_key('finalize') and (
        # self.data['finalize'] == 'true' or self.data['finalize'] == _('Finish')) else False
        # for key, val in self.fields.iteritems():
        #     if not key in ['public', 'finished']:
        #         val.required = req
        #     else:
        #         val.required = False

        is_valid = super(FormPlacement, self).is_valid()

        # """
        # Falls Placement valid und finalize -> Placement.finished
        # """

        # if is_valid and req:
        if is_valid:
            # self.instance.finished = True
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
        fields = ['number_seminars_present', 'presentation_done', 'placement_completed', 'mentoring_accepted']


FormsetWorkCompany = forms.inlineformset_factory(Thesis, WorkCompany, fields=['address'], extra=1,
                                                 fk_name='work', can_delete=False)
FormsetWorkCompanyContactdata = forms.inlineformset_factory(WorkCompany, CompanyContactData, fields='__all__', extra=1,
                                                            can_delete=False)

FormsetPlacementContactdata = forms.inlineformset_factory(Placement, PlacementCompanyContactData, fields='__all__',
                                                          extra=1, can_delete=False)


# Todo FormStudent alternative E-Mail anpassen
class FormSettingsUser(forms.ModelForm):
    class Meta:
        model = MentoringUser
        fields = ['first_name', 'last_name']


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
