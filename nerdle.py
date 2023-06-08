import multiprocessing
from itertools import chain

available_symbols = '0123456789+-*/'

def generate_valid_expressions(previous_symbols, desired_length, expressions=set()):
    if len(previous_symbols) == desired_length:
        try:
            right_side = eval(previous_symbols)
            if (isinstance(right_side, int) or right_side.is_integer()) and right_side >= 0:
                equation = f'{previous_symbols}={int(right_side)}'
                if len(equation) == 8:
                    expressions.add(equation)
        except SyntaxError:
            pass
        return
    possible_symbols = available_symbols
    if len(previous_symbols) == 3 and desired_length == 6 and previous_symbols.isnumeric():
        possible_symbols = '-/'
    if previous_symbols == '' or previous_symbols[-1] in '+-':
        possible_symbols = '123456789'
    elif previous_symbols[-1] in '*/':
        possible_symbols = '123456789-'
    for symbol in possible_symbols:
        generate_valid_expressions(previous_symbols + symbol, desired_length, expressions)
    return expressions

if __name__ == "__main__":
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    inputs = [('', 4), ('', 5)]
    inputs.extend((start + next, 6) for start in '123456789' for next in available_symbols)
    results = pool.starmap(generate_valid_expressions, inputs)
    pool.close()
    expressions = set(chain(*results))

    for expression in sorted(expressions, key=lambda x: len(set(x))):
        print(expression)

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
        filtered_expressions = set()
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
                filtered_expressions.add(expression)
                count += 1
                continue

        for expression in sorted(filtered_expressions, key=lambda x: len(set(x) - set(possibles))):
            print(expression)

        print(f'{count}/{len(expressions)}')
