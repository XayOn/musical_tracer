Musical tracing program
------------------------

   Code is as poetry, why shouldn't it be as music too?


.. image:: ./score.png?raw=True

Have you ever tried debugging *with music*?

**Musical Tracer** is a simple tracer with musical capabilities.

It combines an expert system for musical generation with a tracer that will
dinamically analise your code, as opposed as my previous attempt
`Musical Coding <https://github.com/XayOn/musical_coding>`_
that did a static analysis of the code.

Inspired by `Pysnooper <https://github.com/cool-RR/PySnooper/>`_ and
`pytheory <https://github.com/kennethreitz/pytheory/>`_,
with `Pyknow powers <https://github.com/buguroo/pyknow/>`_.

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


License
-------

Released under the `MIT license <https://opensource.org/licenses/MIT>`_

Copyright 2019 David Francos Cuartero

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
