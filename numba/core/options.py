"""
Target Options
"""

from numba.core import config

class TargetOptions(object):
    OPTIONS = {}

    def __init__(self):
        self.values = {}

    def from_dict(self, dic):
        for k, v in dic.items():
            try:
                ctor = self.OPTIONS[k]
            except KeyError:
                fmt = "%r does not support option: '%s'"
                raise KeyError(fmt % (self.__class__, k))
            else:
                self.values[k] = ctor(v)

    @classmethod
    def parse_as_flags(cls, flags, options):
        opt = cls()
        opt.from_dict(options)
        opt.set_flags(flags)
        return flags

    def set_flags(self, flags):
        """
        Provide default flags setting logic.
        Subclass can override.
        """
        kws = self.values.copy()

        if kws.pop('nopython', False) == False:
            flags.set("enable_pyobject")

        if kws.pop("forceobj", False):
            flags.set("force_pyobject")

        if kws.pop('looplift', True):
            flags.set("enable_looplift")

        if kws.pop('boundscheck', False):
            flags.set("boundscheck")

        if kws.pop('_nrt', True):
            flags.set("nrt")

        if kws.pop('debug', config.DEBUGINFO_DEFAULT):
            flags.set("debuginfo")
            flags.set("boundscheck")

        if kws.pop('nogil', False):
            flags.set("release_gil")

        if kws.pop('no_rewrites', False):
            flags.set('no_rewrites')

        if kws.pop('no_cpython_wrapper', False):
            flags.set('no_cpython_wrapper')

        if 'parallel' in kws:
            flags.set('auto_parallel', kws.pop('parallel'))

        if 'fastmath' in kws:
            flags.set('fastmath', kws.pop('fastmath'))

        if 'error_model' in kws:
            flags.set('error_model', kws.pop('error_model'))

        if 'inline' in kws:
            flags.set('inline', kws.pop('inline'))

        flags.set("enable_pyobject_looplift")

        if kws:
            # Unread options?
            raise NameError("Unrecognized options: %s" % kws.keys())
