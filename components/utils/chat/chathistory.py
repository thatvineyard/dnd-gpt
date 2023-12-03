import json
import os
import re

# STEP 1


class ChatRound:
    """
    Represents one question and response
    """

    def __init__(self, question: str, response: str):
        self.question = question
        self.response = response

    def toPrompt(self, user_prefix, ai_prefix):
        """Format in natural-language-way that OpenAI will understand."""

        return f"""
{user_prefix}{self.question}
{ai_prefix}{self.response}
        """

    @staticmethod
    def fromDict(dict: dict):
        return ChatRound(
            dict["question"],
            dict["response"],
        )


class ChatHistory:
    """
    A class that keeps track of the history, capable of storing it in text files and picking back up the history again.
    """

    def __init__(
        self,
        user_prefix: str = "I said: ",
        ai_prefix: str = "You said: ",
        history: list[ChatRound] = [],
    ):
        self.history = history

        self.user_prefix = user_prefix
        self.ai_prefix = ai_prefix

    def saveChatRound(self, question: str, answer: str):
        """Save a single round of chat. Use to build the history."""

        answer = self.removeWhitespace(answer)
        chatRound = ChatRound(question, answer)
        self.history.append(chatRound)

    def removeLastMessageFromHistory(self):
        self.history.pop()
        self.storeHistory()

    def toHistoryPrompt(self):
        """Format in natural-language-way that OpenAI will understand."""

        history_prompt = "Chat history:\n"

        if len(self.history) == 0:
            history_prompt += "This is the first message."
            return history_prompt

        for round in self.history:
            history_prompt += round.toPrompt(self.user_prefix, self.ai_prefix)
        return history_prompt

    def removeWhitespace(self, text):
        return re.sub(r"\s+", " ", text)

    @staticmethod
    def fromDict(dict: dict):
        return ChatHistory(
            dict["user_prefix"],
            dict["ai_prefix"],
            list(map(lambda e: ChatRound.fromDict(e), dict["history"])),
        )
