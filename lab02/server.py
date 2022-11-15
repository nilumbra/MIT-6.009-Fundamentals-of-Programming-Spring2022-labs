import os
import html
import json
import importlib
import mimetypes
import traceback

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

import lab as lab

LOCATION = os.path.realpath(os.path.dirname(__file__))
CURRENT_GAME = None

# Code for parsing ASCII level files
character_map = {
    "p": "player",
    "t": "target",
    "c": "computer",
    "w": "wall",
}

def parse_post(environ):
    try:
        body_size = int(environ.get("CONTENT_LENGTH", 0))
    except:
        body_size = 0

    body = environ["wsgi.input"].read(body_size)
    try:
        return json.loads(body)
    except:
        return {}


def new_game(params):
    global CURRENT_GAME
    print("[reloading lab.py in case you changed something]")
    importlib.reload(lab)
    if 'raw' in params:
        level = json.loads(params['raw'])
    else:
        level = params["level"]
        with open(os.path.join(LOCATION, 'puzzles', level)) as f:
            level = json.load(f)
            if isinstance(level, dict) and "input" in level:
                level = level["input"]
    CURRENT_GAME = lab.new_game(level)
    return {
        "board": lab.dump_game(CURRENT_GAME),
        "victory": lab.victory_check(CURRENT_GAME),
    }


def step_game(params):
    global CURRENT_GAME
    direction = params["direction"]
    CURRENT_GAME = lab.step_game(CURRENT_GAME, direction)
    return {
        "board": lab.dump_game(CURRENT_GAME),
        "victory": lab.victory_check(CURRENT_GAME),
    }


def get_levels(params):
    return sorted(
        fname
        for fname in os.listdir(os.path.join(LOCATION, "puzzles"))
        if fname.endswith(".json")
    )


funcs = {
    "new_game": new_game,
    "step_game": step_game,
    "get_levels": get_levels,
    "all_objects": lambda params: character_map,
}


def application(environ, start_response):
    path = (environ.get("PATH_INFO", "") or "").lstrip("/")
    if path in funcs:
        try:
            out = funcs[path](parse_post(environ))
            body = json.dumps(out).encode("utf-8")
            status = "200 OK"
            type_ = "application/json"
        except Exception as e:
            tb = traceback.format_exc()
            print(
                "--- Python error (likely in your lab code) during the next operation:\n"
                + tb,
                end="",
            )
            body = html.escape(tb).encode("utf-8")
            status = "500 INTERNAL SERVER ERROR"
            type_ = "text/plain"
    else:
        if path == "":
            static_file = "index.html"
        elif path == "builder":
            static_file = "builder.html"
        else:
            static_file = path

        if static_file.startswith("ui/"):
            static_file = static_file[3:]

        test_fname = os.path.join(LOCATION, "ui", static_file)
        if not os.path.exists(test_fname) and test_fname.endswith(".gif"):
            print('UNKNOWN WORD', test_fname)
            test_fname = os.path.join(LOCATION, "ui", "_unknown_word.gif")

        try:
            status = "200 OK"
            with open(test_fname, "rb") as f:
                body = f.read()
            type_ = mimetypes.guess_type(test_fname)[0] or "text/plain"
        except FileNotFoundError:
            status = "404 FILE NOT FOUND"
            body = test_fname.encode("utf-8")
            type_ = "text/plain"

    len_ = str(len(body))
    headers = [("Content-type", type_), ("Content-length", len_)]
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    print("starting server.  navigate to http://localhost:6009/")
    with make_server("", 6009, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
