
from components.utils.voice.ssmlformatter import SsmlFormatter

# STEP 3

class TtsScript:
  """
  A class used to build a text-to-speech script by adding lines with different voices and emotions. 
  Once the script has had lines added it can be turned to SSML (used by Azure's TTS) by using `toSSML()`.
  """
  
  def __init__(self, defaultVoice: str = "en-US-AriaNeural"):
      self.lines: list[TtsLine] = []
      self.defaultVoice = defaultVoice
  
  def addLine(self, text: str, voice: str = "", style: str = "", styleDegree: int = 1, rate: int = -1, print_prefix: str = ""):
    """Use this function to add a line to the script"""
    
    if(not voice or voice == ""):
      voice = self.defaultVoice
    
    self.lines.append(TtsLine(text, voice, style, styleDegree, rate, print_prefix))
    
  def toSSML(self):      
    """Converts this script to a SSML format to be used by Azure text-to-speech service."""
    
    allLines = "\n".join(map(lambda line: line.toSSML(), self.lines))
    allLines = SsmlFormatter.encaseInSSMLTag(allLines)
    return allLines

  def toString(self):
    """Formats the script for printing in the console."""
    return "\n".join(map(lambda line: f'{line.print_prefix}{line.text}', self.lines))

class TtsLine:
  """
  Represents a line to be read in a certain voice and style. 
  """
  
  def __init__(self, text: str, voice: str, style: str = "", styleDegree: int = 1, rate: int = -1, print_prefix: str = ""):
    self.text = text
    self.voice = voice
    self.style = style
    self.styleDegree = styleDegree
    self.rate = rate
    self.print_prefix = print_prefix
  
  def toSSML(self):
    """Adds SSML tags to line. Note that it does not add the final tags that are required to send to Azure TTS, so make sure to run encaseInSSMLTag on the collection of SSML lines."""
    ssml_text = self.text
    if(self.style != ""):
        ssml_text = SsmlFormatter.encaseInSpeakingStyleTag(ssml_text, self.style, self.styleDegree)
    if(self.rate != -1):
        ssml_text = SsmlFormatter.encaseInRateTag(ssml_text, self.rate)
    ssml_text = SsmlFormatter.encaseInVoiceTag(ssml_text, self.voice)
        
    return ssml_text