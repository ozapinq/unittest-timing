# encoding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

import re
import unittest
import types
import threading

from time import time


thread_local = threading.local()
thread_local.results = []


def add_result(name, result):
    thread_local.results.append((name, result))


def outputTimingResults(stream, tree):
    sep1 = '=' * 70
    sep2 = '-' * 70

    header = "\n{}\nTiming results\n{}\n".format(sep1, sep2)

    results = []
    max_name_len = 0
    for key in sorted(tree.keys()):
        value = tree[key]
        key_parts = key.split('.')
        parts_count = len(key_parts) - 1
        key = key_parts[-1]
        key = ' ' * parts_count + key

        if len(key) > max_name_len:
            max_name_len = len(key)

        if isinstance(value, list):
            if len(value) == 1:
                results.append((key, value[0]))
            else:
                values_sum = sum(value)
                if not values_sum:
                    continue
                results.append((key, values_sum))
        else:
            results.append((key, value))

    max_name_len += 5
    format_string = '{:.<%s} {}s\n' % max_name_len
    output = header
    for result in results:
        output += format_string.format(*result)
    output += '\n' + sep2 + '\n'

    stream.write(output)


def timed(name, func):
    def timed_wrapper(*args, **kwargs):
        start = time()
        if args and isinstance(args[0], type):
            args = args[1:]
        result = func(*args, **kwargs)
        end = time()
        elapsed = round(end - start, 2)

        fname = name or func.__name__
        add_result(fname, elapsed)

        return result
    return timed_wrapper


class TimingTestResult(unittest.TextTestResult):
    def startTest(self, test):
        self._started_at = time()
        return super(TimingTestResult, self).startTest(test)

    def stopTest(self, test):
        elapsed = round(time() - self._started_at, 2)
        name = self.getDescription(test).split('\n')[0]
        name = re.sub(r'([^\s]+) \((.+)\)', r'\2.\1', name)
        add_result(name, elapsed)
        super(TimingTestResult, self).stopTest(test)

    def stopTestRun(self):
        self.results = self._buildResultsTree(thread_local.results)
        self.formatter(self.stream, self.results)

        return super(TimingTestResult, self).stopTestRun()

    def _buildResultsTree(self, results):
        tree = {}

        def build(element, elapsed_time, top=False):
            if element not in tree:
                tree[element] = [elapsed_time] if top else elapsed_time
            else:
                if top:
                    tree[element].append(elapsed_time)
                else:
                    tree[element] += elapsed_time
            try:
                left, right = element.rsplit('.', 1)
            except ValueError:
                return
            else:
                return build(left, elapsed_time)

        for (element, elapsed_time) in results:
            build(element, elapsed_time, top=True)

        return tree


class TimingTestRunner(unittest.TextTestRunner):
    resultclass = TimingTestResult
    formatter = None

    wrapped_methods = ('setUp', 'tearDown')
    wrapped_classmethods = ('setUpClass', 'tearDownClass', 'setUpData')

    def _makeResult(self):
        result = super(TimingTestRunner, self)._makeResult()
        result.formatter = self.formatter or outputTimingResults
        return result

    def _wrap(self, test, method_name):
        method = getattr(test, method_name, None)
        if not method:
            return

        cls = test.__class__
        full_name = '.'.join([cls.__module__, cls.__name__, method_name])

        patch_name = method_name + '_patched'
        patched = getattr(test, patch_name, False)

        if not patched:
            if method_name in self.wrapped_methods:
                new_method = timed(full_name, method)
                setattr(test, method_name, new_method)
                setattr(test, patch_name, True)
            else:
                new_method = types.MethodType(
                    timed(full_name, method), test.__class__)
                setattr(cls, method_name, new_method)
                setattr(cls, patch_name, True)

    def traverse(self, suite):
        if issubclass(suite.__class__, unittest.TestCase):
            for method in self.wrapped_methods + self.wrapped_classmethods:
                self._wrap(suite, method)
        else:
            for test in suite:
                self.traverse(test)

    def run(self, suite):
        self.traverse(suite)
        super(TimingTestRunner, self).run(suite)
