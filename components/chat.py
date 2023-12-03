import os
from pathlib import Path
from typing import Self
import openai
from datetime import datetime

from components.utils.chat.chathistory import ChatHistory
from components.utils.chat.openai import OpenAiClient
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cliprint import cli_print_debug
from components.utils.settings.settings import SessionSettings
from components.utils.state.session import Session
from components.utils.state.sessionhandler import SessionHandler

# STEP 1


class ChatSession:
    """A class used to chat with openAI and to keep track of the history."""

    def __init__(
        self,
        sessionHandler: SessionHandler,
        api_key: str,
        # prompt_directory: str,
        # history_directory: str,
        # history_file_path: str | None = None,
    ):
        self.sessionHandler = sessionHandler

        print(self.sessionHandler.getCurrentSession().sessionSettings)

        self.openai_client = OpenAiClient(
            api_key,
            temp_range_min=self.sessionHandler.getCurrentSession().sessionSettings.temperature_range_min,
            temp_range_max=self.sessionHandler.getCurrentSession().sessionSettings.temperature_range_max,
        )

    def chat(self, message):
        """Build a prompt, send to openAI and then save the history"""

        # Put together system prompt
        system_prompt = build_prompt(
            self.sessionHandler.engineSettings.prompt_directory,
            self.sessionHandler.getCurrentSession().history,
        )

        cli_print_debug(system_prompt)
        cli_print_debug(message)

        response = self.openai_client.generateChatCompletion(
            system_prompt=system_prompt, prompt=message
        )

        self.sessionHandler.getCurrentSession().history.saveChatRound(message, response)
        self.openai_client.randomizeTemperature()

        cli_print_debug(response)

        return response

    def removeLastMessageFromHistory(self):
        self.sessionHandler.getCurrentSession().history.removeLastMessageFromHistory()
