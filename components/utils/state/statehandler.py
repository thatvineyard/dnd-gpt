from genericpath import isfile
import json
import os
from components.utils.chat.chathistory import ChatHistory, ChatRound
from components.utils.cli.cliprint import cli_print_error


class Session:
    def __init__(self, name: str):
        self.name = name
        self.history = []

    def toJson(self):
        return json.dumps({"name": self.name, "history": self.history})

    @staticmethod
    def fromJson(json_string: str):
        json_object = json.loads(json_string)

        return Session(json_object.name)


class SessionHandler:
    def __init__(self, session_directory: str):
        self.session_directory = session_directory
        self.sessions: dict[str, Session] = {}
        self.selected_session = None

    def selectSession(self, name: str):
        if name not in self.sessions.keys():
            self.loadSession(name)

        self.selected_session = self.sessions.get(name)
        if not self.selected_session:
            raise KeyError(f'Session "{name}" could not be found.')

    def loadSession(self, file_name: str):
        self.session_file_path = f"{self.session_directory}/{file_name}"
        if not os.path.isfile(self.session_file_path):
            return None

        session_file = open(self.session_file_path, "r")
        json_string = session_file.read()
        session_file.close()

        session = Session.fromJson(json_string)

        self.sessions[session.name] = session

    def newSession(self, name: str):
        new_session = Session(name)
        print(new_session.toJson())

        self.sessions[new_session.name] = new_session
        # self.history: list[ChatRound] = []
        # self.history_file_path = f"{self.session_directory}/{file_name}"
        # os.makedirs(os.path.dirname(self.history_file_path), exist_ok=True)

        # self.user_prefix = user_prefix
        # self.ai_prefix = ai_prefix

    @staticmethod
    def fromFile(history_directory: str, history_file_name: str):
        """Creates a ChatHistory from the given history_file_name. You should provide the file name of a file within the history directory"""

        history = ChatHistory(history_directory, history_file_name)
        history_file = open(history.history_file_path, "r")
        json_string = history_file.read()
        history_file.close()

        json_list = json.loads(json_string)
        for element in json_list:
            history.history.append(ChatRound(**element))

        return history

    def storeHistory(self):
        """Stores the history to disk. Use ChatHistory.fromFile() to read it back into memory."""

        json_string = json.dumps(
            self.history, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
        history_file = open(self.history_file_path, "w")
        history_file.write(json_string)
        history_file.close()
