fortune_file = '/home/stargriv/Documents/fortune/fortunes'

with open(fortune_file, 'rt', newline=None) as f:
    line = f.readline()
    result = []
    start = None
    pos = 0
    while line:
        if line == "%\n":
            print(start, pos - start - len(line))
            result = []
            start = None
        else:
            if start == None:
                start = f.tell() - len(line)
            result.append(line)
        pos = f.tell()
        line = f.readline()
