from components.chat import ChatSession
from components.parser import InputTextFormatError, parse
from components.utils.cli.cliprint import cli_input, cli_print_error, cli_print_warn
from components.utils.voice.texttospeech import TextToSpeech


def start_cli(chatSession: ChatSession, textToSpeech: TextToSpeech):
    while True:
        # STEP 1: Receives a text from console input.
        question: str = cli_input("INPUT: ")

        # STEP 1: ask openAI for an answer
        answer: str = chatSession.chat(question)

        # STEP 3: Extract parsing to it's own function
        assistance = None
        attempts = 0
        while not assistance:
            attempts += 1
            if attempts > 3:
                cli_print_error(
                    "Did not understand response from OpenAI. Please try again (press up on keyboard to get back previous message)"
                )
                break
            try:
                assistance = parse(answer, textToSpeech)
                assistance.execute()
            except InputTextFormatError:
                chatSession.removeLastMessageFromHistory()
                cli_print_warn(
                    "Error parsing answer, asking OpenAI for a better format."
                )
                answer: str = chatSession.chat(
                    f"{question} - And remember to format the response properly"
                )
