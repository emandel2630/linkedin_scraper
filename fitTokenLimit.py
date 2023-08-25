import nltk
nltk.download('punkt')

def count_tokens(text):
    return len(nltk.word_tokenize(text))

def get_content_of_fields_with_numbers(data):
    fields_with_numbers_content = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key.isdigit():
                fields_with_numbers_content[key] = value
            if isinstance(value, dict):
                nested_content = get_content_of_fields_with_numbers(value)
                fields_with_numbers_content.update({f"{key}.{nested_key}": nested_value for nested_key, nested_value in nested_content.items()})
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, dict):
                        nested_content = get_content_of_fields_with_numbers(item)
                        fields_with_numbers_content.update({f"{key}.{idx+1}.{nested_key}": nested_value for nested_key, nested_value in nested_content.items()})
    return fields_with_numbers_content


def remove_highest_numbered_fields(data, max_tokens):
    fields_with_numbers_content = get_content_of_fields_with_numbers(data)
    while count_tokens(str(data)) > max_tokens:
        highest_numbered_field = max(fields_with_numbers_content, key=lambda x: int(x.split('.')[-1]))
        #content_to_remove = fields_with_numbers_content[highest_numbered_field]
        del data[highest_numbered_field.split(".")[0]][highest_numbered_field.split(".")[1]][highest_numbered_field.split(".")[2]]
        fields_with_numbers_content = get_content_of_fields_with_numbers(data)
    return data
