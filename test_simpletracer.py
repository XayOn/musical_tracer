from musical_tracer.writers import simple
from musical_tracer.tracer import trace


@trace(write=simple.write, max_depth=30)
def test():
    return 1


test()
