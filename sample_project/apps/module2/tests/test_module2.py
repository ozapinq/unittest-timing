from time import sleep
from unittest import TestCase


class Module2SampleTestCase(TestCase):
    def setUp(self):
        sleep(0.5)

    def test_sample_2(self):
        """test with docstring"""
