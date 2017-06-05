import sys
import os
import pickle
import random
import io
from grizzled.cmdline import CommandLineParser

_PICKLE_PROTOCOL = -1

usage = 'Usage: %s [OPTIONS] fortune_file' % os.path.basename(sys.argv[0])

arg_parser = CommandLineParser(usage=usage)

options, args = arg_parser.parse_args(sys.argv)

if len(args) == 2:
    fortune_file = args[1]

else:
    try:
        fortune_file = os.environ['FORTUNE_FILE']
    except KeyError:
        arg_parser.show_usage('Missing fortune file.')

# fortune_file = open(fortune_file, 'rt', newline=None)
def random_int(start, end):
    try:
        # Use SystemRandom, if it's available, since it's likely to have
        # more entropy.
        r = random.SystemRandom()
    except:
        r = random

    return r.randint(start, end)

def _read_fortunes(fortune_file):
    with open(fortune_file, 'rt', newline=None) as f:
        line = f.readline()
        result = []
        start = None
        pos = 0
        while line:
            if line == "%\n":
                yield(start, pos - start - len(line))
                result = []
                start = None
            else:
                if start == None:
                    start = f.tell() - len(line)
                result.append(line)
            pos = f.tell()
            line = f.readline()

def make_fortune_data_file(fortune_file, quiet=False):
    """
    Create or update the data file for a fortune cookie file.

    :Parameters:
        fortune_file : str
            path to file containing fortune cookies
        quiet : bool
            If ``True``, don't display progress messages
    """
    fortune_index_file = fortune_file + '.dat'
    if not quiet:
        print ('Updating "%s" from "%s"...' % (fortune_index_file, fortune_file))

    data = []
    shortest = sys.maxsize
    longest = 0
    for start, length in _read_fortunes(fortune_file):
        data += [(start, length)]
        shortest = min(shortest, length)
        longest = max(longest, length)

    fortuneIndex = open(fortune_index_file, 'wb')
    pickle.dump(data, fortuneIndex, protocol=_PICKLE_PROTOCOL)
    fortuneIndex.close()

    if not quiet:
        print('Processed %d fortunes.\nLongest: %d\nShortest %d' %\
              (len(data), longest, shortest))

def get_random_fortune(fortune_file):
    """
    Get a random fortune from the specified file. Barfs if the corresponding
    ``.dat`` file isn't present.

    :Parameters:
        fortune_file : str
            path to file containing fortune cookies

    :rtype:  str
    :return: the random fortune
    """
    fortune_index_file = fortune_file + '.dat'
    if not os.path.exists(fortune_index_file):
        raise ValueError('Can\'t find file "%s"' % fortune_index_file)

    fortuneIndex = open(fortune_index_file, 'rb')
    data = pickle.load(fortuneIndex)
    fortuneIndex.close()
    randomRecord = random_int(0, len(data) - 1)
    (start, length) = data[randomRecord]
    f = open(fortune_file, 'rt')
    f.seek(start)
    fortuneCookie = f.read(length)
    f.close()
    print(fortuneCookie)

#make_fortune_data_file(fortune_file)
get_random_fortune(fortune_file)
