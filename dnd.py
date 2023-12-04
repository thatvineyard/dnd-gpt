import logging

from components.utils.cli.cliprint import cli_setup_logging

from components.utils.cli.args import Args
from components.utils.cli.signalhandler import setup_signals
from components.utils.engine.engine import Engine
from components.utils.engine.settings.settings import EngineSettings

##############
### SET UP ###
##############

setup_signals()

# Set up logging
cli_setup_logging(level=(logging.DEBUG if Args.debug else logging.INFO))

engineSettings = EngineSettings()
engine = Engine(engineSettings)

engine.start()
