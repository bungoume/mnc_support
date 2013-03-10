# -*- coding: utf-8 -*-
# Create your views here.

from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from models import ClassInfo, Lesson

def index(request):
    return render_to_response('main.html')



def editDayBook(request):
    return render_to_response('editDayBook.html')


def _setData(data):
    data.term = data.get_term_display()
    data.hour = data.get_hour_display()
    data.classroom = data.get_classroom_display()
    data.weekday = data.get_weekday_display()
    data.class_number = str(data.class_number).zfill(2)
    data.ta_support = data.get_ta_support_display()
    return data


def classList(request):
    try:
        class_info = ClassInfo.objects.all()
    except ClassInfo.DoesNotExist:
        return HttpResponseNotFound(mimetype='application/json')

    class_info = map(_setData, class_info)
    json = serializers.serialize('json', class_info, ensure_ascii=False)
    return HttpResponse(json, mimetype='application/json')


def showLesson(request, id):
    try:
        class_info = ClassInfo.objects.get(id__exact=id)
    except ClassInfo.DoesNotExist:
        return HttpResponseNotFound(mimetype='application/json')
    #lessons = Lesson.objects.filter(class_data_id__exact=id)
    lessons = class_info.lesson_set.all()
    class_info = _setData(class_info)
    return render_to_response('lesson.html', {'lessons': lessons, 'class_info':class_info})


#crawler
def updateClassList(request):
    from pyquery import PyQuery as pq
    
    def getSyllabusData(url):
        html = fetch(url)
        d = pq(html)
        td = d('.ct-sirabasu:first td')
        classroom = td.eq(8).text()

        obj = {
            'name': td.eq(2).find('div').text(),
            'other_name' : '',
            'class_number' : int(td.eq(11).text()),
            'teacher' : td.eq(3).text(),
            #年度 学期
            'year' : int(td.eq(0).text()[:4]),
            'term' : 'previous' if td.eq(4).text().find(u'春') != -1 else 'later',
            #曜日 時限 教室
            'weekday' : td.eq(4).text(),
            'hour' : td.eq(4).text(),
            'classroom' : classroom,
            'ta_support' : '',
            'class_key' : int(td.eq(10).text()),
            'syllabus_url' : url,
            'keyword' : ''
        }
        print obj
        return obj

    def getSyllabusUrlList():
        url = "http://www.waseda.jp/mnc/SYLLABUS/2012/kamoku_list.html"
        html = fetch(url)
        d = pq(html)
        return map(lambda x: pq(x).attr("href"), d('a.external'))


    def fetch(url):
        import urllib2, time
        opener = urllib2.build_opener()
        html = opener.open(url).read()
        time.sleep(1)
        return html

    urlList = getSyllabusUrlList()
    syllabusList = map(getSyllabusData, urlList[:10])
    import json
    f = open('text.txt', 'w') # 書き込みモードで開く
    f.write(json.dumps(syllabusList)) # 引数の文字列をファイルに書き込む
    f.close()
    return 'ok'


def signout(request):
    return render_to_response('signout.html')


def hello(request):
    return HttpResponse("Hello, world. You're at the poll index.")
