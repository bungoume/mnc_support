# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.

TERM_CHOICES = (
    ('all','通年'),
    ('previous','前期'),
    ('later','後期'),
    ('summer','夏期集中'),
    ('spring','春季集中'),
    ('others','その他'),
)

WEEKDAY_CHOICES = (
    (0,'日曜'),
    (1,'月曜'),
    (2,'火曜'),
    (3,'水曜'),
    (4,'木曜'),
    (5,'金曜'),
    (6,'土曜'),
    (9,'なし'),
)

#start-stop
HOUR_CHOICES = (
    (11,'1限'),
    (22,'2限'),
    (33,'3限'),
    (44,'4限'),
    (55,'5限'),
    (66,'6限'),
    (77,'7限'),
    (88,'オンデマンド'),
    (99,'なし'),
)

CLASSROOM_CHOICES = (
    ('24_A','24号館Aルーム'),
    ('24_B','24号館Bルーム'),
    ('24_C','24号館Cルーム'),
    ('24_D','24号館Dルーム'),
    ('24_E','24号館Eルーム'),
    ('14_601','14号館601教室'),
    ('14_602','14号館602教室'),
    ('14_603','14号館603教室'),
)

class ClassInfo(models.Model):
    #科目名 (旧科目名) クラス番号 教員名
    name = models.CharField(max_length=30)
    other_name = models.CharField(max_length=30, blank=True)
    class_number = models.IntegerField(blank=True)
    teacher = models.CharField(max_length=20)
    #年度 学期 曜日 時限 教室
    year = models.IntegerField()
    term = models.CharField(choices=TERM_CHOICES, max_length=20)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, max_length=20)
    hour = models.IntegerField(choices=HOUR_CHOICES)
    classroom = models.CharField(choices=CLASSROOM_CHOICES, max_length=10)

    #same_class
    #
    #配当年次 単位 定員 ACPA 備考
    #max_user = 
    #detail = models.TextField(blank=True)
    #datetime = models.DateTimeField(auto_now=True)

TIMING_CHOICES = (
    ('before_class','授業前'),
    ('in_class','授業中'),
    ('after_class','授業後'),
    ('content','授業内容'),
    ('handoff','引き継ぎ'),
    ('for_mnc_message','MNCへの連絡'),
    ('cautions','注意事項'),
    ('communications','先生とのやり取り'),
    ('othres','その他特記事項特記事項'),
)

class Action(models.Model):
    timing = models.CharField(choices=TIMING_CHOICES, max_length=20)
    detail = models.TextField()


class Quesiton(models.Model):
    question = models.TextField()
    response = models.TextField()


class Lesson(models.Model):
    class_data = models.ForeignKey(ClassInfo)
    date = models.DateField()
    hour = models.IntegerField(choices=HOUR_CHOICES, blank=True)
    lesson_number = models.IntegerField()
    #user = models.ForeignKey(User)
    attendance_check = models.BooleanField()
    handout = models.BooleanField()

    #今回の授業(授業の内容 受講者とのやりとり)
    contents = models.ManyToManyField(Action, blank=True)
    questions = models.ManyToManyField(Quesiton, blank=True)

    #連絡事項(  注意点 先生とのやり取り その他特記事項)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



admin.site.register(ClassInfo)
admin.site.register(Lesson)
admin.site.register(Action)
