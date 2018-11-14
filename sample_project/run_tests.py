from unittest_timing import TimingTestRunner
from unittest.loader import TestLoader


suite = TestLoader().discover('apps')
runner = TimingTestRunner()
runner.run(suite)
