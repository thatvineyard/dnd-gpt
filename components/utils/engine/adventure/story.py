class Story:
    def __init__(
        self, synopsis: str | None = None, characters: str | None = None
    ) -> None:
        self.synopsis = synopsis
        self.characters = characters

    @staticmethod
    def fromDict(dict: dict):
        return Story(
            dict["synopsis"],
            dict["characters"],
        )
