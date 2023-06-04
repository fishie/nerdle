square_count = 8
available_symbols = '0123456789+-*/='
count = 0

def get_valid_symbols(previous_symbols):
    if len(previous_symbols) == 8:
        try:
            left, right = previous_symbols.split('=')
            if eval(left) == eval(right):
                yield previous_symbols
        except:
            pass
        return
    if previous_symbols == '':
        for symbol in '1':
            yield from get_valid_symbols(previous_symbols + symbol)
        return
    if len(previous_symbols) == 6 and '=' not in previous_symbols:
        yield from get_valid_symbols(previous_symbols + '=')
        return
    if len(previous_symbols) == 7 or '=' in previous_symbols:
        for symbol in '0123456789':
            yield from get_valid_symbols(previous_symbols + symbol)
        return
    if previous_symbols[-1] in '+-':
        for symbol in '123456789':
            yield from get_valid_symbols(previous_symbols + symbol)
        return
    if previous_symbols[-1] in '*/':
        for symbol in '123456789-':
            yield from get_valid_symbols(previous_symbols + symbol)
        return
    if previous_symbols[-1] == '=':
        if len(previous_symbols) == 7:
            for symbol in '0123456789':
                yield from get_valid_symbols(previous_symbols + symbol)
        else:
            for symbol in '123456789':
                yield from get_valid_symbols(previous_symbols + symbol)
        return
    for symbol in available_symbols:
        yield from get_valid_symbols(previous_symbols + symbol)

for symbol in get_valid_symbols(''):
    count += 1
    print(symbol)

print(count)
