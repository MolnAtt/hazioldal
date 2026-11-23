from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase

from app_naplo.models import Dolgozat
from app_naplo.templatetags.csoportnaplo_templatefilters import jegy2class


class CsoportnaploCompatibilityTests(SimpleTestCase):
    def test_jegyertek_none_and_dash_are_missing(self):
        self.assertIsNone(Dolgozat.jegyertek(None))
        self.assertIsNone(Dolgozat.jegyertek('-'))

    def test_jegy2class_handles_none_and_preserves_grades(self):
        self.assertEqual(jegy2class(None), '')
        self.assertEqual(jegy2class('5'), '5')
        self.assertEqual(jegy2class('4/5'), '45')
        self.assertEqual(jegy2class('1'), '1')

    def test_ok_alapjan_igy_all_skips_none_and_dash_but_keeps_zero_point_grade(self):
        tanulo = object()

        missing_none = SimpleNamespace(
            suly=1,
            sulyvektor=[1],
            ertekeles=lambda user: {'jegy': None},
            matrixaban_tanulo_sorindexe=lambda user: 0,
        )
        missing_dash = SimpleNamespace(
            suly=1,
            sulyvektor=[1],
            ertekeles=lambda user: {'jegy': '-'},
            matrixaban_tanulo_sorindexe=lambda user: 0,
        )
        zero_point = SimpleNamespace(
            suly=2,
            sulyvektor=[1],
            ertekeles=lambda user: {'jegy': '1'},
            matrixaban_tanulo_sorindexe=lambda user: 0,
        )

        with patch.object(Dolgozat.objects, 'filter', return_value=SimpleNamespace(order_by=lambda *args: [missing_none, missing_dash, zero_point])):
            result = Dolgozat.ok_alapjan_igy_all(tanulo, object(), object(), object())

        self.assertEqual(result['atlag'], 1.0)
        self.assertEqual(result['db'], 2)
