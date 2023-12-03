from components.utils.cli.envvars import EnvVars


class EngineSettings:
    def __init__(self):
        self.prompt_directory = EnvVars.PROMPTS_DIRECTORY
        self.session_directory = EnvVars.SESSION_DIRECTORY


kind_of_crazy = 1.3
creative = 1
boring = 0.3


class SessionSettings(dict):
    def __init__(
        self,
        temperature_range_min: int = creative,
        temperature_range_max: int = kind_of_crazy,
    ):
        self.temperature_range_min = temperature_range_min
        self.temperature_range_max = temperature_range_max

    def __dict__(self):
        return {
            "temperature_range_min": self.temperature_range_min,
            "temperature_range_max": self.temperature_range_max,
        }

    def __json__(self):
        return self.__dict__()

    @staticmethod
    def fromDict(dict: dict):
        return SessionSettings(
            dict["temperature_range_min"], dict["temperature_range_max"]
        )
