
import os

from dotenv import load_dotenv
from components.parser import InputTextFormatError, parse
from components.utils.chat.chathistory import ChatHistory
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cli_print import cli_print_debug
from components.utils.voice.texttospeech import TextToSpeech

load_dotenv(".env")
AZURE_KEY_1=os.environ["AZURE_KEY_1"]
AZURE_SERVICE_REGION=os.environ["AZURE_SERVICE_REGION"]
textToSpeech = TextToSpeech(AZURE_KEY_1, AZURE_SERVICE_REGION)

text = open('test_input2.txt', 'r').read()

cli_print_debug(text)

try:
    assistance = parse(text, textToSpeech)
    assistance.execute()
except InputTextFormatError:
    print("hihi")
    exit


