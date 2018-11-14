from time import sleep
from random import random
from unittest import TestCase


class Module1SampleTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        sleep(random())

    @classmethod
    def tearDownClass(cls):
        sleep(random())

    def setUp(self):
        sleep(0.5)

    def test_sample_1(self):
        pass
