from components.utils.voice.azurevoices import Styles, Voices


def selectVoice(character_name: str):
    voice_list = [e.value for e in Voices]
    voice_index = hash(character_name) % len(voice_list)
    if voice_list[voice_index] in reserved_voices:
        return selectVoice(f"{character_name}x")
    return voice_list[voice_index]


gm_voice = Voices.SARA.value
gm_style = ""
reserved_voices = [gm_voice]


def mapCharacterToVoice(character: str):
    """Switch function to get the correct voice"""

    match character:
        case "Aria":
            return Voices.ARIA
        case "Guy":
            return Voices.GUY
        case "Jason":
            return Voices.JASON
        case "Tony":
            return Voices.TONY
        case "Sara":
            return Voices.SARA
        case "Nancy":
            return Voices.NANCY
        case "Jane":
            return Voices.JANE
        case "Jenny":
            return Voices.JENNY
        case _:
            return Voices.ARIA


def mapEmotionToStyle(emotion: str):
    """Switch function to get the correct style"""

    match emotion:
        case "Sad":
            return Styles.sad.value
        case "Angry":
            return Styles.angry.value
        case "Happy":
            return Styles.cheerful.value
        case "Terrified":
            return Styles.terrified.value
        case "Shouting":
            return Styles.shouting.value
        case "Whispering":
            return Styles.whispering.value
        case "Excited":
            return Styles.excited.value
        case "Normal":
            return ""
        case _:
            return ""
