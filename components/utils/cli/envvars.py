import os
from dotenv import load_dotenv

class EnvVars():
    load_dotenv(".env")
    OPENAI_KEY=os.environ["OPENAI_KEY"]
    AZURE_KEY_1=os.environ["AZURE_KEY_1"]
    AZURE_SERVICE_REGION=os.environ["AZURE_SERVICE_REGION"]
    SPOTIFY_CLIENT_ID=os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET=os.environ["SPOTIFY_CLIENT_SECRET"]
    HISTORY_DIRECTORY=os.environ["HISTORY_DIRECTORY"]
    PROMPTS_DIRECTORY=os.environ["PROMPTS_DIRECTORY"]
