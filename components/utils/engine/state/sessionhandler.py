import os
from components.utils.cli.cliprint import CliPrefix, cli_print_debug, cli_print_info
from components.utils.engine.enginestateerror import EngineStateError
from components.utils.engine.settings.settings import EngineSettings
from components.utils.engine.state.session import Session


class SessionHandler:
    def __init__(self, engineSettings: EngineSettings):
        self.engineSettings = engineSettings
        self.session_directory = engineSettings.session_directory
        self.__ensureSessionDirectoryExists(self.session_directory)
        self.selected_session = None

    @staticmethod
    def __ensureSessionDirectoryExists(session_directory: str):
        if not os.path.isdir(session_directory):
            os.mkdir(session_directory)

    def __selectSession(self, session: Session):
        cli_print_debug(
            prefix=CliPrefix.SESSION, message=f"Selecting session: {session.toJson()}"
        )
        self.selected_session = session
        cli_print_info(
            prefix=CliPrefix.SESSION, message=f"Selected session '{session.name}'"
        )

    def prepareSession(self, name: str):
        try:
            session = self.__loadSession(name)
        except FileNotFoundError:
            cli_print_debug(
                prefix=CliPrefix.SESSION,
                message=f"Session '{name}' could not be found.",
            )
            session = self.__newSession(name)

        return session

    def __loadSession(self, name: str):
        cli_print_debug(prefix=CliPrefix.SESSION, message=f"Loading session {name}")
        try:
            loaded_session = Session.fromFile(
                self.session_directory, self.__sessionFileName(name)
            )
        except FileNotFoundError:
            raise FileNotFoundError(f"Session '{name}' could not be found.")

        self.__selectSession(loaded_session)

    def __newSession(self, name: str):
        cli_print_debug(
            prefix=CliPrefix.SESSION, message=f"Creating a new session {name}"
        )
        new_session = Session(name)
        self.__selectSession(new_session)

    def getCurrentSession(self):
        if not self.selected_session:
            raise EngineStateError("No session selected.")

        return self.selected_session

    def saveSession(self):
        self.getCurrentSession().toFile(
            self.session_directory,
            self.__sessionFileName(self.requireSelectedSession().name),
        )
        cli_print_debug(
            prefix=CliPrefix.SESSION,
            message=f"Saved session '{self.requireSelectedSession().name}'",
        )

    def requireSelectedSession(self):
        if not self.selected_session:
            raise EngineStateError("No session selected")

        return self.selected_session

    @staticmethod
    def __sessionFileName(name: str):
        return f"{name}.json"
