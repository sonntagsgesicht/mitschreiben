mitschreiben
============

.. image:: https://img.shields.io/codeship/f797f980-5b19-0135-2a70-66335668a83b/master.svg
    :target: https://codeship.com//projects/237404

.. image:: https://readthedocs.org/projects/mitschreiben/badge
    :target: http://mitschreiben.readthedocs.io



mitschreiben (german for 'to take notes') helps recording values during
calculations for later evaluation, e.g. check if the right objects or
values were used.

It provides a class called Record which is a contextmanager and the also
the Function to call for recording.

Example Usage
-------------

In the first step one places ``Record`` at the places where one wants to
record a value. The decorator ``Prefix`` provided by this class is used
to define a key under which the recorded value will be stored in the
``Record``. The Prefixes get stacked, so when there is a successive
function call to another function which is prefixed those Prefixes are
concatenated.

.. code:: python

    from mitschreiben import Record

    class Foo():

        @Record.Prefix()
        def bar(self, baz, barz)
            some_value1, some_value2 = self.do_something(baz, barz)

            Record(a_key=some_value1, another_key=some_value2)

            return some_value1, some_value2

        @Record.Prefix()
        def do_something(self, baz, barz):

            a_dict = {'again_a_key': baz, 'so_creative': barz}

            Record(a_dict)

            return magical_stuff_happens(baz, barz)

        def __repr__(self):
            return "Foo({})".format(id(self))

Now, since ``Record`` is a contextmanager, the recording will only
happen in such a context.

.. code:: python

    with Record() as rec:
        foo = Foo()
        foo.do_something("baz", "barz")
        foo.bar("baz","barz")

        print rec.entries

The entries are a dict whose keys are tuples which are the stacked
Prefixes. So one can see from which object which function was called
with which object ... and so forth and that led to the recorded value.

::

    {('Foo(42403656).do_something', 'again_a_key'): 'baz', ('Foo(42403656).bar', 'Foo(42403656).do_something', 'again_a_key'): 'baz', ('Foo(42403656).do_something', 'so_creative'): 'barz', ('Foo(42403656).bar', 'a_key'): "That's", ('Foo(42403656).bar', 'another_key'): 'great', ('Foo(42403656).bar', 'Foo(42403656).do_something', 'so_creative'): 'barz'}

Now this dictionary can be made into *tree of dictionaries*, a
``DictTree``, and from there to tables that are nice for investigation
on the recorded data.

.. code:: python

    from mitschreiben.formatting import DictTree

    DT = DictTree(rec.entries)

    tables = DT.make_tables()
    for t in tables:
        print t.pretty_string()
        print

This results in the following output. The first table represents the top
level of the record, whereas the other tabels are named by
*object.function*.

::

                        Values |  a_key | again_a_key | another_key | so_creative
             Foo(42403656).bar | That's |        None |       great |        None
    Foo(42403656).do_something |   None |         baz |        None |        barz

    Foo(42403656).bar
                        Values | again_a_key | so_creative
    Foo(42403656).do_something |         baz |        barz

The call ``DT.html_tables('FOLDER')`` creates *FOLDER* on the Desktop -
if it isn't already there - and places an *index.html* file into it.
With large tables this leads to nicer results if one wants to have a
look at the record. It will look similiar to the following tables
(depending on the css style)

.. raw:: html

   <!DOCTYPE html>

.. raw:: html

   <html>

.. raw:: html

   <body>

::

        <h4></h4><table style="padding: 1em">

.. raw:: html

   <tr>

::

    <th> </th>
    <th>a_key</th>
    <th>again_a_key</th>
    <th>another_key</th>
    <th>so_creative</th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

::

    <td>Foo(42403656).bar</td>
    <td>That's</td>
    <td>None</td>
    <td>great</td>
    <td>None</td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

::

    <td>Foo(42403656).do_something</td>
    <td>None</td>
    <td>baz</td>
    <td>None</td>
    <td>barz</td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

.. raw:: html

   <h4>

Foo(42403656).bar

.. raw:: html

   </h4>

.. raw:: html

   <table>

.. raw:: html

   <tr>

::

    <th> </th>
    <th>again_a_key</th>
    <th>so_creative</th>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

::

    <td>Foo(42403656).do_something</td>
    <td>baz</td>
    <td>barz</td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

.. raw:: html

   </body>

.. raw:: html

   </html>
