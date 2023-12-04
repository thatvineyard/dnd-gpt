import os

from components.utils.engine.state.session import Session

format_prompt_directory = "format"


class PromptFactory:
    def __init__(self, prompts_directory: str, session: Session):
        self.prompts_directory = prompts_directory
        self.session = session

        self.format_prompt_files = []

        self.history = False
        self.history_limit: int | None = None

        self.final_instruction: str | None = None

        self.__section_seperator = "\n----\n"

    def build(self):
        prompt = ""

        # format prompt files
        for prompt_file in self.format_prompt_files:
            format_prompt = ""
            if os.path.isfile(prompt_file):
                format_prompt += open(prompt_file, "r").read()

            prompt += format_prompt
            prompt += self.__section_seperator

        if self.history and self.session.history:
            history_prompt = self.session.history.toHistoryPrompt(self.history_limit)
            prompt += history_prompt
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

    def withAllPromptFiles(self):
        self.format_prompt_files = [
            file_path
            for file_path in map(
                lambda filename: self.prompts_directory + os.path.sep + filename,
                os.listdir(self.prompts_directory),
            )
            if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")
        ]
        return self

    def withFormatPrompts(self):
        directory = os.path.join(self.prompts_directory, format_prompt_directory)
        self.format_prompt_files = [
            file_path
            for file_path in map(
                lambda filename: os.path.join(directory, filename),
                os.listdir(directory),
            )
            if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")
        ]
        return self

    def withFinalInstruction(self, instruction: str):
        self.final_instruction = instruction
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
