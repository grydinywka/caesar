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