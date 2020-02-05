from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.core.serializers import serialize
from geoQuakesapp.models import Quake
from django.template.context import Context
import pandas as pd

def quake_dataset(request):
    quakes = serialize('json', Quake.objects.order_by("ID")[:1000])
    return HttpResponse(quakes, content_type='json')

def home(request):
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page'
        }
    )
