# STEP 3

from enum import Enum


class Voices(Enum):
  ARIA = "en-US-AriaNeural"
  GUY = "en-US-GuyNeural"
  JASON = "en-US-JasonNeural"
  TONY = "en-US-TonyNeural"
  SARA = "en-US-SaraNeural"
  NANCY = "en-US-NancyNeural"
  JANE = "en-US-JaneNeural"
  JENNY = "en-US-JennyNeural"
  DAVIS = "en-US-DavisNeural"
  AMBER = "en-US-AmberNeural"
  ANA = "en-US-AnaNeural"
  ANDREW = "en-US-AndrewNeural"
  ASHLEY = "en-US-AshleyNeural"
  BRANDON = "en-US-BrandonNeural"
  BRIAN = "en-US-BrianNeural"
  CHRISTOPHER = "en-US-ChristopherNeural"
  CORA = "en-US-CoraNeural"
  ELIZABETH = "en-US-ElizabethNeural"
  EMMA = "en-US-EmmaNeural"
  ERIC = "en-US-EricNeural"
  JACOB = "en-US-JacobNeural"
  MICHELLE = "en-US-MichelleNeural"
  MONICA = "en-US-MonicaNeural"
  ROGER = "en-US-RogerNeural"
  STEFFAN = "en-US-SteffanNeural"
  BLUE = "en-US-BlueNeural"

class Styles(Enum): 
  angry = "angry"                     # Expresses an angry and annoyed tone.
  chat = "chat"                       # Expresses a casual and relaxed tone.
  cheerful = "cheerful"               # Expresses a positive and happy tone.
  customerservice = "customerservice" # Expresses a friendly and helpful tone for customer support.
  excited = "excited"                 # Expresses an upbeat and hopeful tone. It sounds like something great is happening and the speaker is happy about it.
  friendly = "friendly"               # Expresses a pleasant, inviting, and warm tone. It sounds sincere and caring.
  hopeful = "hopeful"                 # Expresses a warm and yearning tone. It sounds like something good will happen to the speaker.
  sad = "sad"                         # Expresses a sorrowful tone.
  shouting = "shouting"               # Expresses a tone that sounds as if the voice is distant or in another location and making an effort to be clearly heard.
  whispering = "whispering"           # Expresses a soft tone that's trying to make a quiet and gentle sound.
  terrified = "terrified"             # Expresses a scared tone, with a faster pace and a shakier voice. It sounds like the speaker is in an unsteady and frantic status.
  unfriendly = "unfriendly"           # Expresses a cold and indifferent tone.
