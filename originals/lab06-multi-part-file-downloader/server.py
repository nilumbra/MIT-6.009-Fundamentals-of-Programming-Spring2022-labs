import os
import html
import json
import base64
import importlib
import mimetypes
import traceback

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

import lab as lab

LOCATION = os.path.realpath(os.path.dirname(__file__))
CURRENT = [None, None]


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


def single_file_wrapper(x):
    yield b"".join(x)


def new_request(params):
    url = params["url"]
    CURRENT[1] = (
        "image/jpeg"
        if ".jpg" in url
        else "image/png"
        if ".png" in url
        else "audio/vnd.wav"
        if ".wav" in url
        else "text/plain"
    )
    try:
        CURRENT[0] = lab.download_file(url)
    except (lab.HTTPFileNotFoundError, lab.HTTPRuntimeError) as e:
        CURRENT[0] = CURRENT[1] = None
        return {"ok": False, "error": e.args[0]}
    if "-seq" in url:
        CURRENT[0] = lab.files_from_sequence(CURRENT[0])
    else:
        # make a length-1 thing that just yields the whole file
        CURRENT[0] = single_file_wrapper(CURRENT[0])
    return {"ok": True, "sequence": "-seq" in url, "type": CURRENT[1]}


def get_next_file(params):
    if None in CURRENT:
        return {"ok": False, "error": "No url downloaded?  Error from before?"}

    try:
        if CURRENT[1] == "text/plain":
            data = next(CURRENT[0]).decode("utf-8")
        else:
            data = f'data:{CURRENT[1]};base64,{base64.b64encode(next(CURRENT[0])).decode("utf-8")}'
        out = {"ok": True, "data": data}
    except StopIteration:
        out = {"ok": False, "error": "out of data"}

    return out


funcs = {
    "new_request": new_request,
    "next_file": get_next_file,
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
        else:
            static_file = path

        if static_file.startswith("ui/"):
            static_file = static_file[3:]

        test_fname = os.path.join(LOCATION, "ui", static_file)

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
