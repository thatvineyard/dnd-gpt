from typing import Callable
from colorama import Fore, Style

from components.utils.cli.cliprint import cli_print_info

class Assistance:
  """
  An Assistance is a list of actions that can be executed by the assistant.
  Build it by running `addAction(callback, description)`.
    For example: `assistance.addAction(lambda : print("Hello World"), "Print message")`
  Then execute all the actions sequentially by running `execute()`.
  """
  
  def __init__(self):
    self.actions: list[tuple[Callable[[], None]], str] = []
  
  def addAction(self, callback: Callable[[], None], description: str):
    """Add an action to the assistance. Note that they will run in the order you add them."""
    
    self.actions.append((callback,description))
  
  def execute(self):
    """Execute the actions that have been added and print them to the console."""
    
    for action in self.actions:
      cli_print_info(prefix="D&D-GPT: ", message=action[1])
      action[0]()