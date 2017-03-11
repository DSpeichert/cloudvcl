from django.forms import ModelForm, ModelChoiceField
from .models import Assignment, VmDefinition


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'start_date', 'end_date', 'course', 'environment_definition']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['course'] = ModelChoiceField(queryset=user.instructs.all())
        self.fields['environment_definition'] = ModelChoiceField(queryset=user.environment_definitions.all())


class VmDefinitionForm(ModelForm):
    class Meta:
        model = VmDefinition
        fields = ['name', 'image', 'flavor', 'user_script']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(VmDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['image'] = ModelChoiceField(queryset=user.images.all())
