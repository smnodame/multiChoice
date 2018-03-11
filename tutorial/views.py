import json

from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers

from tutorial.models import FormChoice, Student, Point

def index(request):
    return render(request, 'tutorial/index.html')

@api_view(['POST', ])
@csrf_exempt
def create_question(request):
    queryset = FormChoice.objects.create(
        slug = request.data.get("slug", ""),
        name = request.data.get("name", ""),
        description = request.data.get("description", ""),
        time = request.data.get("time", ""),
        question_amount = request.data.get("question_amount", 10),
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
    queryset = Student.objects.filter(year=request.GET["year"], grade=request.GET["grade"], level=request.GET["level"], room=request.GET["room"])
    serializer = StudentSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="application/json")


@api_view(['PUT', ])
@csrf_exempt
def update_question(request):
    FormChoice.objects.filter(slug=request.data.get("slug", "")).update(
        name = request.data.get("name", ""),
        description = request.data.get("description", ""),
        time = request.data.get("time", ""),
        question_amount = request.data.get("question_amount", 10),
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
    subject = serializers.CharField(max_length=5000)
    date = serializers.CharField(max_length=50)
    answers = serializers.CharField(max_length=5000000)

class PointSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=True)

    class Meta:
        model = Point
        fields = ('point', 'slug', 'student', )

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
