# Set up argument parsing
import argparse

import inquirer
from components.utils.cli.cliprint import cli_print_debug
from components.utils.cli.envvars import EnvVars

class Args:
    arg_parser = argparse.ArgumentParser(
    prog="diy-assistant 🤖",
    description="Talk to your own assistant!"
    )
    arg_parser.add_argument("-m", "--mode", help="Which mode to run in.", choices=["cli", "api", "ask"], required=False, default="ask")
    arg_parser.add_argument("-d", "--debug", action='store_true', help="Debug mode", required=False, default=False)
    arg_parser.add_argument("-n", "--new", action='store_true', help="Create new", required=False)
    arg_parser.add_argument("-f", "--session_file", help=f'If a history file exists, it will be loaded to continue conversation, otherwise it will be the filename given to the new history file. NOTE: Needs to be in the history_directory ({EnvVars.HISTORY_DIRECTORY})', required=False)
    args = arg_parser.parse_args()

    debug=args.debug

    questions = []
    if not args.mode or args.mode == "ask":
        mode = inquirer.list_input(
            message="Mode",
            choices=['cli', 'api'],
        )
    else:
        mode = args.mode
    
    if not args.session_file:
        if not args.new:
            new = inquirer.list_input(
                message="Start a new adventure or load a previous file?",
                choices=['new', 'load'],
            )
        else:
            new = args.new
        if new and new == "load":
            session_file = inquirer.list_input(
                message="Select file to load",
                choices=['1', '2'],
            )
        else:
            session_file = None
    else:
        session_file=args.session_file

