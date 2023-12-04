import random
from openai import OpenAI


class OpenAiException(Exception):
    pass


class OpenAiClient:
    """A wrapper class to handle communicating with openai"""

    model = "gpt-3.5-turbo-1106"

    def __init__(
        self, api_key: str, temp_range_min: float = 0.8, temp_range_max: float = 1
    ):
        self.temp_range_min = max(0, temp_range_min)
        self.temp_range_max = min(1.5, temp_range_max)

        self.client = OpenAI(api_key=api_key)
        self.temp = self.randomizeTemperature()

    def generateChatCompletion(self, system_prompt: str, prompt: str):
        """Generate a chat completion from a system prompt and prompt"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=self.temp,
        )

        if len(response.choices) < 1:
            raise OpenAiException("No response from OpenAI")

        content = response.choices[0].message.content

        if not content or content == "":
            raise OpenAiException("OpenAI response had no content")

        return content.strip()

    def randomizeTemperature(self):
        return (
            random.random() * (self.temp_range_max - self.temp_range_min)
            + self.temp_range_min
        )
