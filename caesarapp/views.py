import os, redis

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import ugettext as _

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

def getRot(word, redis_db):
    attempt_rot = 1
    while attempt_rot < 26: # 26 characters in Eng alphabet
        encrypted = allcrypt(word, attempt_rot, False)
        if redis_db.sismember('setEn', encrypted):
            return attempt_rot
        attempt_rot += 1
    return 0

def index(request):
    if request.method == "POST":
        data = request.POST
        if not data.has_key('ajax-msg'):
            # take data from request
            # create dict for errors
            errors = {}
            # create dict for output data
            result_dict = {}

            # Validate input-text field
            input_text = data.has_key('input-text') and data["input-text"] or ''
            if not input_text:
                errors['input_text'] = _(u'Text is required!')
            else:
                result_dict['input_text'] = data['input-text']

            # Validate rotate field
            rot = data.has_key('rot') and data['rot'] or ''
            if not rot:
                errors['rot'] = _(u'Bias is required!')
            # elif date is not integer or is not number
            else:
                try:
                    rot = int(rot)
                except Exception:
                    errors['rot'] = _(u'Incorrect bias! Type integer!')
                result_dict['rot'] = rot

            result_dict["output_text"] = ''

            if data.has_key("crypt") and data["crypt"] is not None:
                crypt = True
                result_dict["crypt"] = data['crypt']
            elif data.has_key("encrypt") and data["encrypt"] is not None:
                crypt = False
                result_dict["encrypt"] = data['encrypt']

            if not errors:
                rotn = rot % 26 # 26 - length of latin alphabet
                result_dict["output_text"] = allcrypt(data['input-text'], rotn, crypt)

                return JsonResponse(result_dict, safe=False)
            else: # if there are errors
                result_dict["errors"] = errors

                return JsonResponse(result_dict, safe=False)
        # If it is request during outfocus from input-text
        if data.has_key('ajax-msg'):
            import string
            # r = redis.StrictRedis(host='localhost', port=6379, db=0)
            # redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
            r = redis.from_url(redis_url)

            res_string = 'res_string'

            textdata = data['textdata'] # get data from input-text
            textdata = textdata.lower()
            punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
            textdata = [item.strip(punctuation) for item in textdata.split()] # now textdata - is list of input words

            counter_word = 0
            for item in textdata:
                if r.sismember('setEn', item) == True:
                    counter_word += 1

            length_of_data = len(textdata)
            if length_of_data == 0:
                res_string = False
            elif counter_word == length_of_data:
                res_string = _(u"It isn't encrypted text! Every word is word of English language.")
            elif counter_word == 0:
                rotate = getRot(textdata[0], r)
                if rotate > 0: # if word is crypted
                    count_crypted = 1
                    i = 1
                    while i < length_of_data:
                        encrypted = allcrypt(textdata[i], rotate, False)
                        if r.sismember('setEn', encrypted) == True:
                            count_crypted += 1
                        i += 1
                    if count_crypted == length_of_data:
                        res_string = _(u"Text encrypted in ROT{}").format(rotate)
                    else:
                        res_string = _(u"{} words encrypted in ROT{}, rest or have errors, "\
                                       u"or encrypted " \
                                     u"in other way").format(count_crypted, rotate)
                else:
                    res_string = _(u"Unable to determine the encryption of the text!")
            else: # 0 < counter_word < length_of_data
                res_string = _(u"Typed text consist of {} words, rest {} - not in the dictionary.").format(
                    counter_word, length_of_data - counter_word)

            return JsonResponse({'result': res_string}, safe=False)
    else: # if there is not POST and is not GET
        return render(request, 'index.html', {})

def second(request):
    return JsonResponse({'result': 'result_dict'}, safe=False)
    
def diagr(request):
	return render(request, 'diagr.html', {})
