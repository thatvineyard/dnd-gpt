import logging
from components.chat import ChatSession
from components.utils.cli.args import Args
from components.utils.cli.cliprint import cli_setup_logging
from components.utils.cli.envvars import EnvVars
import json_fix
from components.utils.engine.settings.settings import EngineSettings

from components.utils.engine.state.sessionhandler import SessionHandler

cli_setup_logging(level=(logging.DEBUG if Args.debug else logging.INFO))

engineSettings = EngineSettings()

sessionHandler = SessionHandler(engineSettings)
sessionHandler.__newSession("funtime")
sessionHandler.saveSession()


sessionHandler2 = SessionHandler(engineSettings)
sessionHandler2.__loadSession("funtime")

chatSession = ChatSession(
    EnvVars.OPENAI_KEY,
)
