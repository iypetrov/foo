import re
import json
import requests
from datetime import datetime
from src.config.index import DEEPL_AUTH_KEY, POSTMAN_API_KEY, POSTMAN_BPA_COLLECTION_KEY

import deepl

translator = deepl.Translator(DEEPL_AUTH_KEY)


def is_valid_model(model):
    return bool(re.match(r'^[A-Z][a-zA-Z]+$', model))


def extract_words_from_model(model):
    words = []
    current_word = ''

    for char in model:
        if char.isupper():
            if current_word:
                words.append(current_word)
            current_word = char
        else:
            current_word += char

    if current_word:
        words.append(current_word)

    return words


def convert_model_to_snake_case(model):
    delimiter = "_"
    words = extract_words_from_model(model)
    result = ''

    for word in words:
        result = result + word.upper() + delimiter

    return result[:-1] if result else result


def convert_model_to_kebab_case(model):
    delimiter = "-"
    words = extract_words_from_model(model)
    result = ''

    for word in words:
        result = result + word.lower() + delimiter

    return result[:-1] if result else result


def convert_model_to_en_sentence(model):
    delimiter = " "
    words = extract_words_from_model(model)
    result = ''

    for word in words:
        result = result + word.lower() + delimiter

    result = convert_word_to_one_starting_with_upper_case(result)

    return result[:-1] if result else result


def convert_model_to_de_sentence(model):
    words = convert_model_to_en_sentence(model)
    result = translator.translate_text(words, target_lang="DE").text

    return result


def convert_word_to_one_starting_with_lower_case(model):
    if len(model) == 0:
        return ''

    return model[0].lower() + model[1:]


def convert_word_to_one_starting_with_upper_case(model):
    if len(model) == 0:
        return ''

    return model[0].upper() + model[1:]


def create_unique_id():
    current_time = datetime.now()
    hour = '00' if current_time.hour == 0 else str(current_time.hour)
    minute = '00' if current_time.minute == 0 else str(current_time.minute)
    return f'{current_time.day}{current_time.month}{current_time.year}{hour}{minute}'


def get_num_lines_in_file(file_path, enc):
    line_count = 0

    with open(file_path, 'r', encoding=enc) as file:
        for _ in file:
            line_count += 1

    return line_count


def get_line_in_message_file_based_on_model(model, file_path, enc):
    first_letter = model[0]
    headline = '--' + first_letter.upper() + first_letter.lower() + '\n'

    with open(file_path, 'r', encoding=enc) as file:
        total_count = 0
        found_headline = False

        for line in file:
            total_count += 1

            if not found_headline and line == headline:
                found_headline = True
            elif found_headline and line == '\n':
                break

    return total_count


def send_request_to_postman(name, request_method, url):
    request_data = {
        'collection': POSTMAN_BPA_COLLECTION_KEY,
        'name': name,
        'requestMethod': request_method,
        'url': url,
    }

    postman_endpoint = 'https://api.getpostman.com/collections/' + POSTMAN_BPA_COLLECTION_KEY + '/requests'

    bearer_token = '{{token}}'
    headers = {
        'X-Api-Key': POSTMAN_API_KEY,
        'Content-Type': 'application/json',
        # 'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.post(postman_endpoint, headers=headers, data=json.dumps(request_data))
    if response.status_code == 201:
        print(f'request {request_method} {url} was added successfully to Postman')
        return None
    else:
        print("request creation failed with status code:", response.status_code)
        return response.text
