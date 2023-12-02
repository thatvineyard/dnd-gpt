
from genericpath import isdir, isfile
import os

from components.utils.chat.chathistory import ChatHistory
from components.utils.cli.cli_print import cli_print_debug


def build_prompt(promt_folder: str, chat_history: ChatHistory = None):
    if not os.path.isdir(promt_folder):
        raise Exception(f'Prompt folder {promt_folder} doesn\'t exist')
    # prompt_files = [f for f in os.listdir(promt_folder) if (os.path.isfile(promt_folder + os.path.sep + f))]
    prompt_files = [file_path for file_path in map(lambda filename: promt_folder + os.path.sep + filename, os.listdir(promt_folder)) if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")]

    prompt = ""

    for prompt_file in prompt_files:
        if os.path.isfile(prompt_file):
            cli_print_debug(prompt_file)
            prompt_text = open(prompt_file, 'r').read()
            prompt += prompt_text
            prompt += '\n-----\n'

    if(chat_history):
        history_prompt = chat_history.toHistoryPrompt()
        history_prompt += '\n-----\n'
    else:
        history_prompt = ""

    pre_question_prompt = "Respond to the following: "

    system_prompt = prompt + history_prompt + pre_question_prompt

    cli_print_debug(system_prompt)
    return system_prompt
