from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Temperature
from django.utils import timezone
import datetime as dt
import os

from django.conf import settings
from django.conf.urls.static import static
from .forms import ReportForm

from django.http import JsonResponse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):
    return render(request, 'home.html')

def report_list(request):
	reports = Report.objects.all()
	return render(request, 'mydashboard/report_list.html', {'reports': reports})

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    temperatures = Temperature.objects.filter(report_id = pk)
    return render(request, 'mydashboard/report_detail.html', {'report': report , 'temperatures': temperatures})

def get_and_create():
  input_excel = os.path.join(settings.MEDIA_ROOT, 'mydashboard/data.csv')
  f = open(input_excel, 'r')
  nLine = 2
  lines = f.readlines()[nLine-1:]
  del lines[0]
  id_max = Report.objects.latest('id').id
  for line in lines:
    array =  line.split(',')
    ligne = Temperature()
    ligne.report_id = id_max + 1
    ligne.temperature = int(array[1])
    ligne.registered_date = dt.datetime.strptime(array[2][:20], ' %Y-%m-%d %H:%M:%S')
    ligne.save()
  f.close()

def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = timezone.now()
            get_and_create()
            report.save()
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm()
    return render(request, 'mydashboard/report_edit.html', {'form': form})

# def report_edit(request, pk):
#     report = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = ReportForm(request.POST, instance=report)
#         if form.is_valid():
#             report = form.save(commit=False)
#             report.author = request.user
#             report.published_date = timezone.now()
#             report.save()
#             return redirect('report_detail', pk=report.pk)
#     else:
#         form = ReportForm(instance=report)
#     return render(request, 'mydashboard/report_edit.html', {'form': form})

class ChartData(APIView):
    def get(self, request, format=None):
        labels = []
        default_items =[]
        lines = Temperature.objects.all()
        for line in lines:
          labels.append(line.registered_date)
          default_items.append(line.temperature)
        data = {
          "labels": labels,
          "default": default_items,
        }
        return Response(data)
