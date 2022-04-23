# file server application

import os
import mimetypes

BASE_DIR = 'static'

def mainpage(params):
    # if no filename is given, return the HTML of a main page listing the
    # files.  otherwise, return the content of the file.

    filename = params.get('file', None)
    if filename is None:
        # no filename given.  return a little piece of HTML linking to all the
        # files.
        out = '<h3>Listing Files in <tt>%s</tt></h3>' % BASE_DIR
        out += '<ul>'
        for fname in sorted(os.listdir(BASE_DIR)):
            out += '<li><a href="mainpage?file=%s"><tt>%s</tt></a></li>' % (fname, fname)
        out += '</ul>'
        return out
    else:
        # here we find the location on disk of the file we want to return
        result_loc = BASE_DIR + '/' + filename
        # then we check that it is contained within the BASE_DIR and that it
        # exists.
        if os.path.realpath(result_loc).startswith(os.path.realpath(BASE_DIR)) and os.path.isfile(result_loc):
            # if so, guess at the mime type and return
            type_ = mimetypes.guess_type(result_loc)[0] or 'text/plain'
            with open(result_loc, 'rb') as f:
                out = f.read()
            return type_, out
        else:
            return ('text/plain', 'Could not find the specified file: <tt>%s</tt>' % result_loc)
