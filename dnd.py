import argparse
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style

from components.assistance import Assistance
from components.chat import ChatSession
from components.parser import InputTextFormatError, parse
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cli_print import cli_input, cli_print_debug, cli_print_error, cli_print_warn, cli_setup_logging
from components.utils.voice.texttospeech import TextToSpeech
from components.utils.spotify.spotifyclient import SpotipyClient

##############
### SET UP ###
##############

# Read environment
load_dotenv(".env")
OPENAI_KEY=os.environ["OPENAI_KEY"]
AZURE_KEY_1=os.environ["AZURE_KEY_1"]
AZURE_SERVICE_REGION=os.environ["AZURE_SERVICE_REGION"]
SPOTIFY_CLIENT_ID=os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET=os.environ["SPOTIFY_CLIENT_SECRET"]
HISTORY_DIRECTORY=os.environ["HISTORY_DIRECTORY"]
PROMPTS_DIRECTORY=os.environ["PROMPTS_DIRECTORY"]

# Set up argument parsing
arg_parser = argparse.ArgumentParser(
  prog="diy-assistant 🤖",
  description="Talk to your own assistant!"
)
arg_parser.add_argument("-f", "--history_file", help=f'If a history file exists, it will be loaded to continue conversation, otherwise it will be the filename given to the new history file. NOTE: Needs to be in the history_directory ({HISTORY_DIRECTORY})', required=False)
args = arg_parser.parse_args()

# Set up logging
cli_setup_logging(level=logging.DEBUG)

# Set up utilities
# STEP 1: 
chatSession = ChatSession(OPENAI_KEY, PROMPTS_DIRECTORY, HISTORY_DIRECTORY, args.history_file)
# STEP 2: 
textToSpeech = TextToSpeech(AZURE_KEY_1, AZURE_SERVICE_REGION)
# STEP 4: 
# spotipy = SpotipyClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

############
### CHAT ###
############

while True: 
  # STEP 1: Receives a text from console input.
  question: str = cli_input("INPUT: ")

  # STEP 1: ask openAI for an answer
  answer: str = chatSession.chat(question)

  cli_print_debug(answer)

  # STEP 3: Extract parsing to it's own function
  assistance = None
  attempts = 0
  while not assistance:
    attempts+=1
    if attempts > 3:
      cli_print_error("Did not understand response from OpenAI. Please try again (press up on keyboard to get back previous message)")
      break
    try:
      assistance = parse(answer, textToSpeech)
      assistance.execute()
    except InputTextFormatError:
      cli_print_warn("Error parsing answer, asking OpenAI for a better format.")
      answer: str = chatSession.chat("Can you please repeat the previous answer in the correct JSON format?")

