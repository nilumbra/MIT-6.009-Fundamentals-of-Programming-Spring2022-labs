# chat room application

import os
import time
import random
import string


STORAGE_LOC = 'chat_messages'

# make the storage directory if it doesn't exist
if not os.path.isdir(STORAGE_LOC):
    os.makedirs(STORAGE_LOC, exist_ok=True)


def _generate_new_username():
    """
    Helper function to generate a new username (here, a random string of
    characters)
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(10))


def all_messages(params):
    """
    Page to list all messages.  Could be more efficient, but should get the job
    done.
    """
    resp = '<ul>'
    for i in sorted(os.listdir(STORAGE_LOC)):
        time, user = i.split('_', 1)
        with open('%s/%s' % (STORAGE_LOC, i)) as f:
            msg = f.read().replace('<', '&lt;').replace('>', '&gt;')
        resp += '<li><b>%s:</b> %s</li>' % (user, msg)
    resp = resp + '</ul>'
    return resp + '''
<script type="text/javascript">
document.body.scrollTop = document.body.scrollTopMax
</script>
'''

def new_message(params):
    """
    Page to post a new message.  Ultimately returns the HTML associated with
    the main page, after storing the message on disk.

    Messages are stored on disk with the filename TIMESTAMP_USERNAME, and the
    contents are the text of the message that was posted.
    """
    newparams = {}
    user = params.get('user', None)
    if user is not None:
        t = round(time.time(), 2)
        with open('%s/%s_%s' % (STORAGE_LOC, t, user), 'w') as f:
            f.write(params.get('msg', '').replace('<', '&lt;').replace('>', '&gt;'))
        newparams['user'] = user
    return mainpage(newparams)

def mainpage(params):
    """
    Main chat page.  See chatpage.html.
    """
    if 'user' not in params:
        user = _generate_new_username()
    else:
        user = params['user']
    with open('chatpage.html') as f:
        template = f.read()
    return template % user
