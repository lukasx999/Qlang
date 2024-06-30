
import re

class CharCursor:
    def __init__(self, charlist: tuple[str]) -> None:
        self.charlist: tuple[str] = charlist
        self.index: int = 0


    @property
    def end_reached(self) -> bool:
        return True if self.index == len(self.charlist) else False


    @property
    def next_char(self) -> str:
        # If cursor is at the last char, returns the last char
        next = self.charlist[self.index+1]
        return next


    @property
    def current(self) -> str:
        return self.charlist[self.index]


    @property
    def next_is_string(self) -> bool:
        """
        return false if there is no next char, because its the last char
        """
        try:
            next = self.next_char
            return bool(re.search("[a-zA-Z1-9]", next))
        except IndexError:
            return False


    @property
    def next_two_chars(self) -> str:
        """
        returns the next 2 chars as a string
        if the current char is the last one, return an empty string
        """
        try:
            next_two: list[str] = [self.current, self.next_char]
            result: str = "".join(next_two)
            return result
        except IndexError:
            return ""


    @property
    def is_string(self) -> bool:
        return bool(re.search("[a-zA-Z1-9]", self.current))

    def forward(self) -> None:
        self.index += 1
