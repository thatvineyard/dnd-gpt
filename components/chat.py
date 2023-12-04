from components.utils.chat.openai import OpenAiClient
from components.utils.chat.promptbuilder import build_prompt
from components.utils.cli.cliprint import CliPrefix, cli_print_debug
from components.utils.engine.enginestateerror import EngineStateError
from components.utils.engine.state.session import Session

# STEP 1


class ChatSession:
    """A class used to chat with openAI and to keep track of the history."""

    def __init__(self, api_key: str, prompt_directory: str):
        self.api_key = api_key
        self.prompt_directory = prompt_directory
        self.session = None

    def new_session(self, session: Session):
        self.session = session
        self.openai_client = OpenAiClient(
            self.api_key,
            temp_range_min=self.session.sessionSettings.temperature_range_min,
            temp_range_max=self.session.sessionSettings.temperature_range_max,
        )

    def chat(self, message):
        """Build a prompt, send to openAI and then save the history"""

        if not self.session:
            raise EngineStateError("No session selected")

        # Put together system prompt
        system_prompt = build_prompt(
            self.prompt_directory,
            self.session.history,
        )

        cli_print_debug(
            prefix=CliPrefix.CHAT, message=f"System prompt: \n{system_prompt}"
        )
        cli_print_debug(prefix=CliPrefix.CHAT, message=f"Prompt '{message}'")

        response = self.openai_client.generateChatCompletion(
            system_prompt=system_prompt, prompt=message
        )

        self.session.history.saveChatRound(message, response)
        self.openai_client.randomizeTemperature()

        cli_print_debug(prefix=CliPrefix.CHAT, message=f"Response: \n{response}")

        return response

    def removeLastMessageFromHistory(self):
        self.session.history.removeLastMessageFromHistory()
