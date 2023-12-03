import logging

from components.chat import ChatSession
from components.cli import start_cli
from components.utils.cli.cliprint import cli_print_debug, cli_setup_logging

from components.utils.cli.args import Args
from components.utils.cli.envvars import EnvVars
from components.utils.cli.signalhandler import setup_signals
from components.utils.voice.texttospeech import TextToSpeech

##############
### SET UP ###
##############

setup_signals()

# Set up logging
cli_setup_logging(level=(logging.DEBUG if Args.debug else logging.INFO))


cli_print_debug(f'mode: {Args.mode}')

chatSession = ChatSession(EnvVars.OPENAI_KEY, EnvVars.PROMPTS_DIRECTORY, EnvVars.HISTORY_DIRECTORY, Args.session_file)
textToSpeech = TextToSpeech(EnvVars.AZURE_KEY_1, EnvVars.AZURE_SERVICE_REGION)
# spotipy = SpotipyClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

match Args.mode:
  case "cli":
    start_cli(chatSession, textToSpeech)
  case "api":
    pass
  case _:
    start_cli(chatSession, textToSpeech)

