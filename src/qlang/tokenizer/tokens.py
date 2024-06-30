

iota_counter: int = 0

def iota(*, reset=False) -> int:
    global iota_counter
    if reset:
        iota_counter = 0

    result = iota_counter
    return result
    iota_counter += 1


class TokenGroups:
    KEYWORD         = iota()
    KEYWORD_SOFT    = iota()
    PUNCTUATION     = iota()
    DATATYPE        = iota()
    IDENTIFIER      = iota()
    INTEGER_LITERAL = iota()




class Tokens:

    class SoftKeywords:
        SOFT_KEYWORDS: dict[str: str] = {
            "IN"            : "in",
            "END_STATEMENT" : "end",
            "ELSE"          : "else",
            "ELSE_IF"       : "elseif",
        }

    class Keywords:
        KEYWORDS: dict[str: str] = {
            "FUNCTION"      : "func",
            "WHILE"         : "while",
            "FOR"           : "for",
            "IF"            : "if",
        }

    class Datatypes:
        DATATYPES: dict[str: str] = {
            "INTEGER"       : "int",
            "FLOAT"         : "float",
            "STRING"        : "string",
            "STACK"         : "stack",
        }


    class Punctuation:
        SINGLE: dict[str: str] = {
            "WHITESPACE"            : " ",
            "COLON"                 : ":",
            "SEMI_COLON"            : ";",
            "COMMA"                 : ",",
            "HASHSIGN"              : "#",
            "DOUBLE_QUOTE"          : '"',
            "SINGLE_QUOTE"          : "'",
            "PAREN_OPEN"            : "(",
            "PAREN_CLOSED"          : ")",
            "SQUARE_BRACKET_OPEN"   : "[",
            "SQUARE_BRACKET_CLOSED" : "]",
            "CURLY_BRACKET_OPEN"    : "{",
            "CURLY_BRACKET_CLOSED"  : "}",
        }


        SINGLE_OR_DOUBLE: dict[str: str] = {
            "EQUALSIGN"             : "=",
            "GREATER_THAN"          : ">",
            "LESS_THAN"             : "<",
            "DASH"                  : "-",
            "BANG"                  : "!",
        }


        DOUBLE: dict[str: str] = {
            "BITSHIFT_RIGHT"        : ">>",
            "BITSHIFT_LEFT"         : "<<",
            "EQUALSIGN_DOUBLE"      : "==",
            "EQUALSIGN_NOT_EQUAL"   : "!=",
            "GREATER_THAN_EQUAL"    : ">=",
            "LESS_THAN_EQUAL"       : "<=",
            "ARROW_RIGHT"           : "->",
            "ARROW_LEFT"            : "<-",
            "DASH_DOUBLE"           : "--",
            "ARROW_RIGHT_DOUBLE"    : "=>",
        }
