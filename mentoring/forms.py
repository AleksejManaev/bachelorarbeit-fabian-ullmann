# -*- coding: utf-8 -*-
from django import forms
from django.forms.utils import ErrorList
from mentoring.models import *
from django.utils.translation import ugettext_lazy as _
from mentoring.widgets import ClearableFileInput
from django.forms.widgets import DateInput

__author__ = 'ullmanfa'


# Todo TestForm kann gelöscht werden
class TestForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'length': '100'}), label="Hallo Welt", max_length=100)

    disabled = forms.CharField(label="Hallo Welt", max_length=100,
                               widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    textfield = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(widget=forms.EmailInput(attrs={'icon': 'editor-mode-edit'}))
    password = forms.CharField(widget=forms.PasswordInput)
    file = forms.FileField()
    CHOICES = (('1', 'First',), ('2', 'Second',))
    choice_field = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    radio_select = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    checkboxes = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES)
    checkboxes_input = forms.ChoiceField(widget=forms.CheckboxInput)
    switch = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'switch': 'switch', 'on': 'an', 'off': 'aus'}),
                               choices=CHOICES)
    range = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '100'}))
    integer = forms.IntegerField()
    date = forms.DateField()


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


class FormContactData(forms.ModelForm):
    class Meta:
        model = ContactData
        fields = ['title', 'first_name', 'last_name', 'email', 'phone']


class FormTutor2ContactData(forms.ModelForm):
    class Meta:
        model = Tutor2ContactData
        fields = '__all__'


class FormPlacement(forms.ModelForm):
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
        exclude = ['student', 'finished', 'state', 'sent_on']
        fields = ['course', 'tutor', 'task', 'date_from', 'date_to', 'report', 'certificate']
        widgets = {
            'date_from': DateInput(attrs={'class': 'datepicker'}),
            'date_to': DateInput(attrs={'class': 'datepicker'}),
            'report': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class FormPlacementEventRegistration(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormPlacementEventRegistration, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = self.fields['event'].queryset.filter(course=self.instance.placement.course)

    class Meta:
        model = PlacementEventRegistration
        fields = ['event']
        widgets = {
            'event': forms.RadioSelect(),
        }


class FormEvent(forms.ModelForm):
    class Meta:
        model = PlacementEvent
        fields = ['date', 'time', 'room']


class FormThesisDocuments(forms.ModelForm):
    def is_valid(self):
        """
        Falls das Objekt bereits finalisiert wude -> invalid
        """
        # if (self.instance.finished):
        #     return False

        """
        Falls Thesis-Documents finalisiert werden soll, setze all Felder 'required'
        """

        req = True if self.data.has_key('finalize') and self.data['finalize'] == 'true' else False

        for key, val in self.fields.iteritems():
            if not key in ['public', 'finished']:
                val.required = req
            else:
                val.required = False

        is_valid = super(FormThesisDocuments, self).is_valid()

        """
        Falls Thesis-Documents valid und finalize -> Thesis.finished
        """

        if is_valid and req:
            # self.instance.documents_finished = True
            self.instance.save()

        return is_valid

    class Meta:
        model = Thesis
        exclude = ['student', 'finished', 'sent_on', 'state', 'course', 'documents_finished']
        fields = '__all__'
        widgets = {
            'report': ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'poster': ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class FormThesisMentoringrequest(forms.ModelForm):
    def is_valid(self):
        req = True if self.data.has_key('finalize') else False

        for key, val in self.fields.iteritems():
            val.required = req

        is_valid = super(FormThesisMentoringrequest, self).is_valid()
        return is_valid

    class Meta:
        model = Thesis
        exclude = ['student', 'finished', 'report', 'poster', 'sent_on', 'state', 'documents_finished']
        fields = '__all__'
        widgets = {
            'task': forms.Textarea()
        }


class FormStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


FormsetWorkCompany = forms.inlineformset_factory(AbstractWork, WorkCompany, fields=['address'], extra=1,
                                                 fk_name='work', can_delete=False)
FormsetWorkCompanyContactdata = forms.inlineformset_factory(WorkCompany, CompanyContactData, fields='__all__', extra=1,
                                                            can_delete=False)


class FormMentoringrequestStudent(forms.ModelForm):
    def is_valid(self):
        """
        Falls das Objekt bereits angefragt wurde -> invalid
        """
        if (self.instance.state in ['RE', 'AC']):
            return False

        req = True if self.data.has_key('finalize') else False

        for key, val in self.fields.iteritems():
            val.required = True

        is_valid = super(FormMentoringrequestStudent, self).is_valid()
        return is_valid

    class Meta:
        model = MentoringRequest
        fields = ['tutor_email', 'comment']
        widgets = {
            'comment': forms.Textarea()
        }


class FormMentoringrequestTutor(forms.ModelForm):
    permission = forms.BooleanField()
    permission.required = False

    def is_valid(self):
        # Todo Answer soll bei Accept nicht required sein
        self.fields['answer'].required = True
        return super(FormMentoringrequestTutor, self).is_valid()

    class Meta:
        model = MentoringRequest
        fields = ['answer', 'permission']
        exclude = ['state']


class FormMentoringTutor(forms.ModelForm):
    class Meta:
        model = Mentoring
        fields = '__all__'


FormsetMentoringTutor2 = forms.inlineformset_factory(Mentoring, Tutor2ContactData, fields='__all__', extra=1)


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


class FormRegistration(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['mentoring', 'permission_library_tutor', 'pdf_file', 'finished']


class FormRegistrationExamination(forms.ModelForm):
    class Meta:
        model = ResponseExaminationBoard
        fields = '__all__'
        exclude = ['registration', 'finished']


class FormColloquium(forms.ModelForm):
    class Meta:
        model = Colloquium
        fields = '__all__'
        exclude = ['mentoring']


class FormMentoringReport(forms.ModelForm):
    class Meta:
        model = MentoringReport
        fields = '__all__'
        exclude = ['mentoring']


FormsetReportItems = forms.inlineformset_factory(MentoringReport, MentoringReportItem, fields='__all__', extra=1,
                                                 can_delete=True)
