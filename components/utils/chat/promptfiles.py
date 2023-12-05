import os

from components.utils.cli.envvars import EnvVars

PROMPTS_DIR = EnvVars.PROMPTS_DIRECTORY
FORMAT_DIR = "format"
GAME_MASTER_DIR = "gamemaster"


class PromptFiles:
    GAME_MASTER_PROMPT = os.path.join(PROMPTS_DIR, GAME_MASTER_DIR, "gm-prompt.txt")
    CREATE_STORYLINE_PROMPT = os.path.join(
        PROMPTS_DIR, GAME_MASTER_DIR, "create-storyline-prompt.txt"
    )
    IDENTIFY_CHARACTERS_PROMPT = os.path.join(
        PROMPTS_DIR, GAME_MASTER_DIR, "identify-characters-prompt.txt"
    )
    SKILL_CHECK_PROMPT = os.path.join(
        PROMPTS_DIR, GAME_MASTER_DIR, "skill-checks-prompt.txt"
    )

    ROOT_PROMPTS = [
        file_path
        for file_path in map(
            lambda filename: os.path.join(PROMPTS_DIR, filename),
            os.listdir(PROMPTS_DIR),
        )
        if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")
    ]

    FORMAT_CONVERSATION = os.path.join(
        FORMAT_DIR, GAME_MASTER_DIR, "conversation-format-prompt.txt"
    )

    FORMAT_PROMPTS = [
        file_path
        for file_path in map(
            lambda filename: os.path.join(PROMPTS_DIR, FORMAT_DIR, filename),
            os.listdir(os.path.join(PROMPTS_DIR, FORMAT_DIR)),
        )
        if (os.path.isfile(file_path) and os.path.splitext(file_path)[1] == ".txt")
    ]
