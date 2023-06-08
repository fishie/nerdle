import multiprocessing
from itertools import chain

available_symbols = '0123456789+-*/'

def generate_valid_expressions(previous_symbols, desired_length, expressions=set()):
    if len(previous_symbols) == desired_length:
        try:
            right_side = eval(previous_symbols)
            if right_side != None and (isinstance(right_side, int) or right_side.is_integer()) and int(right_side) >= 0:
                equation = f'{previous_symbols}={int(right_side)}'
                if len(equation) == 8:
                    expressions.add(equation)
        except SyntaxError:
            pass
    elif previous_symbols[-1] in '+-':
        for symbol in '123456789':
            generate_valid_expressions(previous_symbols + symbol, desired_length, expressions)
    elif previous_symbols[-1] in '*/':
        for symbol in '123456789-':
            generate_valid_expressions(previous_symbols + symbol, desired_length, expressions)
    else:
        for symbol in available_symbols:
            generate_valid_expressions(previous_symbols + symbol, desired_length, expressions)
    return expressions

def worker(arguments):
    start, left_size = arguments
    return generate_valid_expressions(start, left_size)

if __name__ == "__main__":
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = pool.map(worker, [(start, left_size) for left_size in range(4, 7) for start in '123456789'])
    expressions = set(chain.from_iterable(results))

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
