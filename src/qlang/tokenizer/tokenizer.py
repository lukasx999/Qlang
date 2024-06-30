

import re
import sys
from typing import Generator, Callable, Any, AnyStr

from icecream import ic

from tokenizer.cursor import CharCursor
from tokenizer.tokens import Tokens, TokenGroups



if __name__ == '__main__':
    print("do not run this module as a script!")
    sys.exit(1)


class TokenError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)





class Token:
    def __init__(self, group, type_, value) -> None:
        self.group: int = group
        self.type_: int = type_

        # string: user defined | int: constant from class
        self.value: str = value

    def __repr__(self) -> str:
        repr: str = f"group: {self.group}, type_: {self.type_}, value: {self.value}"
        return repr





def tokenizer(lines: tuple[str]) -> tuple[tuple[str]]:
    """
    takes a list containing strings representing each line
    outputs a list containing tuples which contain strings representing each
    token
    """


    tokens: list[list[str]] = []


    for line in lines:
        print(line)
        # Convert line to tuple of single chars
        chars: tuple[str] = tuple(line)
        line_tokens: list[str] = []

        cursor = CharCursor(chars)
        query_chars: list[str] = []


        # Move the cursor along the line
        while not cursor.end_reached:





            """
            add char to query, so that it can my matched later
            """
            if cursor.is_string:
                query_chars.append(cursor.current)


            """
            if its not a string, it must be punctuation
            """
            if not cursor.is_string:


                # Single character punctuation
                for key, value in Tokens.Punctuation.SINGLE.items():
                    if cursor.current == value:
                        line_tokens.append(Token(TokenGroups.PUNCTUATION, key, value))



                # Single/Double character punctuation
                match: bool = False
                for key, value in Tokens.Punctuation.SINGLE_OR_DOUBLE.items():
                    if cursor.current == value:
                        for key_double, value_double in Tokens.Punctuation.DOUBLE.items():

                            if cursor.next_two_chars == value_double:
                                line_tokens.append(Token(TokenGroups.PUNCTUATION, key_double, value_double))
                                cursor.forward()
                                match = True

                        if not match:
                            line_tokens.append(Token(TokenGroups.PUNCTUATION, key, value))




            """
            if the next char is not a string (a-zA-Z),
            match the query for results
            if the cursor is on the last char and that char is a string,
            still match the query
            """


            query_string: str = "".join(query_chars)


            if not cursor.next_is_string:



                match: bool = False

                for key, value in Tokens.Keywords.KEYWORDS.items():
                    if query_string == value:
                        line_tokens.append(Token(TokenGroups.KEYWORD, key, value))
                        match = True


                for key, value in Tokens.SoftKeywords.SOFT_KEYWORDS.items():
                    if query_string == value:
                        line_tokens.append(Token(TokenGroups.SOFT_KEYWORD, key, value))
                        match = True

                for key, value in Tokens.Datatypes.DATATYPES.items():
                    if query_string == value:
                        line_tokens.append(Token(TokenGroups.DATATYPE, key, value))
                        match = True




                if not match:
                    if not query_chars == []:
                        # Check for integer literals (numbers only)
                        if bool(re.search(r"^[1-9]*$", query_string)):
                            line_tokens.append(Token(TokenGroups.INTEGER_LITERAL, "LITERAL", query_string))

                        else:  # identifiers (text and numbers)
                            line_tokens.append(Token(TokenGroups.IDENTIFIER, "IDENTIFIER", query_string))












                query_chars.clear()  # Reset queries

            cursor.forward()

            # ic(query_char)
        # ic(line_tokens)

        tokens.append(tuple(line_tokens))

    return tuple(tokens)
