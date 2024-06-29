

import re
import sys
from typing import Generator, Callable, Any, AnyStr

from icecream import ic

from tokenizer.cursor import CharCursor
from tokenizer.tokens import Keywords, SoftKeywords, Punctuation, Datatypes


if __name__ == '__main__':
    print("do not run this module as a script!")
    sys.exit(1)



class TokenError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)







class Token:
    def __init__(self) -> None:
        self.name = ...
        self.type = ...
        self.value = ...

    def __repr__(self) -> str:
        return f"{self.name} with type: {self.type} with value of: {self.value}"




def tokenizer(lines: tuple[str]) -> tuple[tuple[str]]:
    """
    takes a list containing strings representing each line
    outputs a list containing tuples which contain strings representing each token
    """


    tokens: list[list[str]] = []

    for line in lines:
        ic(line)
        # Convert line to tuple of single chars
        chars: tuple[str] = tuple(line)
        line_tokens: list[str] = []

        cursor = CharCursor(chars)
        query_char: list[str] = []


        # Move the cursor along the line
        while not cursor.end_reached:


            """
            add char to query, so that it can my matched later
            """
            if cursor.is_string:
                query_char.append(cursor.current)



            """
            if its not a string, it must be punctuation
            """
            if not cursor.is_string:
                match cursor.current:
                    case Punctuation.Single.WHITESPACE:
                        line_tokens.append("whitespace")

                    case Punctuation.Single.COMMA:
                        line_tokens.append("comma")

                    case Punctuation.Single.COLON:
                        line_tokens.append("colon")

                    case Punctuation.Single.SEMI_COLON:
                        line_tokens.append("semi_colon")

                    case Punctuation.Single.HASHSIGN:
                        line_tokens.append("hashsign")

                    case Punctuation.Single.DOUBLE_QUOTE:
                        line_tokens.append("double_quote")

                    case Punctuation.Single.SINGLE_QUOTE:
                        line_tokens.append("single_quote")

                    case Punctuation.Single.PAREN_OPEN:
                        line_tokens.append("paren_open")

                    case Punctuation.Single.PAREN_CLOSED:
                        line_tokens.append("paren_closed")

                    case Punctuation.Single.CURLY_BRACKET_OPEN:
                        line_tokens.append("curly_open")

                    case Punctuation.Single.CURLY_BRACKET_CLOSED:
                        line_tokens.append("curly_closed")

                    case Punctuation.Single.SQUARE_BRACKET_OPEN:
                        line_tokens.append("square_open")

                    case Punctuation.Single.SQUARE_BRACKET_CLOSED:
                        line_tokens.append("square_closed")





                    case Punctuation.SingleOrDouble.GREATER_THAN:
                        match cursor.next_two_chars:
                            case Punctuation.Double.GREATER_THAN_EQUAL:
                                line_tokens.append("greater_than_equal")
                                cursor.forward()

                            case Punctuation.Double.BITSHIFT_RIGHT:
                                line_tokens.append("bitshift_right")
                                cursor.forward()

                            case _:
                                line_tokens.append("greater_than")



                    case Punctuation.SingleOrDouble.LESS_THAN:
                        match cursor.next_two_chars:
                            case Punctuation.Double.LESS_THAN_EQUAL:
                                line_tokens.append("less_than_equal")
                                cursor.forward()

                            case Punctuation.Double.BITSHIFT_LEFT:
                                line_tokens.append("bitshift_left")
                                cursor.forward()

                            case Punctuation.Double.ARROW_LEFT:
                                line_tokens.append("arrow_left")
                                cursor.forward()

                            case _:
                                line_tokens.append("less_than")



                    case Punctuation.SingleOrDouble.DASH:
                        match cursor.next_two_chars:
                            case Punctuation.Double.ARROW_RIGHT:
                                line_tokens.append("arrow_right")
                                cursor.forward()

                            case Punctuation.Double.DASH_DOUBLE:
                                line_tokens.append("dash_double")
                                cursor.forward()

                            case _:
                                line_tokens.append("punctuation_dash")


                    case Punctuation.SingleOrDouble.EQUALSIGN:
                        match cursor.next_two_chars:
                            case Punctuation.Double.EQUALSIGN_DOUBLE:
                                line_tokens.append("equalsign_double")
                                cursor.forward()

                            case Punctuation.Double.ARROW_RIGHT_DOUBLE:
                                line_tokens.append("arrow_right_double")
                                cursor.forward()

                            case _:
                                line_tokens.append("equalsign")


                    case Punctuation.SingleOrDouble.BANG:
                        match cursor.next_two_chars:
                            case Punctuation.Double.EQUALSIGN_NOT_EQUAL:
                                line_tokens.append("equalsign_not_equal")
                                cursor.forward()

                            case _:
                                line_tokens.append("bang")



            """
            if the next char is not a string (a-zA-Z) match the query for results
            if the cursor is on the last char and that char is a string, still match the query
            """
            if not cursor.next_is_string:
                match "".join(query_char):
                    case Keywords.FUNCTION:
                        line_tokens.append("keyword_function")

                    case Keywords.WHILE:
                        line_tokens.append("keyword_while")

                    case Keywords.FOR:
                        line_tokens.append("keyword_for")

                    case Keywords.IF:
                        line_tokens.append("if")

                    case SoftKeywords.END_STATEMENT:
                        line_tokens.append("end_statement")

                    case SoftKeywords.IN:
                        line_tokens.append("in")

                    case SoftKeywords.ELSE:
                        line_tokens.append("else")

                    case SoftKeywords.ELSE_IF:
                        line_tokens.append("else_if")


                    case Datatypes.INTEGER:
                        line_tokens.append("datatype_integer")

                    case Datatypes.FLOAT:
                        line_tokens.append("datatype_float")

                    case Datatypes.STRING:
                        line_tokens.append("datatype_string")

                    case Datatypes.STACK:
                        line_tokens.append("datatype_stack")

                    case _:
                        if not query_char == []:
                            line_tokens.append("identifier")


                query_char.clear()  # Reset queries








            cursor.forward()

            # ic(query_char)
        # ic(line_tokens)

        tokens.append(tuple(line_tokens))

    return tuple(tokens)
