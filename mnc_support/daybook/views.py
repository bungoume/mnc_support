# Create your views here.

from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from models import ClassInfo, Lesson

def index(request):
    return render_to_response('main.html')


def classList(request):
    try:
        class_info = ClassInfo.objects.all()
    except ClassInfo.DoesNotExist:
        return HttpResponseNotFound(mimetype='application/json')
    def setData(data):
        data.term = data.get_term_display()
        data.hour = data.get_hour_display()
        data.classroom = data.get_classroom_display()
        data.weekday = data.get_weekday_display()
        data.class_number = str(data.class_number).zfill(2)
        data.ta_support = data.get_ta_support_display()
        return data

    class_info = map(setData, class_info)
    json = serializers.serialize('json', class_info, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')


def showLesson(request, id):
    try:
        class_info = ClassInfo.objects.get(id__exact=id)
    except ClassInfo.DoesNotExist:
        return HttpResponseNotFound(mimetype='application/json')
    #lessons = Lesson.objects.filter(class_data_id__exact=id)
    lessons = class_info.lesson_set.all()
    return render_to_response('lesson.html', {'lessons': lessons, 'class_info':class_info})
    json = serializers.serialize('json', class_info, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')


def updateClassList(request):
    from pyquery import PyQuery as pq
    def is_end(html):
        d = pq(html)
        return d('.next').length == 0
    def extract(html):
        d = pq(html)
        list = []
        for tr in d(''):
            ar = map((lambda input:(input.name[:-2], input.value)),pq(tr).nextAll()[0:8])
            if len(ar) == 8:
                list.append(dict(ar))
        return list
    def fetch(page):
        url = "http://1"
        if(page):
            url += ""
        opener = urllib2.build_opener()
        html = opener.open(url).read()
        return html

    classList = []
    p = 1
    while 1:
        print p
        html = fetch(p)
        classList.extend(extract(html))
        if is_end(html):
            break
        p += 1
        time.sleep(1)
    setClassList(classList)
    return 'ok'


def signup(request):
    return render_to_response('signup.html')


def signout(request):
    return render_to_response('signout.html')


def hello(request):
    return HttpResponse("Hello, world. You're at the poll index.")
