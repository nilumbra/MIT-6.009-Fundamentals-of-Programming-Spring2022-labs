#!/usr/bin/env python3
import os
import sys
import json
import time
import pickle
import importlib
import mimetypes

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

import lab

current_game_2d = None

def parse_post(environ):
    try:
        body_size = int(environ.get('CONTENT_LENGTH', 0))
    except:
        body_size = 0

    body = environ['wsgi.input'].read(body_size)
    try:
        return json.loads(body)
    except:
        return {}


def handle_render_2d(params):
    return lab.render_2d_locations(current_game_2d, params['xray'])


def handle_dig_2d(params):
    dug_2d = lab.dig_2d(current_game_2d, params['row'], params['col'])
    status = current_game_2d['state']
    return [status, dug_2d]

def handle_new_game_2d(params):
    global current_game_2d
    current_game_2d = lab.new_game_2d(params['num_rows'], params['num_cols'], [tuple(i) for i in params['bombs']])

def handle_restart(params):
    # reload student code
    importlib.reload(lab)

funcs = {
    '/ui_render_2d': handle_render_2d,
    '/ui_dig_2d': handle_dig_2d,
    '/ui_new_game_2d': handle_new_game_2d,
    '/restart': handle_restart,
}


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/') or '/'
    params = parse_post(environ)
    if path in funcs:
        try:
            body = json.dumps(funcs[path](params)).encode('utf-8')
            status = '200 OK'
            type_ = 'application/json'
        except Exception as e:
            body = str(e).encode('utf-8')
            status = '500 INTERNAL SERVER ERROR'
            type_ = 'text/plain'
    else:
        if path == '/':
            static_file = '/ui2d/index.html'
        else:
            static_file = path

        static_file = static_file.lstrip('/')

        if static_file.startswith('ui2d/'):
            static_file = static_file[5:]

        test_fname = os.path.join(os.path.dirname(__file__), 'ui2d', static_file)

        try:
            status = '200 OK'
            with open(test_fname, 'rb') as f:
                body = f.read()
            type_ = mimetypes.guess_type(test_fname)[0] or 'text/plain'
        except FileNotFoundError:
            status = '404 FILE NOT FOUND'
            body = test_fname.encode('utf-8')
            type_ = 'text/plain'

    len_ = str(len(body))
    headers = [('Content-type', type_), ('Content-length', len_)]
    start_response(status, headers)
    return [body]



if __name__ == '__main__':
    print('starting server.  navigate to http://localhost:6009/')
    with make_server('', 6009, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
