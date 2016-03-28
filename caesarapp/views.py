# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

def shift(c, rot, limit, isCrypte):
    lenLatin = 26
    c = ord(c)
    if (isCrypte):
        shift_res = c + rot
        if ( shift_res > limit ):
            shift_res -= lenLatin
    else:
        shift_res = c - rot
        if ( shift_res < limit ):
            shift_res += lenLatin
    return chr(shift_res)

def crypt(str, rot):
    crypted = ''
    for c in str:
        if c.isalpha():
            if c.isupper():
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
        if c.isalpha():
            if c.isupper():
                limit = ord('A')
            else:
                limit = ord('a')
            encrypted += shift(c, rot, limit, False)
        else:
            encrypted += c

    return encrypted

def index(request):
    if request.method == "POST":
        # take data from request
        data = request.POST
        # create dict for errors
        errors = {}
        # create dict for output data
        result_dict = {}

        # Validate input-text field
        input_text = data.has_key('input-text') and data["input-text"] or ''
        if not input_text:
            errors['input_text'] = u'Текст для шифрування/дешифрування є обов’язковим!'
        else:
            result_dict['input_text'] = data['input-text']

        # Validate rotate field
        rot = data.has_key('rot') and data['rot'] or ''
        if not rot:
            errors['rot'] = u'Зміщення є обов’язковим!'
        # elif date is not integer or is not number
        else:
            try:
                rot = int(rot)
            except Exception:
                errors['rot'] = u'Невірне значення зміщення! Введіть ціле число!'
            result_dict['rot'] = rot

        result_dict["output_text"] = ''

        if not errors:
            rotn = rot % 26 # 26 - length of latin alphabet
            output_text = ''

            if data.has_key("crypt") and data["crypt"] is not None:
                output_text = crypt(data['input-text'], rotn)
                result_dict["crypt"] = data['crypt']
            elif data.has_key("encrypt") and data["encrypt"] is not None:
                output_text = encrypt(data['input-text'], rotn)
                result_dict["encrypt"] = data['encrypt']

            result_dict["output_text"] = output_text

            return JsonResponse(result_dict, safe=False)
        else: # if there are errors
            result_dict["errors"] = errors

            return JsonResponse(result_dict, safe=False)
    else: # if there is not POST
        return render(request, 'index.html', {})
