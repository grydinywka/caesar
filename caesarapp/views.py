# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
import json

def crypt(str):
    pass
def encrypt(str):
    pass

def index(request):
    # Якщо форма була запощена:
    if request.method == "POST":
        # Перевіряємо дані на коректність та збираємо помилки
        errors = {}
       # Якщо дані були введені не коректно:
            #Віддаємо шаблон форми разом з помилками
        if not errors:
        # Якщо дані були введені коректно:
            if request.POST.get("crypt") is not None:
            # Якщо кнопка "шифрувати"  була натиснута:
                 #Проводимо шифрування
                crypt(request.POST['input-text'])
            elif request.POST.get("encrypt") is not None:
            # Якщо кнопка "Розшифрувати" була натиснута
                #Проводимо розшифрування
                encrypt(request.POST['input-text'])

            # Формуємо JSON Відповідь і повертаємо форму, в яку розміщуємо вихідні данні і шифр
            return JsonResponse({"code": "GrateBritain",	"value": 34, "name": "a"}, safe=False)
            # return HttpResponse('<h1>{0}!</h1>'.format(request.POST['input-text']))
        else: # if there are errors
            return render(request, 'index.html', {'errors': errors})
    else: # if there is not POST
        return render(request, 'index.html', {})

def diagr(request):
    return render(request, 'diagr.html', {})

def data_response(request):
    new_http_request = {"code": "GrateBritain", "value": 34, "name": "a"}
    return JsonResponse(new_http_request, safe=False)