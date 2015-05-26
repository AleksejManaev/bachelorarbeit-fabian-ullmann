from django.forms import ModelForm, inlineformset_factory

from materialize.models import MaterializeTestModel, MaterializeForeignModel

__author__ = 'ullmanfa'


class MaterializeTestForm(ModelForm):
    class Meta:
        model = MaterializeTestModel
        fields = '__all__'


class MaterializeForeignForm(ModelForm):
    class Meta:
        model = MaterializeForeignModel
        fields = '__all__'


MaterializeFormset = inlineformset_factory(MaterializeForeignModel, MaterializeTestModel, form=MaterializeTestForm,
                                           fk_name='foreign', extra=1, can_delete=False)
