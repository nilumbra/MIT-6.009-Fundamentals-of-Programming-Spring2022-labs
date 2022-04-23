# No Imports Allowed!


def backwards(sound):
    # raise NotImplementedError
    new_sound = {}
    new_sound['rate'] = sound['rate']
    new_sound['left'] = sound['left'][::-1]
    new_sound['right'] = sound['right'][::-1]

    return new_sound


def mix(sound1, sound2, p):
    # raise NotImplementedError
    assert (p >= 0 and p <= 1)

    if(sound1['rate'] != sound2['rate']):
        return None

    # Taking the minimum of two sounds 
    proper_sound_length = min(len(sound1['left']), len(sound2['left']))

    new_sound = {}
    new_sound['rate'] = sound1['rate']

    s1_l = sound1['left'][:proper_sound_length]
    s2_l = sound2['left'][:proper_sound_length]

    s1_r = sound1['right'][:proper_sound_length]
    s2_r = sound2['right'][:proper_sound_length]

    new_sound['left'] = [l1*p + l2*(1-p) for (l1, l2) in zip(s1_l,  s2_l)]
    new_sound['right'] = [r1*p + r2*(1-p) for (r1, r2) in zip(s1_r,  s2_r)]

    return new_sound

def echo(sound, num_echos, delay, scale):
    # raise NotImplementedError
    assert(num_echos >= 0)
    sample_delay = int(round(delay * sound['rate']))
    slen = len(sound['left'])

    new_sound = {}

    new_sound['rate'] = sound['rate']

    new_sound['left'] = [l for l in sound['left']]
    new_sound['left'].extend([0]*(sample_delay*num_echos))

    new_sound['right'] = [r for r in sound['right']]
    new_sound['right'].extend([0]*(sample_delay*num_echos))

    for i in range(num_echos):
        for j in range(slen): 
            new_sound['left'][j + (i+1)* sample_delay] += sound['left'][j] * scale**(i+1)
            new_sound['right'][j + (i+1)* sample_delay] += sound['right'][j] * scale**(i+1)
    return new_sound

def pan(sound):
    # raise NotImplementedError
    new_sound = {}
    new_sound['rate'] = sound['rate']
    slen = len(sound['left'])

    new_sound['left'] = [datum*(1 - i/(slen-1)) for (i, datum) in zip(range(slen), sound['left'])]
    new_sound['right'] = [datum*(i/(slen-1)) for (i, datum) in zip(range(slen), sound['right'])]

    return new_sound

def remove_vocals(sound):
    # raise NotImplementedError
    new_sound = {}
    new_sound['rate'] = sound['rate']
    slen = len(sound['left'])

    new_sound['left'] = [(l - r) for (l, r) in zip(sound['left'], sound['right'])]
    new_sound['right'] = new_sound['left']
    return new_sound


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds

import io
import wave
import struct

def load_wav(filename):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    f = wave.open(filename, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    left = []
    right = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            left.append(struct.unpack('<h', frame[:2])[0])
            right.append(struct.unpack('<h', frame[2:])[0])
        else:
            datum = struct.unpack('<h', frame)[0]
            left.append(datum)
            right.append(datum)

    left = [i/(2**15) for i in left]
    right = [i/(2**15) for i in right]

    return {'rate': sr, 'left': left, 'right': right}


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    outfile = wave.open(filename, 'w')
    outfile.setparams((2, 2, sound['rate'], 0, 'NONE', 'not compressed'))

    out = []
    for l, r in zip(sound['left'], sound['right']):
        l = int(max(-1, min(1, l)) * (2**15-1))
        r = int(max(-1, min(1, r)) * (2**15-1))
        out.append(l)
        out.append(r)

    outfile.writeframes(b''.join(struct.pack('<h', frame) for frame in out))
    outfile.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav('sounds/hello.wav')

    # write_wav(backwards(hello), 'cde_reversed.wav')
    # mystery = load_wav('sounds/mystery.wav')
    # write_wav(backwards(mystery), 'mystery_reversed.wav')

    #****** MIX ******
    chord = load_wav('sounds/chord.wav')
    meow = load_wav('sounds/meow.wav')
    write_wav(mix(chord, meow, 0.9), 'mix_guitar&cat.wav')

    #****** ECHO ******
    write_wav(echo(hello, 4, 0.4, 0.4), 'hello_echoed.wav')

    #****** PAN ******
    # doorcreak = load_wav('sounds/doorcreak.wav')
    # write_wav(pan(doorcreak), 'doorcreak_paned.wav')
    car = load_wav('sounds/car.wav')
    write_wav(pan(car), 'car_paned.wav')

    #****** VOCAL REMOVAL ******
    coffee = load_wav('sounds/coffee.wav')
    write_wav(remove_vocals(coffee), 'coffee_de-voiced.wav')
