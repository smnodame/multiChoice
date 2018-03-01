import json

from django.core import serializers
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from tutorial.models import FormChoice

def index(request):
    return render(request, 'tutorial/index.html')

@api_view(['GET', 'POST', ])
@csrf_exempt
def create_question(request):
    form = FormChoice.objects.create(
        slug = request.data.get("slug", ""),
        name = request.data.get("name", ""),
        description = request.data.get("description", ""),
        time = request.data.get("time", ""),
        question_amount = request.data.get("question_amount", 10),
        subject = request.data.get("subject", ""),
        date = request.data.get("date", ""),
        answers = request.data.get("answers", "")
    )
    data = serializers.serialize('json', [form,])

    struct = json.loads(data)
    data = json.dumps(struct[0]['fields'])

    return Response(json.loads(data), status=status.HTTP_201_CREATED, content_type="application/json")


@api_view(['GET', 'POST', ])
@csrf_exempt
def get_question(request):
    form = FormChoice.objects.get(slug=request.GET["slug"])
    data = serializers.serialize('json', [form,])

    struct = json.loads(data)
    data = json.dumps(struct[0]['fields'])

    return Response(json.loads(data), status=status.HTTP_200_OK, content_type="application/json")
