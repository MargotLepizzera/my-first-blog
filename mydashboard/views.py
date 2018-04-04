from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Report, Temperature
from django.utils import timezone
import datetime as dt
import time
import os

from django.conf import settings
from django.conf.urls.static import static
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from microfs import ls, rm, put, get, get_serial
from django.db.models import Avg


def home(request):
    return render(request, 'home.html')

@login_required
def report_list(request):
    user = request.user
    reports = Report.objects.filter(author__id=user.id)

    return render(request, 'mydashboard/report_list.html', {'reports': reports, 'user': user})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    temperatures = Temperature.objects.filter(report_id = pk)
    data = round(Temperature.objects.filter(report_id = pk).aggregate(Avg('temperature'))['temperature__avg'], 1)
    return render(request, 'mydashboard/report_detail.html', {'report': report , 'temperatures': temperatures, 'data': data})

def get_and_create():
  fichier = 'data.csv'
  get(fichier, target=None, serial=None)
  input_excel = os.path.join(settings.MEDIA_ROOT, 'data.csv')
  f = open(input_excel, 'r')
  nLine = 2
  lines = f.readlines()[nLine-1:]
  del lines[0]
  if Report.objects.count() == 0:
    id_max = 0
  else:
    id_max = Report.objects.latest('id').id
  for line in lines:
    array =  line.split(',')
    ligne = Temperature()
    ligne.report_id = id_max + 1
    ligne.temperature = int(array[1])
    index = line.index(",") + 6
    millis = line[index:]
    ligne.registered_date = dt.datetime.now(timezone.utc) + dt.timedelta(milliseconds = -float(millis))
    ligne.save()
  f.close()


@login_required
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

def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.published_date = timezone.now()
            report.save()
            return redirect('report_detail', pk=report.pk)
    else:
        form = ReportForm(instance=report)
    return render(request, 'mydashboard/report_edit.html', {'form': form})

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

