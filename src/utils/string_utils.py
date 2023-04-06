import re


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


def re_clean(string):
    pattern1 = r"(?i)as an AI language model, "
    pattern2 = r"(?<=\w)#\d{4}"
    gpt = r"^ChatGPT: "
    paulie = r"^Paulie Zasa: "
    aspaulie = r"^As Paulie Zasa, "
    gptpaulie = r"^ChatGPT \(as Paulie Zasa\): "
    rusty = r"^Rusty: "
    asrusty = r"^As Rusty, "
    gptrusty = r"^ChatGPT \(as Rusty\): "
    gptrusty2 = r"As Rusty, a right-wing conspiracy theorist, "
    oblivion = r"Oblivion: "
    asoblivion = r"As Oblivion, "
    gptoblivion = r"^ChatGPT \(as Oblivion\): "
    oblivion = r"^Adrienne Laroche: "
    asoblivion = r"^As Adrienne Laroche, "
    gptoblivion = r"^ChatGPT \(as Adrienne Laroche\): "
    luna = r"^Luna Noir: "
    asluna = r"^As Luna Noir, "
    gptluna = r"^ChatGPT \(as Luna Noir\): "
    fluffaloria = r"^Lady Fluffaloria: "
    asfluffaloria = r"^As Lady Fluffaloria, "
    gptfluffaloria = r"^ChatGPT \(Lady Fluffaloria\): "
    gregory = r"^Gregory der Schreckliche: "
    asgregory = r"^Gregory der Schreckliche, "
    gptgregory = r"^ChatGPT \(Gregory der Schreckliche\): "
    sirgregory = r"^Sir Gregory der Schreckliche: "
    sirasgregory = r"^Sir Gregory der Schreckliche, "
    sirgptgregory = r"^Sir ChatGPT \(Gregory der Schreckliche\): "

    string = re.sub(pattern1, "", string)
    string = re.sub(pattern2, "", string)

    string = re.sub(gpt, "", string)

    string = re.sub(paulie, "", string)
    string = re.sub(aspaulie, "", string)
    string = re.sub(gptpaulie, "", string)

    string = re.sub(rusty, "", string)
    string = re.sub(asrusty, "", string)
    string = re.sub(gptrusty, "", string)
    string = re.sub(gptrusty2, "", string)

    string = re.sub(oblivion, "", string)
    string = re.sub(asoblivion, "", string)
    string = re.sub(gptoblivion, "", string)
    string = re.sub(luna, "", string)
    string = re.sub(asluna, "", string)
    string = re.sub(gptluna, "", string)
    string = re.sub(fluffaloria, "", string)
    string = re.sub(asfluffaloria, "", string)
    string = re.sub(gptfluffaloria, "", string)
    string = re.sub(gregory, "", string)
    string = re.sub(asgregory, "", string)
    string = re.sub(gptgregory, "", string)
    string = re.sub(sirgregory, "", string)
    string = re.sub(sirasgregory, "", string)
    string = re.sub(sirgptgregory, "", string)

    return string
