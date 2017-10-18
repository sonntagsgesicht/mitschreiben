from inspect import getargspec
from functools import wraps


__all__ = ['Record']


class RecordMeta(type):
    """A MetaClass to allow Record to be used in more universal way"""

    def __call__(cls, *args, **kwargs):
        record = cls.__new__(cls)
        if record.is_started and (args or kwargs):
            record._record(*args, **kwargs)
        return record


class Record(object):
    """
    This class can be used to record values during calculations. The class can be called to do the actual recording.
    Moreover the class grants access to the record depending on the record level and finally it is a contextmanager to
    control whether to record or not.
    """

    __metaclass__ = RecordMeta
    _records = list()
    _record_level = 0

    class Key(tuple):
        """
        Key for the record entries
        """

        def __add__(self, other):
            if isinstance(other, str):
                other = (other,)
            if isinstance(other, list):
                other = tuple(other)
            return Record.Key(super(Record.Key, self).__add__(other))

        def __radd__(self, other):
            if isinstance(other, str):
                other = (other,)
            if isinstance(other, list):
                other = tuple(other)
            return Record.Key(other.__add__(self))

        def __str__(self):
            return '|'.join(map(str, self))

    class _add_prefix_context(object):


        def __enter__(self):
            return self

        def __exit__(self, a, b, c):
            Record().pop_prefix()

    # Public decorator
    class Prefix(object):
        """
        This decorator generates a key extension depending on the method it decorates and the object that is passed
        to that method. This class remembers which methods have been decorated.
        """

        _logged_methods = dict()
        _auto_log_return_value = False
        _Record_Reference = None

        @classmethod
        def logged_methods(cls):
            return cls._logged_methods

        @classmethod
        def autologging(cls, boolean):
            cls._auto_log_return_value = boolean

        def __init__(self, prefix=None):
            self.prefix = prefix

        def __call__(self, function):
            if not isinstance(function, type(lambda x: x)):
                msg = "This Decorator can only be applied to functions. You tried to decorate {}. Changing order of " \
                      "Decorators might resolve the problem".format(type(function))
                raise TypeError(msg)
            if not self.prefix:
                self.prefix = function.__name__

            origin = function.__module__

            BUILTINTYPES = [t for t in __builtins__.values() if isinstance(t, type)]

            @wraps(function)
            def helper(*args, **kwargs):
                if args:
                    if args[0] in BUILTINTYPES or type(args[0]) in BUILTINTYPES:
                        pass
                    elif isinstance(args[0], type):
                        origin = str(args[0])
                    else:
                        origin = str(args[0].__class__)


                Record.Prefix._log_method(origin, function)
                if args:
                    caller = repr(args[0])
                else:
                    caller = origin
                pref = caller + '.' + self.prefix

                with Record().append_prefix(pref):
                    value = function(*args, **kwargs)
                return value
            setattr(helper, 'getargsinspect', getargspec(function))

            return helper

        @classmethod
        def _log_method(cls, origin, function):

            A = cls.logged_methods()
            a = A.get(origin) if A.get(origin) else set()
            a.add(function.__name__)
            A[origin] = a

    def __new__(cls):

        if cls._records and len(cls._records)-1 == cls._record_level:
            instance = cls._records[-1]
        else:
            new_instance = super(Record, cls).__new__(cls)
            new_instance._entries = dict()
            new_instance._prefix_stack = list()
            new_instance._started = False
            new_instance._level = cls._record_level
            cls._records.append(new_instance)
            instance = new_instance
        return instance

    @property
    def is_started(self):
        """Returns a bool whether the Record is started or not. If False, Record(*args, **kwargs) has no effect."""
        return self._started

    @property
    def entries(self):
        """returns a dictionary with Recordkeys and Values"""
        return self._entries

    def clear(self):
        """this method clears the entries of a Record instance. Since there is only one toplevel Record instance everything
        is recorded there during its lifetime."""
        self._entries.clear()

    def start(self):
        self._started = True

    def stop(self):
        """"""
        self._started = False

    def append_prefix(self, prefix):
        """extend the current prefix stack by the prefix. If used as contextmanager the prefix will be removed outside
        of the context"""
        self._prefix_stack.append(prefix)
        return Record._add_prefix_context()

    def pop_prefix(self):
        "remove the last extension from the prefix stack"
        return self._prefix_stack.pop()

    def _add_entry(self, key_word, value):
        key = Record.Key(self._prefix_stack) + key_word
        self._entries[key] = value

    def _record(self, *args, **kwargs):
        """This method is invoked when calling Record(*args, **kwargs) and 'Record().is_started'. Arguments can be a dict containing values
        to be recorded and keys that are used to build the keys of the record together with the prefix stack.
        kwargs are used just as a dict which was passed as argument."""
        for arg in [arg for arg in args if isinstance(arg, dict)]:
            for key, value in arg.items():
                self._add_entry(key, value)
        for key, value in kwargs.items():
            self._add_entry(key, value)

    def __enter__(self):
        cls = self.__class__
        cls._record_level += 1
        rec = cls()
        rec.start()
        return rec

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        rec = self.__class__._records.pop()
        if self.__class__._record_level > 0:
            self.__class__._record_level -= 1
            Record()._extend(rec)


    def _extend(self, other):
        """A (sub)record can be united with its (parent)record by extending the subrecordkeys with the present state
        of the parentrecordkeys"""
        for key, value in other.entries.items():
            self._add_entry(key, value)

    def __str__(self):
        return "Record({})".format(self._level)













