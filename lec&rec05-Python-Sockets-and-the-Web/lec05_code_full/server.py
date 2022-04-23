# minimal web server and web application framework
# 6.009 lecture 5

# running this file will start the server running on port 6009.  after doing
# so, going to http://localhost:6009 will take you to the web application.  or,
# going to http://YOUR_IP_ADDRESS_HERE:6009 from a different machine will also
# load the web app (where YOUR_IP_ADDRESS_HERE is the IP address of the machine
# running this file).

# this switch is for selecting the application to run.
# this is not terribly elegant, but a web application is defined as a Python
# module.  to change what application we're using, modify the following to be
# `import ... as content`
import chatroom as content

import os
import socket
import mimetypes
import traceback

import urllib.parse

HOSTNAME = ''
PORT = 6009

# create a socket, bind it to the port given above, and start listening for
# connections
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOSTNAME, PORT))
my_socket.listen()

def send_response(sock, message, type_, code="200 OK"):
    """
    Helper function to send an HTTP response across a socket.
    """
    # make sure the input is a byte string
    if isinstance(message, str):
        message = message.encode('utf-8')
    assert isinstance(message, bytes), "message must be a bytestring!"

    # now send a response
    sock.sendall(b'HTTP/1.1 ' + code.encode('utf-8') + b'\r\n')
    sock.sendall(b'Content-type: ' + type_.encode('utf-8') + b'\r\n')
    sock.sendall(b'Content-length: %d\r\n' % len(message))
    sock.sendall(b'\r\n')
    sock.sendall(message)


while True:
    #wait for someone to connect
    connected_socket, addr = my_socket.accept()
    print('received connection from', addr)

    # receive a message (up to 4096 bytes)
    req = connected_socket.recv(4096).decode('utf-8')

    req_tokens = req.split()
    if req_tokens[0] == 'GET':
        # the location is the second token
        location = req_tokens[1].lstrip('/')

        # parse the query string to get the parameters from the query string
        parsed = urllib.parse.urlparse(location)
        location = parsed.path
        qstring = urllib.parse.parse_qs(parsed.query)
        params = {k: v[-1] for k,v in qstring.items()}

        # if no location was specified, fall back to a default called 'mainpage'
        location = location or 'mainpage'

        # look up the function we want to call in the content module, and
        # default to None.  treat all function names that start with an
        # underscore as nonexistent (hidden) so that we can define helper
        # functions within the content module
        page_func = None if location.startswith('_') else getattr(content, location, None)

        if page_func is None:
            send_response(connected_socket, 'File not found', 'text/plain', '404 FILE NOT FOUND')
        else:
            # our "page" functions are defined so that they return either a
            # single string (representing HTML output) or a tuple (mimetype,
            # data).
            try:
                # load the page and send a response.
                contents = page_func(params)
                if isinstance(contents, tuple):
                    mtype, contents = contents
                else:
                    mtype = 'text/html'
                send_response(connected_socket, contents, mtype, '200 OK')
            except:
                # if we failed, don't crash!  send a nice error message instead.
                contents = 'An error occurred!\n%s' % traceback.format_exc()
                send_response(connected_socket, contents, 'text/plain', '500 INTERNAL SERVER ERROR')

    # close the connection
    connected_socket.close()
