from django.shortcuts import render
from django.http import HttpResponse
import time

def hello(request):
    for i in range(10):
        print(i)
        # time.sleep(1)
    return HttpResponse('hello Django')