import re

import openai as openai

openai.api_key = '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'

model_engine = "text-davinci-003"


def my_translator(text_for_translation: str, from_language: str, to_language: str):
    prompt = f"Translate the text in brackets ({text_for_translation}) from {from_language} language to {to_language}." \
             f" Do not translate it literally, it is names. Just transfer to {to_language} layout."

    # задаем макс кол-во слов
    max_tokens = len(text_for_translation.split(' '))

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    str_without_n = completion.choices[0].text.replace('\n', '')
    symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
               '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '\t', '\n', '\r', '\x0b', '\x0c', 'А', 'Б',
               'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
               'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
               'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю',
               'я', '\d']

    all_simbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                   'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'თ',
                   'ი', 'კ', 'ლ', 'მ', 'ნ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'უ', 'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ',
                   'წ', 'ჭ', 'ხ', 'ჯ', 'ჰ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                   ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '\t', '\n',
                   '\r', '\x0b', '\x0c', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
                   'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в',
                   'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                   'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

    brackets = ['(', ')', '[', ']', '{', '}']

    '''
    counter = 0
    lst = ['any', 'text', 'here']
    for i in all_simbols:
        for obj in lst:
            counter += 1
            obj[counter - 1] = obj.split(i)
        print(lst)
    for i in symbols:
        str_without_n.replace(i, '')
        print(str_without_n)
    
    '''
    clean_str = ''

    for char in symbols:
        clean_str = str_without_n.replace(char, "")

    if clean_str[0] == '[':
        index = clean_str.find(']') + 1
        clean_str = clean_str[index:-1]
    if clean_str[0] == '(':
        index = clean_str.find(')') + 1
        clean_str = clean_str[index:-1]
    '''
    for i in symbols:
        if str_without_n[0] == i:
            str_without_n = str_without_n[1:-1]
        if str_without_n[-1] == i:
            str_without_n = str_without_n[0:-2]
    '''

    # clean_str = re.sub(r"\W", '', str_without_n)
    # clean_str = str_without_n
    return clean_str
