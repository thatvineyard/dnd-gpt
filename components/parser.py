import json
from components.assistance import Assistance
from components.utils.cli.cliprint import cli_print_debug, cli_print_error, cli_print_info
from components.utils.voice.azurevoices import Voices
from components.utils.voice.charactervoices import mapCharacterToVoice, mapEmotionToStyle, selectVoice, gm_voice, gm_style
from components.utils.voice.texttospeech import TextToSpeech
from components.utils.voice.ttsscript import TtsScript

# STEP 3

def parse(text: str, textToSpeech: TextToSpeech = None) -> Assistance:
  """A function which takes in text and acts on it"""
    
  assistance = Assistance()
    
  # Try to load the json. This will fail if the assistant decides to answer in a non-JSON way, 
  # which it will do a lot. 
  try:
    character_index = text.find('[')
    if character_index < 0:
      character_index = text.find('{')
    if character_index < 0:
      raise ValueError
    text = text[character_index:]
  except ValueError:
    cli_print_debug("Could not find '[' or '{' in string")
    pass
  
  try:
    character_index = text.find(']')
    if character_index < 0:
      character_index = text.find('}')
    if character_index < 0:
      raise ValueError
    text = text[:character_index + 1]
  except ValueError:
    cli_print_debug("Could not find '[' or '{' in string")
    pass  

  try:
    lines = json.loads(text)
  except json.JSONDecodeError as error:
    cli_print_debug("Error decoding JSON")
    raise InputTextFormatError(error)

  script = TtsScript()
  skillChecks = []

  # If we only got one line for some reason, put it in a list
  if isinstance(lines, dict):
    lines = [lines]

  # Go through each line given in the response and add a line to the TTS script
  for line in lines:
    
    character = line.get('character', 'gm')
    text = line.get('text', '')
    emotion = line.get('emotion', 'Normal')
    
    voice = selectVoice(character)
    style = mapEmotionToStyle(emotion)
    print_prefix = f'{character}: '
    
    gm_prefix = ""

    rate=1

    if character == "gm":
      script.addLine(text, voice=gm_voice, style=gm_style, styleDegree=2, rate=rate, print_prefix=gm_prefix)
    else:
      parts = text.split("\"")
      for i, part in enumerate(parts):
        part = part.strip()
        if i % 2 == 0:
          if part == "":
            continue
          cli_print_debug(voice)
          script.addLine(part, voice=gm_voice, style=gm_style, styleDegree=2, rate=rate, print_prefix=gm_prefix)
        else:
          if part == "":
            continue
          script.addLine(part, voice=voice, style=style, styleDegree=2, rate=rate, print_prefix=print_prefix)

    try: 
      skillCheckDc = int(line.get('skillCheck', -1))
    except:
      skillCheckDc = -1

    skillCheckPrompt = line.get('skillCheckPrompt', '')


    if skillCheckDc >= 0:
      skillChecks.append(f'{skillCheckPrompt} ({skillCheckDc})')

  # Set up the actions in the assistance.
  assistance.addAction(lambda : cli_print_info(script.toString()), "🖨️ Printing script")
  # if(textToSpeech):
  assistance.addAction(lambda: textToSpeech.speakScript(script), "🗣️ Speaking script")
  assistance.addAction(lambda : print("\n".join(skillChecks)), "🖨️ Printing script")

  return assistance


class InputTextFormatError(Exception):
  "Raised format of input text cannot be handled by the parser"

