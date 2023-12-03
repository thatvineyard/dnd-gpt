
import logging
import os

from components.utils.state.statehandler import SessionHandler


stateHandler = SessionHandler("./session")
stateHandler.newSession("funtime")
stateHandler.selectSession("funtime")

# load_dotenv(".env")
# AZURE_KEY_1=os.environ["AZURE_KEY_1"]
# AZURE_SERVICE_REGION=os.environ["AZURE_SERVICE_REGION"]
# textToSpeech = TextToSpeech(AZURE_KEY_1, AZURE_SERVICE_REGION)

# text = open('test/test_input2.txt', 'r').read()

# cli_setup_logging(logging.DEBUG)

# cli_print_debug(text)

# try:
#     assistance = parse(text, textToSpeech)
#     assistance.execute()
# except InputTextFormatError:
#     exit
