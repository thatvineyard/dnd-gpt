# STEP 3

from components.utils.cli.cli_print import cli_print_debug


class SsmlFormatter:
  """
  Utility class that provides static methods for formatting a given text with voice and style into SSML.
  """

  @staticmethod
  def encaseInSSMLTag(text: str):
    """Surround text with speak tags. This is required when sending to Azure speech services."""
    
    prefix = '''
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
      xmlns:mstts="https://www.w3.org/2001/mstts" 
      xml:lang="en-US"
    >
    '''
    postfix = '</speak>'
    return prefix + text + postfix
  
  @staticmethod
  def encaseInVoiceTag(text: str, voice: str):
    """Surround text with voice tags"""
    
    prefix = f'<voice name="{voice}">'
    postfix = '</voice>'
    return prefix + text + postfix

  @staticmethod
  def encaseInSpeakingStyleTag(text: str, style: str, styleDegree: float = 1):
      """Surround text with mstts:express-as tags"""
    
      if styleDegree < 0.01:
        cli_print_debug("Style degree too low, clamping to 0.01")
        styleDegree = 0.01
      if styleDegree > 2:
        cli_print_debug("Style degree too high, clamping to 2")
        styleDegree = 2
      
      prefix = f'<mstts:express-as style="{style}" styledegree="{styleDegree}">'
      postfix = "</mstts:express-as>"

      return prefix + text + postfix

  @staticmethod
  def encaseInRateTag(text: str, rate: float):
      """Surround text with rate tags"""
      
      if rate < 0.5:
        cli_print_debug("Rate too low, clamping to 0.5")
        rate = 0.5
      if rate > 2:
        cli_print_debug("Rate too high, clamping to 2")
        rate = 2
      
      prefix = f'<prosody rate="{rate}">'
      postfix = "</prosody>"

      return prefix + text + postfix
