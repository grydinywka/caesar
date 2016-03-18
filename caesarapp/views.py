# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
import json

def is_alpha(c):
    c = ord(c)
    if ord('A') <= c and c <= ord('Z'):
        return True
    if ord('a') <= c and c <= ord('z'):
        return True
    return False

def is_upper(c):
    if ord(c) <= ord('Z'):
        return True # If ord('A') <= ord(c) and ord(c) <= ord('Z')
    return False # If ord('a') <= ord(c) and ord(c) <= ord('z')

def shift(c, rot, limit, isCrypte):
    c = ord(c)
    if (isCrypte):
        shift_res = c + rot
        if ( shift_res > limit ):
            shift_res -= 26
    else:
        shift_res = c - rot
        if ( shift_res < limit ):
            shift_res += 26
    return chr(shift_res)

def crypt(str, rot):
    crypted = ''
    for c in str:
        if is_alpha(c):
            if is_upper(c):
                limit = ord('Z')
            else:
                limit = ord('z')
            crypted += shift(c, rot, limit, True)
        else:
            crypted += c
        pass

    return crypted

def encrypt(str, rot):
    encrypted = ''
    for c in str:
        if is_alpha(c):
            if is_upper(c):
                limit = ord('A')
            else:
                limit = ord('a')
            encrypted += shift(c, rot, limit, False)
        else:
            encrypted += c

    return encrypted

def index(request):
    # Якщо форма була запощена:
    if request.method == "POST":
        data = request.POST

        # Перевіряємо дані на коректність та збираємо помилки
        errors = {}
       # Якщо дані були введені не коректно:
            #Віддаємо шаблон форми разом з помилками
        if not errors:
            rotn = int(data['rot']) % 26
        # Якщо дані були введені коректно:
            if request.POST.get("crypt") is not None:
                output_text = crypt(data['input-text'], rotn)
            elif request.POST.get("encrypt") is not None:
                output_text = encrypt(data['input-text'], rotn)
                # pass
            result_dict = {"input-text": str(data['input-text']),	"rot": data['rot'],
                           "output_text": output_text}
            if ( data.has_key("crypt") ):
                result_dict["crypt"] = data['crypt']
            elif ( data.has_key("encrypt") ):
                result_dict["encrypt"] = data['encrypt']
            # Формуємо JSON Відповідь і повертаємо форму, в яку розміщуємо вихідні данні і шифр
            return JsonResponse(result_dict,
                                safe=False)
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