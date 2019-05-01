"""Default tracer writer, sends data trough socket.

This can (and probably only ever will) be received by muical_tracer unix socket
server, wich will feed it to a knowledgeEngine.
"""
import ast2json
import datetime
import json


def encoder(obj):
    """Encode datetime objects, so we avoid having to install bson.json_util"""
    if isinstance(obj, datetime.datetime):
        return f'{obj:%S}'


def write(result, socket=None):
    """Write full ast tree and datetime to json format over socket."""
    result['ast_tree'] = ast2json.ast2json(result['ast_tree'])
    socket.send(json.dumps(result, default=encoder).encode() + b'\n')
