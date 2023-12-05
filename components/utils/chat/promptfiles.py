import os

from components.utils.cli.envvars import EnvVars

PROMPTS_DIR = EnvVars.PROMPTS_DIRECTORY
FORMAT_DIR = "format"
GAME_MASTER_DIR = "gamemaster"
WORLDS_DIR = "worlds"


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

    WORLD_PROMPTS = {
        "feskejord": os.path.join(PROMPTS_DIR, WORLDS_DIR, "feskefjord-prompt.txt"),
        "uppsala2403": os.path.join(PROMPTS_DIR, WORLDS_DIR, "uppsala2403-prompt.txt"),
    }

    FORMAT_CONVERSATION = os.path.join(
        PROMPTS_DIR, FORMAT_DIR, "conversation-format-prompt.txt"
    )

    FORMAT_CHARACTERS = os.path.join(
        PROMPTS_DIR, FORMAT_DIR, "character-format-prompt.txt"
    )
