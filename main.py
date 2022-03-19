import pathlib
from pprint import pprint


def recipes(filename):
    cook_book = {}
    with open(filename, 'rt', encoding='utf-8') as file:
        dish = True
        qnt = False
        ingredients = False
        for line in file:
            line = line.strip()
            line = line.strip(' ')
            if line:
                if dish:
                    current_dish = line
                    cook_book.update({current_dish: []})
                    dish = False
                    qnt = True
                    continue
                if qnt:
                    qnt = False
                    ingredients = True
                    continue
                if ingredients:
                    cur_line = line.split('|')
                    cur_line = [row.strip(' ') for row in cur_line]
                    cook_book[current_dish] += [
                        {'ingredient_name': cur_line[0], 'quantity': int(cur_line[1]), 'measure': cur_line[2]}]
                    continue
            else:
                dish = True
                ingredients = False
    return cook_book


def get_shop_list_by_dishes(dishes, persons):
    shop_list = {}
    for dish in dishes:
        if dish in cook_book:
            ingredients = cook_book[dish]
            for ingredient in ingredients:
                if ingredient['ingredient_name'] in shop_list:
                    shop_list[ingredient['ingredient_name']]['quantity'] += ingredient['quantity']*persons
                else:
                    shop_list.update({ingredient['ingredient_name']: {'measure': ingredient['measure'],
                                                                      'quantity': ingredient['quantity']*persons}})
        else:
            print(f'блюда с названием {dish} нет в книге')

    return shop_list


cook_book = recipes('recipes.txt')
pprint(cook_book)
pprint(get_shop_list_by_dishes(['Омлет', 'Омлет'], 2))


def file_lenghs(file):
    len = 0
    f = open(file, 'r', encoding='utf-8')
    for line in f:
        len += 1
    f.close()
    return len


dict_files_len = {}
for filename in pathlib.Path('files').iterdir():
    dict_files_len.update({filename.name: file_lenghs(filename)})
sorted_list_of_files_by_len = sorted(dict_files_len, key=dict_files_len.get)
with open('result.txt', 'w', encoding='utf-8') as f:
    for file in sorted_list_of_files_by_len:
        f.write(file+'\n')
        f.write(str(dict_files_len[file])+'\n')
        with open(pathlib.Path('files', file), 'r', encoding='utf-8') as f1:
            for line in f1.readlines():
                f.write(line)
            f.write('\n')
with open('result.txt', 'r', encoding='utf-8') as file:
    print(f"\n{file.read()}")
