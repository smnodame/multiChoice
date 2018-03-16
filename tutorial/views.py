import json
import pdfkit

from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers

from tutorial.models import FormChoice, Student, Point

def index(request):
    return render(request, 'tutorial/index.html')

def qrcode(request):
    return render(request, 'qrcode/index.html')

def send_pdf(request):
    pdf = pdfkit.from_url("http://192.168.1.39:8000/form-pdf?slug={}".format(request.GET.get("slug")), False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example_file.pdf"'

    return response

def form_pdf(request):
    data = model_to_dict(FormChoice.objects.get(slug=request.GET.get("slug")))
    return render(request, 'form_pdf/index.html', {
        'data': data,
        'answers': json.loads(data['answers'])
    })

@api_view(['POST', ])
@csrf_exempt
def create_question(request):
    queryset = FormChoice.objects.create(
        slug = request.data.get("slug", ""),
        name = request.data.get("name", ""),
        description = request.data.get("description", ""),
        time = request.data.get("time", ""),
        question_amount = request.data.get("question_amount", 10),
        answer_amount = request.data.get("answer_amount", 4),
        subject = request.data.get("subject", ""),
        date = request.data.get("date", ""),
        answers = request.data.get("answers", "")
    )
    serializer = FormSerializer(queryset)

    return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="application/json")


@api_view(['GET', ])
@csrf_exempt
def get_question(request):
    queryset = FormChoice.objects.get(slug=request.GET["slug"])
    serializer = FormSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")


@api_view(['GET', ])
@csrf_exempt
def get_student(request):
    queryset = Student.objects.all()

    if request.GET.get("year", False):
        queryset = queryset.filter(year=request.GET["year"])

    if request.GET.get("grade", False):
        queryset = queryset.filter(grade=request.GET["grade"])

    if request.GET.get("level", False):
        queryset = queryset.filter(level=request.GET["level"])

    if request.GET.get("room", False):
        queryset = queryset.filter(room=request.GET["room"])

    if request.GET.get("firstname", False):
        queryset = queryset.filter(firstname__contains=request.GET["firstname"])

    if request.GET.get("lastname", False):
        queryset = queryset.filter(lastname__contains=request.GET["lastname"])

    # queryset = Student.objects.filter(year=request.GET["year"], grade=request.GET["grade"], level=request.GET["level"], room=request.GET["room"])
    serializer = StudentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")


# @csrf_exempt
@api_view(['PUT', ])
def update_question(request):
    FormChoice.objects.filter(slug=request.data.get("slug", "")).update(
        name = request.data.get("name", ""),
        description = request.data.get("description", ""),
        time = request.data.get("time", ""),
        question_amount = request.data.get("question_amount", 10),
        answer_amount = request.data.get("answer_amount", 4),
        subject = request.data.get("subject", ""),
        date = request.data.get("date", ""),
        answers = request.data.get("answers", "")
    )

    return Response(status=status.HTTP_204_NO_CONTENT)

class StudentSerializer(serializers.Serializer):
    slug = serializers.CharField(max_length=50)
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    year = serializers.CharField(max_length=100)
    grade = serializers.CharField(max_length=100)
    level = serializers.CharField(max_length=100)
    room = serializers.CharField(max_length=50)

class FormSerializer(serializers.Serializer):
    slug = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=5000)
    description = serializers.CharField(max_length=5000)
    time = serializers.CharField(max_length=5000)
    question_amount = serializers.IntegerField()
    answer_amount = serializers.IntegerField()
    subject = serializers.CharField(max_length=5000)
    date = serializers.CharField(max_length=50)
    answers = serializers.CharField(max_length=5000000)

class PointSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=True)
    form = FormSerializer(required=True)

    class Meta:
        model = Point
        fields = ('point', 'slug', 'student', 'form')

@api_view(['GET', ])
def get_forms(request):
    queryset = FormChoice.objects.all()
    serializer = FormSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")

@api_view(['DELETE', ])
def delete_question(request):
    queryset = FormChoice.objects.get(slug=request.GET["slug"])
    queryset.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', ])
def get_point(request):
    point_lists = Point.objects.filter(form__slug=request.GET["slug"])
    serializer = PointSerializer(point_lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")

@api_view(['GET', ])
def get_point_form_student(request):
    point_lists = Point.objects.filter(student__slug=request.GET["slug"])
    serializer = PointSerializer(point_lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")
