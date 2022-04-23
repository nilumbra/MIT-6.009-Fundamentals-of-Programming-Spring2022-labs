"""
Utilities for the game:
    * helper to print string at a given location in a given color
    * context manager for making sys.stdin raw and turning off buffering
    * helper for parsing keystrokes from raw stdin
"""

import sys
import os
import time
import random
if sys.platform != 'win32':
    import fcntl
    import tty
    import termios
else:
    import ctypes,  msvcrt

color_map = {
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
    'reset': 0,
}

keymap = {
    # Arrow keys
    '\x1b[A': (3, 'UP'),
    '\x1b[B': (3, 'DOWN'),
    '\x1b[C': (3, 'RIGHT'),
    '\x1b[D': (3, 'LEFT'),
    # Windows arrow keys
    b'\x00H': (3, 'UP'),
    b'\x00P': (3, 'DOWN'),
    b'\x00M': (3, 'RIGHT'),
    b'\x00K': (3, 'LEFT'),
    # vi
    'h': (2, 'LEFT'),
    'j': (2, 'DOWN'),
    'k': (2, 'UP'),
    'l': (2, 'RIGHT'),
    b'h': (2, 'LEFT'),
    b'j': (2, 'DOWN'),
    b'k': (2, 'UP'),
    b'l': (2, 'RIGHT'),
    # WASD
    'w': (1, 'UP'),
    'a': (1, 'LEFT'),
    's': (1, 'DOWN'),
    'd': (1, 'RIGHT'),
    b'w': (1, 'UP'),
    b'a': (1, 'LEFT'),
    b's': (1, 'DOWN'),
    b'd': (1, 'RIGHT'),
    # Numpad
    '8': (4, 'UP'),
    '4': (4, 'LEFT'),
    '2': (4, 'DOWN'),
    '6': (4, 'RIGHT'),
    b'8': (4, 'UP'),
    b'4': (4, 'LEFT'),
    b'2': (4, 'DOWN'),
    b'6': (4, 'RIGHT'),
}


class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
        return self
    def __exit__(self, type_, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

class keystrokes(raw):
    def __init__(self, stream):
        raw.__init__(self, stream)
        self.buff = ''
    def regioned_keys(self):
        try:
            self.buff += sys.stdin.read(1024)
        except IOError:
            pass
        keys, self.buff = parse_keystrokes(self.buff)
        return keys
    def keys(self):
        return [key for region, key in self.regioned_keys()]

if sys.platform == 'win32':
    class keystrokes(keystrokes):
        def __init__(self, stream):
            self.buff = bytes()
        def __enter__(self):
            return self
        def __exit__(self, type_, value, traceback):
            pass
        def regioned_keys(self):
            while msvcrt.kbhit():
                try:
                    self.buff += ctypes.c_char(msvcrt.getch()).value
                except IOError:
                    pass
            keys, self.buff = parse_keystrokes(self.buff)
            return keys

def print_at_location(r, c, text, color='white'):
    success = False
    while not success:
        try:
            sys.stdout.write("\x1b7\x1b[%d;%df\x1b[%dm%s\x1b[0m\x1b8" % (r, c, color_map[color], text))
            sys.stdout.flush()
            success = True
        except BlockingIOError:
            continue


def parse_keystrokes(buff):
    keys = []
    ix = 0
    lastix = None
    while ix < len(buff):
        c = buff[ix:ix+1]
        if c == '\x1b':  # special character of some kind
            sequence = buff[ix:ix+3]
            if sequence in keymap:
                keys.append(keymap[sequence])
                ix += 3
                lastix = ix
        elif c == b'\x00':  # Windows special character
            sequence = buff[ix:ix+2]
            if sequence in keymap:
                keys.append(keymap[sequence])
                ix += 2
                lastix = ix
        else:
            keys.append(keymap.get(c, (0, c)))
            lastix = ix + 1
        ix += 1
    return keys, buff[lastix:]


def clear_screen():
    print('\33[2J', flush=True)