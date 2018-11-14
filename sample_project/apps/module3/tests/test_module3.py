from time import sleep
from unittest import TestCase


class Module3SampleTestCase(TestCase):
    def setUp(self):
        sleep(0.5)

    def test_first_case(self):
        pass

    def test_second_case(self):
        sleep(0.5)
