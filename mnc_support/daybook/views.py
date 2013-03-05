# Create your views here.

from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from models import ClassInfo

def index(request):
    return render_to_response('main.html')


def classList(request):
    try:
        #class_info = ClassInfo.objects.get()
        class_info = ClassInfo.objects.all()
    except ClassInfo.DoesNotExist:
        return HttpResponseNotFound(mimetype='application/json')
 
    json = serializers.serialize('json', class_info, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')


def signin(request):
    return render_to_response('signin.html')


def uploader(request):
    return render_to_response('uploader.html')


def signup(request):
    return render_to_response('signup.html')


def signout(request):
    return render_to_response('signout.html')


def hello(request):
    return HttpResponse("Hello, world. You're at the poll index.")
