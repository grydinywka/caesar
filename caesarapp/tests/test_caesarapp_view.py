# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class TestCrypt(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def test_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # check page title, few field titles on edit form
        self.assertIn(u'Зашифрувати', response.content)
        self.assertIn(u'Розшифрувати', response.content)
        self.assertIn(u'Зміщення', response.content)
        self.assertIn('name="crypt"', response.content)
        self.assertIn('name="encrypt"', response.content)
        self.assertIn('action="%s"' % self.url, response.content)

    def test_crypt_post(self):
        response = self.client.post(self.url, {
            'input-text': 'My name!',
            'rot': '2',
            'crypt': '1'
            },
            follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'Oa pcog!')
        self.assertEqual(response.json()['input_text'], u'My name!')
        self.assertEqual(response.json()['rot'], 2)
        self.assertEqual(response.json()['crypt'], u'1')

        # check unicode
        response = self.client.post(
            self.url,
            {
                'input-text': u'Стовідсотковий спирт',
                'rot': '29',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'Стовідсотковий спирт')
        self.assertEqual(response.json()['input_text'], u'Стовідсотковий спирт')
        self.assertEqual(response.json()['rot'], 29)
        self.assertEqual(response.json()['crypt'], u'1')

        # check unicode-latin mix
        response = self.client.post(
            self.url,
            {
                'input-text': u'Wine is not beer! Стовідсотковий спирт',
                'rot': '29',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'Zlqh lv qrw ehhu! Стовідсотковий спирт')
        self.assertEqual(response.json()['input_text'], u'Wine is not beer! Стовідсотковий спирт')
        self.assertEqual(response.json()['rot'], 29)
        self.assertEqual(response.json()['crypt'], u'1')

        # check negative rotate
        response = self.client.post(
            self.url,
            {
                'input-text': u'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG',
                'rot': '-3',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD')
        self.assertEqual(response.json()['input_text'], u'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG')
        self.assertEqual(response.json()['rot'], -3)
        self.assertEqual(response.json()['crypt'], u'1')

        # check big data to crypt
        simpletext = open('caesarapp/static/txt/copperfield.txt', 'r')
        crypttext = open('caesarapp/static/txt/copperfield_rot2.txt', 'r')
        response = self.client.post(
            self.url,
            {
                'input-text': simpletext.read(),
                'rot': '2',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], crypttext.read())
        simpletext.seek(0)
        self.assertEqual(response.json()['input_text'], simpletext.read())
        self.assertEqual(response.json()['rot'], 2)
        self.assertEqual(response.json()['crypt'], u'1')

        # check no text-input
        response = self.client.post(
            self.url,
            {
                'input-text': '',
                'rot': '33',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'')
        self.assertEqual(response.json()['errors']['input_text'], u'Текст для шифрування/дешифрування є обов’язковим!')
        self.assertEqual(response.json()['rot'], 33)
        self.assertEqual(response.json()['crypt'], u'1')

        # check one character text-input
        response = self.client.post(
            self.url,
            {
                'input-text': 'G',
                'rot': '33',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'N')
        self.assertEqual(response.json()['input_text'], u'G')
        self.assertEqual(response.json()['rot'], 33)
        self.assertEqual(response.json()['crypt'], u'1')

        # check no rotation
        response = self.client.post(
            self.url,
            {
                'input-text': 'Hello, Babby!',
                'rot': '',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'')
        self.assertEqual(response.json()['errors']['rot'], u'Зміщення є обов’язковим!')
        self.assertEqual(response.json()['crypt'], u'1')

        # check one rotation
        response = self.client.post(
            self.url,
            {
                'input-text': 'Hello, Babby!',
                'rot': '1',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'Ifmmp, Cbccz!')
        self.assertEqual(response.json()['input_text'], u'Hello, Babby!')
        self.assertEqual(response.json()['rot'], 1)
        self.assertEqual(response.json()['crypt'], u'1')

        # check zero rotation
        response = self.client.post(
            self.url,
            {
                'input-text': 'Hello, Babby!',
                'rot': '0',
                'crypt': '1'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['output_text'], u'Hello, Babby!')
        self.assertEqual(response.json()['input_text'], u'Hello, Babby!')
        self.assertEqual(response.json()['rot'], 0)
        self.assertEqual(response.json()['crypt'], u'1')


