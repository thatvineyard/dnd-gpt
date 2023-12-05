import json
from typing import Callable
from components.assistance import Assistance
from components.chat import ChatSession
from components.parser import InputTextFormatError, parse
from components.utils.chat.promptfactory import PromptFactory
from components.utils.cli.cliprint import (
    cli_input,
    cli_print_error,
    cli_print_info,
    cli_print_warn,
)
from components.utils.engine.adventure.story import Story
from components.utils.voice.texttospeech import TextToSpeech


class GameMaster:
    def __init__(
        self,
        chatSession: ChatSession,
        textToSpeech: TextToSpeech,
        create_prompt_factory: Callable[[], PromptFactory],
        story: Story,
    ):
        self.chatSession = chatSession
        self.textToSpeech = textToSpeech
        self.create_prompt_factory = create_prompt_factory
        self.story = story

    def createSynposis(self):
        storyline_system_prompt = (
            self.create_prompt_factory()
            .withRootPromptFiles()
            .withGameMasterInstruction()
            .withCreateStoryLineInstruction()
            .withLimitResponse(sentences=20, paragraphs=4)
            .build()
        )
        self.chatSession.setTemperatureProcent(100)
        story_response: str = self.chatSession.chat(
            prompt="Create a story line", system_prompt=storyline_system_prompt
        )

        self.story.synopsis = story_response

    def identifyCharacters(self):
        storyline_system_prompt = (
            self.create_prompt_factory()
            .withSynopsis()
            .withGameMasterInstruction()
            .withIdentifyCharactersInstruction()
            .withLimitResponse(sentences=20, paragraphs=4)
            .build()
        )
        self.chatSession.setTemperatureProcent(100)
        characters_response: str = self.chatSession.chat(
            prompt="Identify 5 characters", system_prompt=storyline_system_prompt
        )

        self.story.characters = characters_response

    def takeTurn(self):
        player_input: str = cli_input("INPUT: ")

        story_system_prompt = (
            self.create_prompt_factory()
            .withRootPromptFiles()
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
            .withFormatInstructions()
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
                    .withFormatInstructions()
                    .withFinalInstruction("Reformat this answer in proper JSON format.")
                    .build()
                )
                formatted_response: str = self.chatSession.chat(
                    prompt=story_response, system_prompt=format_system_prompt
                )
