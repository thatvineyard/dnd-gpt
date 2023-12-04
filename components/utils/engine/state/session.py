import json
import os
from components.utils.chat.chathistory import ChatHistory

from components.utils.engine.settings.settings import SessionSettings


class Session:
    def __init__(
        self,
        name: str,
        sessionSettings: SessionSettings = None,
        chat_history: ChatHistory = None,
    ):
        self.name = name
        self.sessionSettings = sessionSettings if sessionSettings else SessionSettings()
        self.history = chat_history if chat_history else ChatHistory()

    def toJson(self):
        return json.dumps(
            {
                "name": self.name,
                "history": self.history,
                "sessionSettings": self.sessionSettings,
            },
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4,
        )

    def toFile(self, session_directory: str, file_name: str):
        file_path = os.path.join(session_directory, file_name)

        file = open(file_path, "w+")
        file.write(self.toJson())
        file.close()

    @staticmethod
    def fromJson(json_string: str):
        json_object = json.loads(json_string)

        return Session(
            json_object.get("name"),
            SessionSettings.fromDict(json_object.get("sessionSettings")),
            ChatHistory.fromDict(json_object.get("history")),
        )

    @staticmethod
    def fromFile(session_directory: str, file_name: str):
        file_path = os.path.join(session_directory, file_name)

        if not os.path.isfile(file_path):
            raise Exception(
                f"File ({file_name}) not found in session directory ({session_directory})"
            )

        file = open(file_path, "r")
        file_contents = file.read()
        file.close()

        return Session.fromJson(file_contents)
