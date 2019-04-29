from collections import defaultdict
from contextlib import contextmanager
from contextlib import suppress
from datetime import datetime
import functools
import inspect
import pathlib
import sys
import ast

CACHES = {'files': {}, 'modules': {}}


class Found(Exception):
    pass


class Tracer:
    """Tracer object.

    Implement tracing logic, calls write function with a result dict
    """

    def __init__(self, target, write, max_depth=1):
        self.write = write
        self.target = target
        self.max_depth = max_depth
        self.frame_caches = defaultdict(dict)

    @functools.lru_cache()
    def get_source(self, frame):
        """Get source from frame"""
        with suppress(ImportError, AttributeError, KeyError):
            module = frame.f_globals['__name__']
            source = CACHES['modules'].get(
                module,
                frame.f_globals.get('__loader__').get_source(module).
                splitlines())
            CACHES['modules'][module] = source
            return source

        with suppress(OSError, IOError):
            file_src = frame.f_code.co_filename
            source = CACHES['files'].get(
                file_src,
                pathlib.Path(file_source).read_text().splitlines())
            CACHES['files'][file_src] = source
            return source

    def get_ast(self, frame_source):
        """get ast from frame source"""
        return ast.parse('\n'.join(frame_source))

    def trace(self, frame, event, arg):
        """Trace."""

        def find_in_tree(ast_, lineno):
            """Find a line number in ast tree"""
            for elem in ast_.body:
                if elem.lineno == lineno:
                    exc = Found()
                    exc.elem = elem
                    raise exc
                if hasattr(elem, "body"):
                    find_in_tree(elem, lineno)

        result = {'depth': 0}
        frame_source = self.get_source(frame)

        if frame.f_code is not self.target.__code__:
            _frame = frame
            for depth in range(1, self.max_depth):
                # Try to find original parent amongst our target object.
                # And apply expected prefix
                with suppress(AttributeError):
                    _frame = _frame.f_back
                    if _frame.f_code is self.target.__code__:
                        result['depth'] = depth
                        break
            else:
                return self.trace

        result['line_number'] = frame.f_lineno
        result['source_line'] = frame_source[result['line_number'] - 1]
        result['time'] = datetime.utcnow()
        result['event'] = event
        try:
            print(self.get_ast(frame_source))
            find_in_tree(self.get_ast(frame_source), result['line_number'])
        except Found as err:
            result['ast_tree'] = err.elem

        result['modified_variables'] = {}
        result['new_variables'] = {}

        for key, value in frame.f_locals.items():
            if key not in self.frame_caches[frame]['locals']:
                result['new_variables'][key] = value
            elif self.frame_caches[frame]['locals'][key] != value:
                result['modified_variables'][key] = value

        # Update cached values
        self.frame_caches[frame]['locals'] = frame.f_locals.copy()

        if result['source_line'].lstrip().startswith('@') and event == 'call':
            # Source line is a decorator, so we look for the actual def
            # on the remaining of the file
            for lin, src in enumerate(frame_source[result['line_number']:]):
                if src.lstrip()[4:] in ('async', 'def '):
                    result['source_line'] = src
                    result['line_number'] = lin
                    break

        if result['event'] == 'return':
            result['return_value'] = arg

        self.write(result)
        return self.trace


@contextmanager
def tracer(target, write, max_depth):
    """Trace and cleanup sys tracer."""
    _trace = sys.gettrace()
    sys.settrace(Tracer(target, write, max_depth).trace)
    yield
    sys.settrace(_trace)


def trace(*args, **kwargs):
    """Trace.

    Writer is simply a function that will output formatted text.
    You could configure a logger and set it up like so::

        snoop(write=logging.debug)
    """

    def decorate(function):
        @functools.wraps(function)
        def inner(*in_args, **in_kwargs):
            with tracer(*args, **kwargs, target=function):
                return function(*in_args, **in_kwargs)

        @functools.wraps(function)
        async def ainner(*in_args, **in_kwargs):
            with tracer(*args, **kwargs, target=function):
                return await function(*in_args, **in_kwargs)

        if inspect.iscoroutinefunction(function):
            return ainner
        return inner

    return decorate
