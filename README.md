# unittest-timing
Python unittest runner with test timing (including setUp, tearDown, setUpClass, tearDownClass)

## Installation

```shell
$ git clone https://github.com/ozaPiNq/unittest-timing.git
$ cd unittest-timing && python setup.py install
```

## Usage

```python
from unittest_timing.runner import TimingTestRunner
from unittest.loader import TestLoader

suite = TestLoader().discover('.')
runner = TimingTestRunner()
runner.run(suite)
```

## Example output

```
======================================================================
Timing results
----------------------------------------------------------------------
apps.......................... 5.61s
 module1...................... 2.04s
  tests....................... 2.04s
   test_module1............... 2.04s
    Module1SampleTestCase..... 2.04s
     setUp.................... 0.5s
     setUpClass............... 0.7s
     tearDown................. 0.0s
     tearDownClass............ 0.34s
     test_sample_1............ 0.5s
 module2...................... 1.02s
  tests....................... 1.02s
   test_module2............... 1.02s
    Module2SampleTestCase..... 1.02s
     setUp.................... 0.51s
     setUpClass............... 0.0s
     tearDown................. 0.0s
     tearDownClass............ 0.0s
     test_sample_2............ 0.51s
 module3...................... 2.55s
  tests....................... 2.55s
   test_module3............... 2.55s
    Module3SampleTestCase..... 2.55s
     setUp.................... 1.02s
     setUpClass............... 0.0s
     tearDownClass............ 0.0s
     test_first_case.......... 0.51s
     test_second_case......... 1.02s

----------------------------------------------------------------------
```
