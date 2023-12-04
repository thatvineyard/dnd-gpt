import json
import os
from components.utils.cli.cliprint import CliPrefix, cli_print_debug, cli_print_info
from components.utils.engine.enginestateerror import EngineStateError
from components.utils.engine.settings.settings import EngineSettings
from components.utils.engine.state.session import Session


class SessionHandler:
    def __init__(self, engineSettings: EngineSettings = None):
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
        except KeyError:
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
        except Exception:
            raise KeyError(f"Session '{name}' could not be found.")

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
            self.session_directory, self.__sessionFileName(self.selected_session.name)
        )
        cli_print_debug(
            prefix=CliPrefix.SESSION,
            message=f"Saved session '{self.selected_session.name}'",
        )

    @staticmethod
    def __sessionFileName(name: str):
        return f"{name}.json"

    def storeHistory(self):
        """Stores the history to disk. Use ChatHistory.fromFile() to read it back into memory."""

        json_string = json.dumps(
            self.history, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
        history_file = open(self.history_file_path, "w")
        history_file.write(json_string)
        history_file.close()
