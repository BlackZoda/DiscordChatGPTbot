import json
import os

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
prompts_file = os.path.join(
    current_directory, '..', 'data', 'settings', 'prompts.json')

with open(prompts_file, "r") as f:
    custom_prompts = json.load(f)

npcs = custom_prompts["npcs"]


def load_prompts():
    with open(prompts_file, "r") as f:
        data = json.load(f)
    return data


def combine_npc_prompt(prompts, character):
    pre = prompts["npcs"][character]["pre"]
    boilerplate = prompts["npcs"]["Boilerplate"]
    post = prompts["npcs"][character]["post"]
    return pre + " " + boilerplate + " " + post


def get_npc_prompt(character):
    return combine_npc_prompt(load_prompts(), character)
