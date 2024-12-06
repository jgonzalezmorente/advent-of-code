from functools import lru_cache, cmp_to_key, partial

def read_and_parse_file(file_path):
    page_ordering_rules = []
    pages_update = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Procesa líneas con '|'
                if '|' in line:
                    try:
                        parts = line.split('|')
                        page_ordering_rules.append((int(parts[0]), int(parts[1])))
                    except ValueError as e:
                        print(f"Error al procesar la línea '{line}': {e}")
                        return None

                # Procesa líneas con ','
                elif ',' in line:
                    try:
                        pages_update.append([int(x) for x in line.split(',')])
                    except ValueError as e:
                        print(f"Error al procesar la línea '{line}': {e}")
                        return None

        return tuple(page_ordering_rules), pages_update

    except FileNotFoundError:
        print(f'Error: El archivo {file_path} no se encontró.')
        return None
    except Exception as e:
        print(f"Error inesperado al leer el archivo {file_path}: {e}")
        return None

# @lru_cache(maxsize=None)
def is_printed_before(page1, page2, rules):
    if (page1, page2) in rules:
        return True
    # for rule in filter(lambda r: r[0] == page1, rules):
    #     return is_printed_before(rule[1], page2, rules)
    return False

def is_in_correct_order(page_update, rules):
    for i in range(len(page_update) - 1):
        for j in range(i + 1, len(page_update)):
            if not is_printed_before(page_update[i], page_update[j], rules):
                return False
    return True

if __name__ == '__main__':
    inputs = 'inputs/day5.txt'
    sample = 'samples/day5.txt'

    page_ordering_rules, pages_update = read_and_parse_file(inputs)

    result = sum(map(
        lambda page_update: page_update[len(page_update) // 2],
        filter(lambda page_update: is_in_correct_order(page_update, page_ordering_rules), pages_update)
    ))
    print(result)

    result2 = sum(map(
        lambda page_update: page_update[len(page_update) // 2],
        map(
            lambda page_update: sorted(page_update, key=cmp_to_key(lambda x, y: -1 if is_printed_before(x, y, page_ordering_rules) else 1)),
            filter(lambda page_update: not is_in_correct_order(page_update, page_ordering_rules), pages_update)
        )
    ))
    print(result2)
