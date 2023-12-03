import os
from pathlib import Path
from typing import Self
import openai
from datetime import datetime

from components.utils.chat.chathistory import ChatHistory
from components.utils.chat.openai import OpenAiClient
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cliprint import cli_print_debug

# STEP 1

class ChatSession:
  """A class used to chat with openAI and to keep track of the history."""
  
  def __init__(self, api_key: str, prompt_directory: str, history_directory: str, history_file_path: str | None = None):
    kind_of_crazy=1.3
    creative=1
    boring=0.3

    self.openai_client = OpenAiClient(api_key, temp_range_min=creative, temp_range_max=kind_of_crazy)
    
    self.prompt_directory = prompt_directory

    self.history = self.__getOrCreateChatHistory(history_directory, history_file_path)

  def chat(self, message):
      """Build a prompt, send to openAI and then save the history"""
      
      # Put together system prompt
      system_prompt = build_prompt(self.prompt_directory, self.history)

      cli_print_debug(system_prompt)
      cli_print_debug(message)
      
      response = self.openai_client.generateChatCompletion(system_prompt=system_prompt, prompt=message)

      self.history.saveChatRound(message, response)
      self.openai_client.randomizeTemperature()

      cli_print_debug(response)

      return response
  
  def removeLastMessageFromHistory(self):
    self.history.removeLastMessageFromHistory()

  def __getOrCreateChatHistory(self, history_directory: str, history_file_path: str | None = None):
      if history_file_path is not None:
        history_file_name = str(Path(history_file_path).relative_to(history_directory))
      else:
        history_file_name = f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json'
      
      if os.path.exists(f'{history_directory}/{history_file_name}'):
        return ChatHistory.fromFile(history_directory, history_file_name)
      else:
        return ChatHistory(history_directory, history_file_name)