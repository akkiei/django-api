from django.test import TestCase

from .calc import add


class CalcTest(TestCase):

    def test_add(self):
        """ this will test the add function """
        self.assertEqual(add(2, 4), 6)
