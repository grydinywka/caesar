# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

def is_alpha(c):
    c = ord(c)
    if ord('A') <= c and c <= ord('Z'):
        return True
    if ord('a') <= c and c <= ord('z'):
        return True
    return False

def shift(c, rot, isCrypte):
    lenLatin = 26
    if (isCrypte):
        if c.isupper():
            limit = ord('Z')
        else:
            limit = ord('z')
        shift_res = ord(c) + rot
        if ( shift_res > limit ):
            shift_res -= lenLatin
    else:
        if c.isupper():
            limit = ord('A')
        else:
            limit = ord('a')
        shift_res = ord(c) - rot
        if ( shift_res < limit ):
            shift_res += lenLatin
    return chr(shift_res)

def allcrypt(str, rot, crypt=True):
    result = ''
    for c in str:
        if is_alpha(c):
            result += shift(c, rot, crypt)
        else:
            result += c

    return result

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

            if data.has_key("crypt") and data["crypt"] is not None:
                crypt = True
                result_dict["crypt"] = data['crypt']
            elif data.has_key("encrypt") and data["encrypt"] is not None:
                crypt = False
                result_dict["encrypt"] = data['encrypt']

            result_dict["output_text"] = allcrypt(data['input-text'], rotn, crypt)

            return JsonResponse(result_dict, safe=False)
        else: # if there are errors
            result_dict["errors"] = errors

            return JsonResponse(result_dict, safe=False)
    else: # if there is not POST
        return render(request, 'index.html', {})
