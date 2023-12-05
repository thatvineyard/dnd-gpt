import os
from uu import Error
from components.utils.chat.promptfiles import PromptFiles

from components.utils.engine.state.session import Session

format_prompt_directory = "format"


class PromptFactory:
    def __init__(self, session: Session):
        self.session = session

        self.game_master_instruction_files: list[str] = []

        self.root_prompt_files: list[str] = []

        self.format_prompt_files: list[str] = []

        self.world_prompt_file: str | None = None

        self.synopsis = False
        self.history = False
        self.history_limit: int | None = None

        self.limit_response_instruction: str | None = None

        self.final_instruction: str | None = None

        self.__section_seperator = "\n----\n"

    def build(self):
        prompt = ""

        if self.root_prompt_files and len(self.root_prompt_files) > 0:
            for prompt_file in self.root_prompt_files:
                root_prompt = ""
                if os.path.isfile(prompt_file):
                    root_prompt += open(prompt_file, "r").read()

                prompt += root_prompt
            prompt += self.__section_seperator

        if (
            self.game_master_instruction_files
            and len(self.game_master_instruction_files) > 0
        ):
            for prompt_file in self.game_master_instruction_files:
                gm_prompt = ""
                if os.path.isfile(prompt_file):
                    gm_prompt += open(prompt_file, "r").read()

                prompt += gm_prompt
            prompt += self.__section_seperator

        if self.format_prompt_files and len(self.format_prompt_files) > 0:
            for prompt_file in self.format_prompt_files:
                format_prompt = ""
                if os.path.isfile(prompt_file):
                    format_prompt += open(prompt_file, "r").read()

                prompt += format_prompt
            prompt += self.__section_seperator

        if self.world_prompt_file:
            world_prompt = ""
            if os.path.isfile(self.world_prompt_file):
                world_prompt = open(self.world_prompt_file, "r").read()
            prompt += world_prompt
            prompt += self.__section_seperator

        if self.synopsis and self.session.story.synopsis:
            synopsis_prompt = self.session.story.synopsis
            prompt += synopsis_prompt
            prompt += self.__section_seperator

        if self.history and self.session.history:
            history_prompt = self.session.history.toHistoryPrompt(self.history_limit)
            prompt += history_prompt
            prompt += self.__section_seperator

        if self.limit_response_instruction:
            prompt += self.limit_response_instruction
            prompt += self.__section_seperator

        if self.final_instruction:
            prompt += self.final_instruction

        return prompt

    def withHistory(self):
        self.history = True
        return self

    def withHistoryLimit(self, limit: int):
        self.history_limit = limit
        return self

    def withRootPromptFiles(self):
        self.root_prompt_files = PromptFiles.ROOT_PROMPTS
        return self

    def withWorldPromptFile(self, world_name: str):
        if self.world_prompt_file:
            raise Exception("World prompt already set")
        world_prompt_file = PromptFiles.WORLD_PROMPTS[world_name]
        if not world_prompt_file:
            raise Exception(f"Could not find world prompt {world_name}")
        self.world_prompt_file = world_prompt_file
        return self

    def withSynopsis(self):
        self.synopsis = True
        return self

    def withGameMasterInstruction(self):
        self.game_master_instruction_files.append(PromptFiles.GAME_MASTER_PROMPT)
        return self

    def withSkillCheckInstruction(self):
        self.game_master_instruction_files.append(PromptFiles.SKILL_CHECK_PROMPT)
        return self

    def withCreateStoryLineInstruction(self):
        self.game_master_instruction_files.append(PromptFiles.CREATE_STORYLINE_PROMPT)
        return self

    def withIdentifyCharactersInstruction(self):
        self.game_master_instruction_files.append(
            PromptFiles.IDENTIFY_CHARACTERS_PROMPT
        )
        return self

    def withConversationFormatInstructions(self):
        self.format_prompt_files.append(PromptFiles.FORMAT_CONVERSATION)
        return self

    def withCharacterFormatInstructions(self):
        self.format_prompt_files.append(PromptFiles.FORMAT_CHARACTERS)
        return self

    def withFinalInstruction(self, instruction: str):
        self.final_instruction = instruction
        return self

    def withLimitResponse(
        self,
        characters: int | None = None,
        words: int | None = None,
        sentences: int | None = None,
        paragraphs: int | None = None,
    ):
        instruction = ""

        if characters and characters > 0:
            instruction += f"Limit your answer to {characters} characters. "

        if words and words > 0:
            instruction += f"Limit your answer to {words} words. "

        if sentences and sentences > 0:
            instruction += f"Limit your answer to {sentences} sentences. "

        if paragraphs and paragraphs > 0:
            instruction += f"Limit your answer to {paragraphs} paragraphs. "

        self.limit_response_instruction = instruction

        return self


# def build_prompt(promt_folder: str, chat_history: ChatHistory):
#     if not os.path.isdir(promt_folder):
#         raise Exception(f"Prompt folder {promt_folder} doesn't exist")
#     # prompt_files = [f for f in os.listdir(promt_folder) if (os.path.isfile(promt_folder + os.path.sep + f))]
#     prompt_files = [
#         file_path
#         for file_path in map(
#             lambda filename: promt_folder + os.path.sep + filename,
#             os.listdir(promt_folder),
#         )
#         if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")
#     ]

#     prompt = ""

#     for prompt_file in prompt_files:
#         if os.path.isfile(prompt_file):
#             prompt_text = open(prompt_file, "r").read()
#             prompt += prompt_text
#             prompt += "\n-----\n"

#     if chat_history:
#         history_prompt = chat_history.toHistoryPrompt()
#         history_prompt += "\n-----\n"
#     else:
#         history_prompt = ""

#     pre_question_prompt = "Respond to the following: "

#     system_prompt = prompt + history_prompt + pre_question_prompt

#     return system_prompt
