import logging
from contextlib import suppress
from musical_tracer.tracer import trace
# import pytheory

logging.basicConfig(level=logging.DEBUG)

PARSER = {ast.FunctionDef: parse_function}


def parse_function(ast_elem):
    """Function."""
    return {'name': ast_elem.name, 'class': 'function'}


def default_parser(ast_elem):
    """Default parser."""
    return {'name': ast_elem.__class__.__name__, 'class': 'unknown'}


def play(what):
    """Rules:
    - Same lines of code should sound similar.
    - But all changed variables should sound somehow
    - We should be able to differenciate lines that execute a specific behaviour:
        - Loops
        - Variable definitions
        - function calls (and similar function names should sound similar)
            - Maybe calculate a kinda "hash" for them
    """

    what['line_number']
    what['modified_variables'].update(what['new_variables'])
    what['depth']
    what['event']
    # We can only actually know when a

    source = what['source_line']

    # pytheory.play(pytheory.Tone.from_string("C2"), t=100)
    # print(what['ast_tree'], what['source_line'], ['line_number'])
    print(what)


def test2():
    print("OK")
    return 2


@trace(write=play, max_depth=30)
def test():
    test2()
    return 1


test()
