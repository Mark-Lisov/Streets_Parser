import re

import openai as openai

openai.api_key = 'your_key' # Replace with your key

model_engine = "text-davinci-003"


def my_translator(text_for_translation: str, from_language: str, to_language: str):
    prompt = f"Translate the text in brackets ({text_for_translation}) from {from_language} language to {to_language}." \
             f" Do not translate it literally, it is names. Just transfer to {to_language} layout."

    # Set max number of words
    max_tokens = len(text_for_translation.split(' '))

    # Generate a response
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

    brackets = ['(', ')', '[', ']', '{', '}']
    
    clean_str = ''

    for char in symbols:
        clean_str = str_without_n.replace(char, "")

    if clean_str[0] == '[':
        index = clean_str.find(']') + 1
        clean_str = clean_str[index:-1]
    if clean_str[0] == '(':
        index = clean_str.find(')') + 1
        clean_str = clean_str[index:-1]

    return clean_str
