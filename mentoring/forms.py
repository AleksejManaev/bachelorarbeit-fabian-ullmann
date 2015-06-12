# -*- coding: utf-8 -*-
from django import forms
from django.forms.utils import ErrorList

from mentoring.models import *

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
        if not self['name'].value():
            return False
        else:
            self.instance = Company.objects.get_or_create(name=self['name'].value())[0]
            self.instance.save()
            if self.parent:
                self.parent.company = self.instance
                self.parent.save()
            return super(FormCompany, self).is_valid()

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
        """
        Falls das Objekt bereits finalisiert wude -> invalid
        """
        if (self.instance.finished):
            return False

        """
        Falls Placement finalisiert werden soll, setze all Felder 'required'
        """

        req = True if self.data.has_key('finalize') and self.data['finalize'] == 'true' else False

        for key, val in self.fields.iteritems():
            if not key in ['public', 'finished']:
                val.required = req
            else:
                val.required = False

        is_valid = super(FormPlacement, self).is_valid()

        """
        Falls Placement valid und finalize -> Placement.finished
        """

        if is_valid and req:
            self.instance.finished = True
            print(self.instance.finished)
            self.instance.save()

        return is_valid

    class Meta:
        model = Placement
        exclude = ['student', 'finished']
        fields = '__all__'
        widgets = {
            'report': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'presentation': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }

class FormThesis(forms.ModelForm):
    def is_valid(self):
        req = True if self.data.has_key('finalize') else False

        for key, val in self.fields.iteritems():
            val.required = req

        is_valid = super(FormThesis, self).is_valid()
        return is_valid

    class Meta:
        model = Thesis
        exclude = ['student', 'finished']
        fields = '__all__'
        widgets = {
            'description': forms.Textarea()
        }

FormsetWorkCompany = forms.inlineformset_factory(AbstractWork, WorkCompany, fields=['description'], extra=1,
                                                 fk_name='work', can_delete=False)
FormsetWorkCompanyContactdata = forms.inlineformset_factory(WorkCompany, CompanyContactData, fields='__all__', extra=1,
                                                            can_delete=False)

class FormMentoringrequestStudent(forms.ModelForm):
    def is_valid(self):
        """
        Falls das Objekt bereits angefragt wurde -> invalid
        """
        if (self.instance.status in ['RE', 'AC']):
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
        exclude = ['status']

class FormMentoringTutor(forms.ModelForm):
    class Meta:
        model = Mentoring
        fields = '__all__'

FormsetMentoringTutor2 = forms.inlineformset_factory(Mentoring, Tutor2ContactData, fields='__all__', extra=1)

# Todo FormStudent alternative E-Mail anpassen
class FormSettings(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


FormsetUserPortaluser = forms.inlineformset_factory(User, PortalUser, fields='__all__', extra=1, can_delete=False)
FormsetStudentAddress = forms.inlineformset_factory(Student, Address, fields='__all__', extra=1, can_delete=False)


class FormRegistration(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['mentoring', 'permission_library_tutor', 'pdf_file']


class FormRegistrationExamination(forms.ModelForm):
    class Meta:
        model = ResponseExaminationBoard
        fields = '__all__'
        exclude = ['registration']
