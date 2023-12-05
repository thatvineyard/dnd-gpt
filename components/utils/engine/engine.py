import json
from components.chat import ChatSession
from components.cli import start_cli
from components.utils.chat.promptfactory import PromptFactory
from components.utils.cli.cliprint import CliPrefix, cli_print_debug, cli_print_info
from components.utils.engine.settings.settings import EngineSettings
from components.utils.engine.state.sessionhandler import SessionHandler
from components.utils.voice.texttospeech import TextToSpeech


class Engine:
    def __init__(self, engineSettings: EngineSettings):
        cli_print_debug(
            prefix=CliPrefix.ENGINE,
            message=f"Engine settings: {json.dumps(engineSettings, default=lambda o: o.__dict__, sort_keys=True, indent=4)}",
        )
        self.engineSettings = engineSettings

        self.sessionHandler = SessionHandler(self.engineSettings)

        self.chatSession = ChatSession(
            self.engineSettings.openai_key,
        )
        # spotipy = SpotipyClient(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

    def start(self):
        cli_print_info(
            prefix=CliPrefix.ENGINE,
            message=f"Starting engine in mode {self.engineSettings.mode}",
        )
        match self.engineSettings.mode:
            case "cli":
                self.__start_cli()
            case "api":
                raise NotImplementedError("API not implemented yet")
            case _:
                self.__start_cli()

    def __start_cli(self):
        textToSpeech = TextToSpeech(
            self.engineSettings.azure_key_1, self.engineSettings.azure_service_region
        )

        start_cli(
            sessionHandler=self.sessionHandler,
            create_prompt_factory=self.__create_prompt_factory,
            chatSession=self.chatSession,
            textToSpeech=textToSpeech,
        )

    def __create_prompt_factory(self):
        return PromptFactory(
            self.sessionHandler.requireSelectedSession(),
        )
