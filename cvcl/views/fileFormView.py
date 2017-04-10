from django.shortcuts import render
from django.views.generic import FormView, DetailView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from ..forms import ProfileImageForm
from ..models import ProfileImage


class ProfileImageView(FormView):
    template_name = './fileUpload.html'
    form_class = ProfileImageForm

    def form_valid(self, form):
        profile_image = ProfileImage(
            image=self.get_form_kwargs().get('files')['image'])
        profile_image.save()
        self.id = profile_image.id
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile_image', kwargs={'pk': self.id})


class ProfileDetailView(DetailView):
    model = ProfileImage
    template_name = './fileUpload.html'
    context_object_name = 'image'


class ProfileImageIndexView(ListView):
    model = ProfileImage
    template_name = '../fileUpload.html'
    context_object_name = 'images'
    queryset = ProfileImage.objects.all()

# from ..forms import fileForm
# #View current Upload Form
# class DataView(FormView):
#     template_name = 'index.html'
#     form_class = fileForm
#     success_url = '/upload'
#
#     def form_valid(self, form):
#         form.readData()
#         return super().form_valid(form)
