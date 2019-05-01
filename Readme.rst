Usage example

::

        poetry run musical_tracer start_server --socket=/tmp/musical.sock --debug


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
