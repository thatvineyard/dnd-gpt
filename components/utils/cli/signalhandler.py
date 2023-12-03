import signal
import sys

from components.utils.cli.cliprint import cli_print_info

def sigint_handler(signal, frame):
    print(flush=True)
    cli_print_info('Goodbye 👋')
    sys.exit(0)

def setup_signals():
    signal.signal(signal.SIGINT, sigint_handler)
