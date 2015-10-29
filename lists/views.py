from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

def home_page(request):
    return HttpResponse('<html><title>Lista rzeczy do zrobienia</title></html>')
# Create your views here.
