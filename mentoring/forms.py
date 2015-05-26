from django import forms

from mentoring.models import *

__author__ = 'ullmanfa'


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


class FormThesisInvitation(forms.Form):
    desc = forms.CharField(label="Thema beschreiben", max_length=1000, widget=forms.Textarea(attrs={'length': '1000'}))
    company = forms.CharField(label="Unternehmen beschreiben")


class FormThesisRegistration(forms.Form):
    pass


class FormThesisFinalization(forms.Form):
    upload_thesis = forms.FileField(label="Abschlussarbeit hochladen")
    upload_poster = forms.FileField(label="Poster hochladen")


class FormCompany(forms.ModelForm):
    validate = False

    class Meta:
        model = Company
        fields = '__all__'


class FormContactModel(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'


class FormPlacement(forms.ModelForm):
    finish = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)

    class Meta:
        model = Placement
        exclude = ['student', 'finished']
        include = ['finish']
        fields = '__all__'
        widgets = {
            'report': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'presentation': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'certificate': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }


class FormThesis(forms.ModelForm):
    class Meta:
        model = Thesis
        exclude = ['student']
        fields = '__all__'
        widgets = {
            'finished': forms.HiddenInput()
        }


FormsetWorkCompany = forms.inlineformset_factory(AbstractWork, WorkCompany, fields=['description'], extra=1,
                                                 fk_name='work', can_delete=False)
FormsetWorkCompanyContactdata = forms.inlineformset_factory(WorkCompany, ContactData, fields='__all__', extra=1,
                                                            can_delete=True);
# FormsetMentoringRequest = forms.inlineformset_factory(Thesis, Mentoring, fields=['tutor_email', 'comment'], extra=1, can_delete=False)

class FormMentoringRequest(forms.ModelForm):
    class Meta:
        model = MentoringRequest
        fields = ['tutor_email', 'comment']


class FormTutorRequest(forms.ModelForm):
    class Meta:
        model = MentoringRequest
        fields = ['answer']
        exclude = ['status']
