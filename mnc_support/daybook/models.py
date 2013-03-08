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
    (0, '未設定'),
    (11,'1限'),
    (22,'2限'),
    (33,'3限'),
    (44,'4限'),
    (55,'5限'),
    (66,'6限'),
    (77,'7限'),
    (88,'オンデマンド'),
    (99,'なし'),
    (12,'1限～2限'),
    (23,'2限～3限'),
    (24,'2限～4限'),
    (25,'2限～5限'),
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

TA_SUPPORT_CHOICES = (
    ('TA','TAが必要'),
    ('SA','SAでも対応可能'),
    ('suspense','受講者数によってサポートが決定'),
    ('none','サポート不要'),
    ('new','未選択'),
)

class ClassInfo(models.Model):
    #科目名 (旧科目名) クラス番号 教員名
    name = models.CharField(max_length=30)
    other_name = models.CharField(max_length=30, blank=True)
    class_number = models.IntegerField()
    teacher = models.CharField(max_length=30)
    #年度 学期
    year = models.IntegerField('開講年度')
    term = models.CharField(choices=TERM_CHOICES, max_length=20)
    #曜日 時限 教室
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, max_length=20)
    hour = models.IntegerField(choices=HOUR_CHOICES)
    classroom = models.CharField(choices=CLASSROOM_CHOICES, max_length=10)

    ta_support = models.CharField(choices=TA_SUPPORT_CHOICES, max_length=10)
    class_key = models.CharField(max_length=12)
    syllabus_url = models.URLField()
    keyword = models.CharField(max_length=200, blank=True)
    #same_class
    #
    #配当年次 単位 定員 ACPA 備考
    #max_user = 
    #detail = models.TextField(blank=True)
    #datetime = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name + str(self.class_number).zfill(2)

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


class Document(models.Model):
    name = models.CharField(max_length=100)
    file_data = models.FileField(upload_to='./upload')


class Lesson(models.Model):
    class_data = models.ForeignKey(ClassInfo)
    date = models.DateField()
    hour = models.IntegerField(choices=HOUR_CHOICES, blank=True, default=0)
    lesson_number = models.IntegerField()
    #user = models.ForeignKey(User)
    attendance_check = models.BooleanField()
    handout = models.BooleanField()

    #今回の授業(授業の内容 受講者とのやりとり)
    contents = models.ManyToManyField(Action, blank=True)
    questions = models.ManyToManyField(Quesiton, blank=True)
    documents = models.ManyToManyField(Document, blank=True)
    #連絡事項(  注意点 先生とのやり取り その他特記事項)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.class_data.name + str(self.lesson_number).zfill(2)

admin.site.register(ClassInfo)
admin.site.register(Lesson)
admin.site.register(Action)
admin.site.register(Quesiton)
admin.site.register(Document)
