# -*- coding: utf-8 -*-

# mitschreiben
# ------------
# Python library supplying a tool to record values during calculations
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.3, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/mitschreiben
# License:  Apache License 2.0 (see LICENSE file)


from datetime import datetime
import unittest
import os
import sys

sys.path.append('.')
sys.path.append('..')

from mitschreiben import Record


# dummy functions and classes to test Record and Prefix


def magical_stuff_happens(baz, barz):
    return "That's", "great"


class Foo():
    def __init__(self, name):
        self.name = name

    @Record.Prefix()
    def bar(self, baz, barz):
        some_value1, some_value2 = self.do_something(baz, barz)
        Record(a_key=some_value1, another_key=some_value2)
        return some_value1, some_value2

    @Record.Prefix()
    def do_something(self, baz, barz):
        a_dict = {'again_a_key': baz, 'so_creative': barz}
        Record(a_dict)
        return magical_stuff_happens(baz, barz)

    def __repr__(self):
        return "Foo({})".format(self.name)


def do_stuff():
    with Record() as rec:
        foo = Foo("Rom")
        foo.do_something("baz", "barz")
        foo.bar("baz", "barz")


# Test section


class PrefixTest(unittest.TestCase):
    def setUp(self):
        Record().clear()

    def test_decoration_memory(self):
        do_stuff()
        decorated_functions = {'{}.Foo'.format(__name__): {'do_something', 'bar'}}
        self.assertEqual(Record.Prefix.logged_methods(), decorated_functions)

    def test_Prefix_decorator(self):
        baz = 'baz'
        barz = 'barz'
        name = 'fara'

        with Record() as rec:
            foo = Foo(name)
            foo.do_something(baz, barz)
            foo.bar(baz, barz)

        assumed_record_entries = {('Foo({}).do_something'.format(name), 'again_a_key'): baz,
                                  ('Foo({}).do_something'.format(name), 'so_creative'): barz,
                                  ('Foo({}).bar'.format(name), 'Foo({}).do_something'.format(name), 'again_a_key'): baz,
                                  (
                                  'Foo({}).bar'.format(name), 'Foo({}).do_something'.format(name), 'so_creative'): barz,
                                  ('Foo({}).bar'.format(name), 'a_key'): "That's",
                                  ('Foo({}).bar'.format(name), 'another_key'): "great"}
        self.assertEqual(Record().entries, assumed_record_entries)

    def test_multilevel_record_append_prefix_context(self):
        with Record() as R1:
            with Record().append_prefix('level2'):
                self.assertEqual(Record()._prefix_stack, ['level2'])
                with Record() as R2a:
                    self.assertEqual(Record()._prefix_stack, [])
                    Record(level=Record._record_level, name='R2a')

                    self.assertEqual(Record().entries, {('level',): 2, ('name',): 'R2a'})
                self.assertNotEqual(Record(), R2a)
                self.assertEqual(Record(), R1)
                with Record().append_prefix('another_prefix'):
                    self.assertEqual(Record()._prefix_stack, ['level2', 'another_prefix'])
                    with Record() as R2b:
                        self.assertEqual(Record()._prefix_stack, [])
                        Record(recorded='just something')
                        self.assertEqual(Record().entries, {('recorded',): 'just something'})

                self.assertEqual(Record()._prefix_stack, ['level2'])
            self.assertEqual(Record()._prefix_stack, [])

        assumed_record_entries = {('level2', 'level'): 2,
                                  ('level2', 'name'): 'R2a',
                                  ('level2', 'another_prefix', 'recorded'): 'just something'}
        self.assertEqual(Record().entries, assumed_record_entries)


class RecordTest(unittest.TestCase):
    """Testing Basic Functionality"""

    def setUp(self):
        Record().clear()

    def test_call_to_RecordClass_not_started(self):
        value = 'value'
        a_dict = {'a_key': 'a_value'}

        Record(key=value)
        self.assertEqual(Record().entries, dict())
        Record(a_dict)
        self.assertEqual(Record().entries, dict())
        Record(a_dict, key=value)
        self.assertEqual(Record().entries, dict())

    def test_call_to_RecordClass_start_stop(self):
        value = 'value'

        a_dict = {'a_key': 'a_value'}
        b_dict = {'b_key': 'b_value'}

        Record().start()
        Record(key=value)
        self.assertEqual(Record().entries, {('key',): 'value'})
        Record(a_dict)
        self.assertEqual(Record().entries, {('key',): 'value', ('a_key',): 'a_value'})
        Record().stop()
        Record(b_dict, INT=12345)
        self.assertEqual(Record().entries, {('key',): 'value', ('a_key',): 'a_value'})

    def test_Record_as_context(self):
        a_dict = {'a_key': 'a_value'}
        Record(a_dict, key='value')
        self.assertEqual(Record().entries, dict())

        with Record() as R:
            Record(a_dict)
            self.assertEqual(Record().entries, {('a_key',): 'a_value'})
            self.assertEqual(R, Record())

        self.assertEqual(R.entries, {('a_key',): 'a_value'})

    def test_record_of_RecordObject(self):
        value = 'value'

        a_dict = {'a_key': 'a_value'}
        b_dict = {'b_key': 'b_value'}

        R = Record()
        R._record(key=value)
        self.assertEqual(Record().entries, {('key',): 'value'})
        R._record(a_dict)
        self.assertEqual(Record().entries, {('key',): 'value', ('a_key',): 'a_value'})
        R._record(b_dict, INT=12345)
        self.assertEqual(Record().entries,
                         {('key',): 'value', ('a_key',): 'a_value', ('b_key',): 'b_value', ('INT',): 12345})

    def test_multilevel_record_context(self):
        R1 = Record()
        R2 = Record()
        self.assertEqual(R1, R2)
        with Record() as R1:
            with Record() as R2a:
                self.assertNotEqual(R1, R2a)
                self.assertEqual(Record(), R2a)
            with Record() as R2b:
                self.assertNotEqual(R1, R2b)
                self.assertEqual(Record(), R2b)
            self.assertNotEqual(R2a, R2b)


if __name__ == "__main__":
    import sys

    start_time = datetime.now()

    print('')
    print('======================================================================')
    print('')
    print(('run %s' % __file__))
    print(('in %s' % os.getcwd()))
    print(('started  at %s' % str(start_time)))
    print('')
    print('----------------------------------------------------------------------')
    print('')

    suite = unittest.TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = unittest.TextTestRunner(stream=sys.stdout, descriptions=2, verbosity=2)
    testrunner.run(suite)

    print('')
    print('======================================================================')
    print('')
    print(('ran %s' % __file__))
    print(('in %s' % os.getcwd()))
    print(('started  at %s' % str(start_time)))
    print(('finished at %s' % str(datetime.now())))
    print('')
    print('----------------------------------------------------------------------')
    print('')
