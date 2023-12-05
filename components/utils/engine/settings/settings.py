from components.utils.cli.args import Args
from components.utils.cli.envvars import EnvVars


class EngineSettings:
    def __init__(self):
        self.prompt_directory = EnvVars.PROMPTS_DIRECTORY
        self.session_directory = EnvVars.SESSION_DIRECTORY
        self.openai_key = EnvVars.OPENAI_KEY
        self.azure_key_1 = EnvVars.AZURE_KEY_1
        self.azure_service_region = EnvVars.AZURE_SERVICE_REGION
        self.mode = Args.mode


class SessionTempDefaults:
    kind_of_crazy = 1.1
    creative = 0.8
    boring = 0.3


class SessionSettings:
    def __init__(
        self,
        temperature_range_min: float = SessionTempDefaults.creative,
        temperature_range_max: float = SessionTempDefaults.kind_of_crazy,
    ):
        self.temperature_range_min = temperature_range_min
        self.temperature_range_max = temperature_range_max

    @staticmethod
    def fromDict(dict: dict):
        return SessionSettings(
            dict["temperature_range_min"], dict["temperature_range_max"]
        )
