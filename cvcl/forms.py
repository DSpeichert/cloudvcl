from django.forms import ModelForm, ModelChoiceField
from django.conf import settings
from django import forms
from .models import Assignment, VmDefinition, User, Course
from bootstrap3_datetime.widgets import DateTimePicker
import io
import csv
import re


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'start_date', 'end_date', 'course', 'environment_definition']
        widgets = {
            'start_date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:ss"}),
            'end_date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:ss"})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['course'] = ModelChoiceField(queryset=user.instructs.all())
        self.fields['environment_definition'] = ModelChoiceField(queryset=user.environment_definitions.all())


class VmDefinitionForm(ModelForm):
    class Meta:
        model = VmDefinition
        fields = ['name', 'image', 'flavor', 'shell_script', 'install_packages', 'timezone', 'hostname',
                  'default_user_password', 'default_user_public_key', 'student_user', 'student_user_sudo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # pop the 'user' from kwargs dictionary
        super(VmDefinitionForm, self).__init__(*args, **kwargs)
        self.fields['image'] = ModelChoiceField(queryset=user.images.all())


class CourseUploadCsvForm(forms.Form):
    data_file = forms.FileField()

    def clean_data_file(self):
        f = self.cleaned_data['data_file']
        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('Please upload only csv file')

        return f

    def process_data(self, course_id):
        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)
        for users in reader:
            users = {re.sub("['\"]", "", str(k.encode('ascii', 'ignore')))[1:]: v for k, v in users.items()}
            username = users['Username']
            email = users['Username'] + getattr(settings, "EMAIL_DOMAIN", "")
            user, created = User.objects.get_or_create(username=username)

            if created:
                user.first_name = users['First Name']
                user.last_name = users['Last Name']
                user.email = email
                user.save()

            course = Course.objects.get(id=course_id)
            course.students.add(user)
