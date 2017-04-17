from django.shortcuts import render
from django.views.generic import FormView, DetailView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import csv
import io

from ..forms import UploadFileForm
from ..models import User


# class DataView(FormView):
# template_name = 'fileUpload.html'
# form_class = DataForm
# success_url = '/upload2/'
#
# def form_valid(self, form):
#     form.process_data()
#     return super().form_valid(form)
def addreport(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # reader = csv.reader(form.cleaned_data['file'])
            # reader = io.TextIOWrapper(temreader)
            # temp = self.cleaned_data['data_file']
            reader = io.TextIOWrapper((form.cleaned_data['file']).file)
            # print(reader.read())
            y = []
            x = reader.readlines()
            for line in x:
                y.append(line.split(','))
            return render(request, 'fileUpload.html', {'form': form, 'content': y})

        else:
            print
            form.errors
            print
            request.FILES
            # form = UploadFileForm()
    else:
        form = UploadFileForm()

    return render(request, 'fileUpload.html', {'form': form})
    # return render(request,'fileUpload.html',{'form': form, 'content':reader})

# def handle_csv_data(csv_file):
#     csv_file = io.TextIOWrapper(csv_file)
#     dialect = csv.Sniffer().sniff(csv_file.read(1024), delimiters=";,")
#     csv_file.seek(0)
#     reader = csv.reader(csv_file, dialect)
#     return list(reader)
#
#
# def upload_csv(request):
#     csv_content = []
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES['file'].file
#             csv_content = handle_csv_data(csv_file)
#     return render(request, 'fileUpload.html', {'content': csv_content})
