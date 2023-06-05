available_symbols = '0123456789+-*/'

def generate_valid_expressions(previous_symbols, desired_length):
    if len(previous_symbols) == desired_length:
        try:
            right_side = eval(previous_symbols)
            if isinstance(right_side, int) or right_side.is_integer():
                equation = f'{previous_symbols}={int(right_side)}'
                if len(equation) == 8:
                    yield equation
        except SyntaxError:
             pass
        return
    if previous_symbols == '' or previous_symbols[-1] in '+-':
        for symbol in '123456789':
            yield from generate_valid_expressions(previous_symbols + symbol, desired_length)
        return
    if previous_symbols[-1] in '*/':
        for symbol in '123456789-':
            yield from generate_valid_expressions(previous_symbols + symbol, desired_length)
        return
    for symbol in available_symbols:
        yield from generate_valid_expressions(previous_symbols + symbol, desired_length)

expressions = set()
for left_size in range(4, 7):
    for expression in generate_valid_expressions('', left_size):
        print(expression)
        expressions.add(expression)
print(len(expressions))

while True:
    try:
        known, possibles, not_possibles = input().split(',')
    except Exception as e:
        print(e, 'try again!')
        continue
    print(f'known={known}, possibles={possibles}, not_possibles={not_possibles}')

    if len(known) != 8:
        print('the length of known is not 8, please try again')
        continue

    count = 0
    for expression in expressions:
        expression_set = set(expression)
        if expression_set & set(not_possibles):
            continue

        if set(possibles) - expression_set:
            continue

        for (k, e) in zip(known, expression):
            if k != ' ' and k != e:
                break
        else:
            print(expression)
            count += 1
            continue

    print(f'{count}/{len(expressions)}')
