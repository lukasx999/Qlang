
class SoftKeywords:
    # Keywords that can only be used, if other keywords have already been used
    IN = "in"
    END_STATEMENT = "end"
    ELSE          = "else"
    ELSE_IF       = "elseif"

class Keywords:
    FUNCTION      = "func"
    WHILE         = "while"
    FOR           = "for"
    IF            = "if"

class Datatypes:
    INTEGER       = "int"
    FLOAT         = "float"
    STRING        = "string"
    STACK         = "stack"


class Punctuation:
    class Single:
        # Single chars
        WHITESPACE            = " "
        COLON                 = ":"
        SEMI_COLON            = ";"
        COMMA                 = ","
        HASHSIGN              = "#"
        DOUBLE_QUOTE          = '"'
        SINGLE_QUOTE          = "'"
        ###########################
        PAREN_OPEN            = "("
        PAREN_CLOSED          = ")"
        SQUARE_BRACKET_OPEN   = "["
        SQUARE_BRACKET_CLOSED = "]"
        CURLY_BRACKET_OPEN    = "{"
        CURLY_BRACKET_CLOSED  = "}"

    class SingleOrDouble:
        # Single or double
        EQUALSIGN             = "="
        GREATER_THAN          = ">"
        LESS_THAN             = "<"
        DASH                  = "-"
        BANG                  = "!"

    class Double:
        # Double chars
        BITSHIFT_RIGHT        = ">>"
        BITSHIFT_LEFT         = "<<"
        EQUALSIGN_DOUBLE      = "=="
        EQUALSIGN_NOT_EQUAL   = "!="
        GREATER_THAN_EQUAL    = ">="
        LESS_THAN_EQUAL       = "<="
        ARROW_RIGHT           = "->"
        ARROW_LEFT            = "<-"
        DASH_DOUBLE           = "--"
        ARROW_RIGHT_DOUBLE    = "=>"
