from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.core.serializers import serialize
from geoQuakesapp.models import Quake, QuakePredictions
from django.template.context import Context
import pandas as pd

def quake_dataset(request):
    quakes = serialize('json', Quake.objects.order_by("ID")[:1000])
    return HttpResponse(quakes, content_type='json')

def quake_dataset_pred(request):
    quakes_pred = serialize('json', QuakePredictions.objects.all()[:1000])
    return HttpResponse(quakes_pred, content_type='json')

def quake_dataset_pred_risk(request):
    quake_risk = serialize('json', QuakePredictions.objects.filter(Magnitude__gt=6.5))
    return HttpResponse(quake_risk, content_type='json')

def home(request):
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page'
        }
    )
