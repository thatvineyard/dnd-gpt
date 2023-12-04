from components.chat import ChatSession
from components.utils.cli.args import Args
from components.utils.engine.gamemaster.gamemaster import GameMaster
from components.utils.engine.state.sessionhandler import SessionHandler
from components.utils.voice.texttospeech import TextToSpeech


def start_cli(
    sessionHandler: SessionHandler, chatSession: ChatSession, textToSpeech: TextToSpeech
):

    sessionHandler.prepareSession(Args.session_file)
    sessionHandler.saveSession()

    chatSession.new_session(sessionHandler.requireSelectedSession())

    gameMaster = GameMaster(chatSession, textToSpeech)

    while True:
        gameMaster.takeTurn()
        sessionHandler.saveSession()
