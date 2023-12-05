import math
import random
from components.utils.chat.openai import OpenAiClient
from components.utils.cli.cliprint import CliPrefix, cli_print_debug
from components.utils.engine.enginestateerror import EngineStateError
from components.utils.engine.state.session import Session

# STEP 1


class ChatSession:
    """A class used to chat with openAI and to keep track of the history."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        self.randomizeTemperature()

    def new_session(self, session: Session):
        self.session = session
        self.openai_client = OpenAiClient(
            self.api_key,
            temp_range_min=self.session.sessionSettings.temperature_range_min,
            temp_range_max=self.session.sessionSettings.temperature_range_max,
        )

    def requireSession(self):
        if not self.session:
            raise EngineStateError("No session selected")

        return self.session

    def chat(self, prompt="", system_prompt: str = "", temperature: int | None = None):
        """Build a prompt, send to openAI and then save the history"""

        cli_print_debug(
            prefix=CliPrefix.CHAT, message=f"System prompt: \n{system_prompt}"
        )
        cli_print_debug(prefix=CliPrefix.CHAT, message=f"Prompt '{prompt}'")

        response = self.openai_client.generateChatCompletion(
            system_prompt=system_prompt,
            prompt=prompt,
            temperature_procent=self.temperature_procent,
        )

        self.requireSession().history.saveChatRound(prompt, response)

        cli_print_debug(prefix=CliPrefix.CHAT, message=f"Response: \n{response}")

        return response

    def removeLastMessageFromHistory(self):
        self.requireSession().history.removeLastMessageFromHistory()

    def randomizeTemperature(self):
        self.setTemperatureProcent(math.ceil(random.random() * 100))

    def setTemperatureProcent(self, temperature: int):
        self.temperature_procent = min(100, max(1, temperature))
