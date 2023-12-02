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


class ChatHistory:
    """
    A class that keeps track of the history, capable of storing it in text files and picking back up the history again.
    """
    
    def __init__(self, history_directory: str, file_name: str, user_prefix: str = "I said: ", ai_prefix: str = "You said: "):
        self.history: list[ChatRound] = []
        self.history_file_path = f"{history_directory}/{file_name}"
        os.makedirs(os.path.dirname(self.history_file_path), exist_ok=True)

        self.user_prefix = user_prefix
        self.ai_prefix = ai_prefix

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

    def saveChatRound(self, question: str, answer: str):
        """Save a single round of chat. Use to build the history."""
        
        answer = self.removeWhitespace(answer)
        chatRound = ChatRound(question, answer)
        self.history.append(chatRound)
        self.storeHistory()

    def storeHistory(self):
        """Stores the history to disk. Use ChatHistory.fromFile() to read it back into memory."""
        
        json_string = json.dumps(
            self.history, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
        history_file = open(self.history_file_path, "w")
        history_file.write(json_string)
        history_file.close()

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
        return re.sub(r'\s+', ' ', text)
