from openai import OpenAI

# STEP 1

class OpenAiClient:
  """A wrapper class to handle communicating with openai"""
  
  model = 'gpt-3.5-turbo-1106'
  
  def __init__(self, api_key: str, temp: int = 1):
    self.client = OpenAI(
      api_key=api_key
    )
    self.temp = temp

  def generateChatCompletion(self, system_prompt: str, prompt: str):
    """Generate a chat completion from a system prompt and prompt"""
    
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=self.temp
    )

    return response.choices[0].message.content.strip()