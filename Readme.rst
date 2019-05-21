Musical tracing program
------------------------

   Code is as poetry, why shouldn't it be as music too?


.. image:: ./score.png?raw=True

Have you ever tried debugging *with music*?
This is a simple tracer with musical capabilities.

Inspired by `Pysnooper <https://github.com/cool-RR/PySnooper/>`_ and
`pytheory <https://github.com/kennethreitz/pytheory/>`_,
with `Pyknow powers <https://github.com/buguroo/pyknow/>`_.

This combines an expert system for musical generation with a tracer that will
dinamically analise your code, as opposed as my previous attempt
`Musical Coding <https://github.com/XayOn/musical_coding>`_
that did a static analysis of the code.

How to make it work
-------------------

This software works by stablising a communications socket between a server that
actually decides and plays music, and the running code, wich should be
decorated with a trace() call


Usage example (running the server)

::

        poetry run musical_tracer start_server --socket=/tmp/musical.sock --debug

Usage example (adding trace decorator)

::

        from musical_tracer.tracer import trace
        from pathlib import Path


        @trace(write=Path('/tmp/musical.sock'), max_depth=30)
        def test():
            for i in range(10):
                print(i)
            return 1


        test()


And listen to the results

Colaborators required
---------------------

My musical knowledge is limited to say the least, any colaborators with python
and musical skills will be really appreciated.
