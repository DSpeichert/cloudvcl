from django.forms import ModelForm, ModelChoiceField
from .models import Assignment, VmDefinition
import io
from django import forms
import csv

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


class fileForm():
    tempFile = forms.FileField()

    def checkData(self):
        f = self.cleaned_data['tempfile']

        if f:
            end = f.name.split('.')[-1]
            if end != 'csv':
                raise forms.ValidationError('Only accept csv files')

    def readData(self):
        f = io.TextIOWrapper(self.cleaned_data['tempFile'].file)
        reader = csv.DictReader(f)

        for row in reader:
            print(row)

            # def checkData(self):
            #     f= self.cleaned_data['tempfile']
            #
            #     #check if file type is a csv file
            #     if f:
            #         end = f.name.split('.')[-1]
            #         if end != 'csv':
            #             raise forms.ValidationError('Only accept csv files')
            #
            # def readData(self):
            #     f = io.TextIOWrapper(self.cleaned_data['tempFile'].file)
            #     reader = csv.DictReader(f)
            #
            #     #print row in csv file
            #     for row in reader:
            #         print(row)


class ProfileImageForm(forms.Form):
    image = forms.FileField(label="Select a file")
