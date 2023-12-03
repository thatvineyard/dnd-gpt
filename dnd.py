import argparse
from ast import arg
import logging
import os
from pathlib import Path
import re
import signal
import sys
from dotenv import load_dotenv
from colorama import Fore, Style
import inquirer

from components.assistance import Assistance
from components.chat import ChatSession
from components.cli import start_cli
from components.parser import InputTextFormatError, parse
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cliprint import cli_input, cli_print_debug, cli_print_error, cli_print_info, cli_print_warn, cli_setup_logging
from components.utils.cli.envvars import envvars
from components.utils.cli.args import args
from components.utils.cli.signalhandler import setup_signals
from components.utils.voice.texttospeech import TextToSpeech
from components.utils.spotify.spotifyclient import SpotipyClient

##############
### SET UP ###
##############

setup_signals()

# Set up logging
cli_setup_logging(level=(logging.DEBUG if args.debug else logging.INFO))


cli_print_debug(f'mode: {args.mode}')


# Set up utilities
# STEP 1: 
chatSession = ChatSession(envvars.OPENAI_KEY, envvars.PROMPTS_DIRECTORY, envvars.HISTORY_DIRECTORY, args.history_file)
# STEP 2: 
textToSpeech = TextToSpeech(envvars.AZURE_KEY_1, envvars.AZURE_SERVICE_REGION)
# STEP 4: 
# spotipy = SpotipyClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

match args.mode:
  case "cli":
    start_cli(chatSession, textToSpeech)
  case "api":
    pass
  case _:
    start_cli(chatSession, textToSpeech)

