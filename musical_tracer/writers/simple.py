import socket
import ast2json
import datetime
import json

CLIENT = socket.socket(socket.AF_UNIX)
CLIENT.connect("/tmp/musical.sock")


def encoder(obj):
    if isinstance(obj, datetime.datetime):
        return f'{obj:%S}'


def write(result):
    result['ast_tree'] = ast2json.ast2json(result['ast_tree'])
    CLIENT.send(json.dumps(result, default=encoder).encode() + b'\n')
