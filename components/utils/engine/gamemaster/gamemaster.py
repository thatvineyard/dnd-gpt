from typing import Callable
from components.chat import ChatSession
from components.parser import InputTextFormatError, parse
from components.utils.chat.promptfactory import PromptFactory
from components.utils.cli.cliprint import cli_input, cli_print_error, cli_print_warn
from components.utils.voice.texttospeech import TextToSpeech


class GameMaster:
    def __init__(
        self,
        chatSession: ChatSession,
        textToSpeech: TextToSpeech,
        create_prompt_factory: Callable[[], PromptFactory],
    ):
        self.chatSession = chatSession
        self.textToSpeech = textToSpeech
        self.create_prompt_factory = create_prompt_factory

    def takeTurn(self):
        player_input: str = cli_input("INPUT: ")

        story_system_prompt = (
            self.create_prompt_factory()
            .withAllPromptFiles()
            .withHistory()
            .withHistoryLimit(2000)
            .withLimitResponse(words=10, paragraphs=1)
            .build()
        )
        self.chatSession.setTemperatureProcent(100)
        story_response: str = self.chatSession.chat(
            prompt=player_input, system_prompt=story_system_prompt
        )

        format_system_prompt = (
            self.create_prompt_factory()
            .withFormatPrompts()
            .withFinalInstruction("Reformat this answer in proper JSON format.")
            .build()
        )
        self.chatSession.setTemperatureProcent(0)
        formatted_response: str = self.chatSession.chat(
            prompt=story_response, system_prompt=format_system_prompt
        )

        # STEP 3: Extract parsing to it's own function
        assistance = None
        attempts = 0
        while not assistance:
            attempts += 1
            if attempts > 3:
                cli_print_error(
                    "Did not understand response from OpenAI. Please try again (press up on keyboard to get back previous message)"
                )
                break
            try:
                assistance = parse(formatted_response, self.textToSpeech)
                assistance.execute()
            except InputTextFormatError:
                self.chatSession.removeLastMessageFromHistory()
                cli_print_warn(
                    "Error parsing answer, asking OpenAI for a better format."
                )
                format_system_prompt = (
                    self.create_prompt_factory()
                    .withFormatPrompts()
                    .withFinalInstruction("Reformat this answer in proper JSON format.")
                    .build()
                )
                formatted_response: str = self.chatSession.chat(
                    prompt=story_response, system_prompt=format_system_prompt
                )
