import logging
from components.chat import ChatSession
from components.utils.cli.args import Args
from components.utils.cli.cliprint import cli_setup_logging
from components.utils.cli.envvars import EnvVars
import json_fix

from components.utils.state.sessionhandler import SessionHandler

cli_setup_logging(level=(logging.DEBUG if Args.debug else logging.INFO))

sessionHandler = SessionHandler(EnvVars.SESSION_DIRECTORY)
sessionHandler.__newSession("funtime")
sessionHandler.saveSession()


sessionHandler2 = SessionHandler(EnvVars.SESSION_DIRECTORY)
sessionHandler2.__loadSession("funtime")

chatSession = ChatSession(
    sessionHandler.getCurrentSession(),
    EnvVars.OPENAI_KEY,
)

# cli_setup_logging(logging.DEBUG)

# cli_print_debug(text)

# try:
#     assistance = parse(text, textToSpeech)
#     assistance.execute()
# except InputTextFormatError:
#     exit
