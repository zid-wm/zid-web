from django.http import HttpResponse
from django.shortcuts import render


def view_test(request):
    return HttpResponse('Hello world!')
