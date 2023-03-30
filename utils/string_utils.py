def split_string_list(strings, max_length=1990):
    result = []
    current_chunk = ""

    for text in strings:
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) + 1 <= max_length:
                if current_chunk:
                    current_chunk += "\n"
                current_chunk += paragraph
            else:
                result.append(current_chunk.strip())
                current_chunk = paragraph

    if current_chunk:
        result.append(current_chunk.strip())

    return result