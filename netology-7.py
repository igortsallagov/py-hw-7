def read_file(file):
    if '.xml' in file:
        import xml.etree.ElementTree as ET
        tree = ET.parse(file)
        descriptions = []
        root = tree.getroot()
        xml_items = root.findall('channel/item')

        for item in xml_items:
            description = item.find('description')
            descriptions += description.text.split(" ")
        return descriptions

    elif '.json' in file:
        import json
        import chardet
        with open(file, 'rb') as f:
            data = f.read()
            result = chardet.detect(data)
            data = data.decode(result['encoding'])
            data = json.loads(data)
            full_text = ''
            for items in data['rss']['channel']['items']:
                full_text += ' ' + items['description']
            descriptions = full_text.split(' ')
            return descriptions


def longer_than_x(descriptions, x):
    longer_than_list = list()
    for word in descriptions:
        if len(word) > x:
            longer_than_list.append(word)
    return longer_than_list


def sort_dict(longer_than_list):
    sorted_dict = {word: longer_than_list.count(word) for word in longer_than_list}
    return sorted_dict


def top_y_words(sorted_dict, y):
    list_of_lists = list()
    for word in sorted_dict.keys():
        list_of_lists.append([word, sorted_dict[word]])
    result = sorted(list_of_lists, key=lambda pair: pair[1], reverse=True)

    counter = 1
    for element in result:
        print('{}. {} - {}'.format(counter, element[0], element[1]))
        if counter == y:
            break
        counter += 1


def core():
    input_1 = input('Введите имя папки: ')
    input_2 = input('Введите имя файла (XML или JSON): ')
    input_3 = int(input('Минимальное число символов в словах для поиска: '))
    input_4 = int(input('Введите длину списка часто повторяющихся слов: '))
    file = str(input_1 + '/' + input_2)
    data = read_file(file)
    data_list = longer_than_x(data, input_3)
    data_dict = sort_dict(data_list)
    top_y_words(data_dict, input_4)


if __name__ == '__main__':
    core()
