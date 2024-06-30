#!/usr/bin/env python3

import re
import sys
from textwrap import dedent
from typing import Generator, Callable, Any, AnyStr
from pprint import pprint
from copy import deepcopy

# Third party
from icecream import ic


# Modules
from include.preprocessor import define, include, Arguments
from include.stack import Stack, StackError

from tokenizer.tokenizer import tokenizer
from tokenizer.token_checker import token_checker





MESSAGE: str = dedent("""\
                      Q - a primitive programming language
                      usage: qlang <filename.q>\
                      """)

COMMENT_CHAR: str = "#"
DOCSTRING_START: str = "->"
DOCSTRING_END: str = "<-"

TOKEN_SEPERATOR: str = " "




def prettify_lines(lines: tuple[str]) -> tuple[str]:
    FLAG_DOCSTRING_ENFORCE_END: str = True


    # Remove comments and newline chars
    no_comments_newlines: list[str] = [re.sub(f"{COMMENT_CHAR}.*$|\n", "", line) for line in lines]

    # Remove blank lines and trailing whitespace
    no_blank_whitespace = [line.strip() for line in no_comments_newlines if bool(re.search("^$", line)) == False]

    # Remove docstrings
    no_docstring: list[str] = []
    docstring_flag: bool  = False

    for line in no_blank_whitespace:

        if tuple(line.split(TOKEN_SEPERATOR)) == (DOCSTRING_START,):
            docstring_flag = True

        if docstring_flag == False:
            no_docstring.append(line)

        if tuple(line.split(TOKEN_SEPERATOR)) == (DOCSTRING_END,):
            docstring_flag = False



    if FLAG_DOCSTRING_ENFORCE_END == True:
        assert docstring_flag == False, f"ERROR: docstring has not been ended with `{DOCSTRING_END}`!"



    return tuple(no_docstring)






class Operations:
    _instance = None

    # Singleton
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance





    def __init__(self) -> None:

        # Operation identifiers
        self.DECLARATION_VAR: str = "DECLARATION_VAR"
        self.DECLARATION_CONST: str = "DECLARATION_CONST"

        self.DECLARATION_STACK_DYNAMIC: str = "DECLARATION_STACK_DYNAMIC"
        self.STACK_PUSH: str = "STACK_PUSH"
        self.STACK_POP: str = "STACK_POP"

        self.DECLARATION_STACK_STATIC: str = "DECLARATION_STACK_STATIC"


        self.ASSIGNMENT: str = "ASSIGNMENT"

        # None means that var has not been defined yet
        self.variables: dict[str: int | None] = {}
        self.constants: dict[str: int | None] = {}

        self.stacks: dict[str: Stack] = {}



    @property
    def varconst(self) -> dict[str: int | None]:  # Holds all variables and constants
        vars: dict[str: int | None] = deepcopy(self.variables)
        const: dict[str: int | None] = deepcopy(self.constants)

        vars.update(const)

        return vars



    def _check_varconst_exist(self, name: str, /) -> None:
        """
        check if a variable or constant by the name of `name` already exists
        throw an error if it does
        """
        assert name not in self.varconst, f"ERROR: var/const of the name {name} already exists!"



    def declaration_var(self, *, name: str) -> None:
        self._check_varconst_exist(name)
        self.variables[name] = None


    def declaration_const(self, *, name: str) -> None:
        self._check_varconst_exist(name)
        self.constants[name] = None



    def _check_stack_exist(self, name) -> None:
        """
        checks if a stack already exists
        if not raise an exception (TODO: raise exception, not assertion)
        """
        assert name not in self.stacks, f"STACK ERROR: stack named `{name}` already exists!"


    def declaration_stack_dynamic(self, *, name: str) -> None:
        self._check_stack_exist(name)
        self.stacks[name] = Stack()


    def declaration_stack_static(self, *, name: str, size: int) -> None:
        self._check_stack_exist(name)
        self.stacks[name] = Stack(size=size)


    def stack_push(self, *, name: str, value: str) -> None:
        assert name in self.stacks, f"STACK ERROR: stack named `{name}` does not exist!"
        stack = self.stacks[name]

        if value.isdigit() == True:
            try:
                stack.push(value)
            except StackError:  # pushing to static stack
                assert False, f"STATIC STACK ERROR: cannot exceed stack size of `{stack.size}`!"

        elif value.isalpha() == True:
            raise NotImplementedError("pushing variables onto the stack is not yet supported! use a macro instead! :)")  # TODO: add this feature


    def stack_pop(self, *, name: str) -> None:
        assert name in self.stacks, f"STACK ERROR: stack named `{name}` does not exist!"
        stack = self.stacks[name]

        try:
            stack.pop()
        except StackError:  # Poping empty stack
            raise Exception("STACK ERROR: cannot pop from empty stack!")





    def assignment(self, *, name: str, value: str | int) -> None:
        assert name in self.varconst, f"ERROR: variable/constant named `{name}` does not exist! declare it using `var/const {name}`!"

        # Determine if value is a var/const or a numberic literal
        val: str | None = None

        # Assign a numeric literal
        if value.isdigit() == True:
            val = value


        # Assign value of another var/const to this var/const
        elif value.isalpha() == True:
            assert value in self.varconst and self.varconst[value] != None, f"ERROR: var/const named `{value}` does not exist or has not been defined yet!"
            val = self.varconst[value]

        else:
            assert False, f"UNKNOWN ERROR: `{value}` is not a alphabetic value nor a digit?! what the hell!"


        # Determine if the to be assigned var/const is of type var or const
        if name in self.variables:
            self.variables[name] = val

        elif name in self.constants:
            assert self.constants[name] == None, f"CONST ERROR: constant named `{name}` due to its nature cannot be redefined!"
            self.constants[name] = val

        else:
            assert False, f"UNKNOWN ERROR: var/const `{name}` is not a variable nor a constant?! what the hell!"







def execute(operations: tuple[dict[tuple[str]: str]]) -> None:

    op = Operations()

    # print(operations)
    for operation in operations:

        for op_name, values in operation.items():

            match op_name:

                case op.DECLARATION_VAR:
                    name = values[1]
                    op.declaration_var(name=name)


                case op.DECLARATION_CONST:
                    name = values[1]
                    op.declaration_const(name=name)


                # Dynamic Stack
                case op.DECLARATION_STACK_DYNAMIC:
                    name = values[1]
                    op.declaration_stack_dynamic(name=name)


                # Push onto Stack
                case op.STACK_PUSH:
                    value = values[1]
                    name = values[3]
                    op.stack_push(name=name, value=value)


                # Poping from the Stack (no assignment)
                case op.STACK_POP:
                    name = values[2]
                    op.stack_pop(name=name)



                # Static Stack
                case op.DECLARATION_STACK_STATIC:
                    name: str = values[1]
                    size: int = int(values[3])
                    op.declaration_stack_static(name=name, size=size)




                # Assigning value to var/const (can be another var/const)
                case op.ASSIGNMENT:
                    name = values[0]  # var/const name
                    value = values[2]
                    op.assignment(name=name, value=value)













                case _:
                    raise Exception("ERROR: operation has not yet been implemented!")

    # Debugging
    print("variables: ", end="")
    print(op.variables)
    print("constants: ", end="")
    print(op.constants)
    print("var/const: ", end="")
    print(op.varconst)
    print("stacks: ", end="")
    print(op.stacks)



# Returns a dict containing a statement and the equivalent instruction
def get_operation(lines: tuple[str]) -> tuple[dict[str: tuple[str]]]:

    op = Operations()

    DECLARATION_VAR: str = "var"
    DECLARATION_CONST: str = "const"
    ASSIGNMENT_EQUALS: str = "="

    # Dynamic Stack
    DECLARATION_STACK: str = "stack"
    STACK_PUSH: str = "push"
    STACK_PUSH_KEYWORD: str = "onto"
    STACK_POP: str = "pop"
    STACK_POP_KEYWORD: str = "from"


    # Static Stack
    STACK_STATIC: str = "stack"
    STACK_STATIC_KEYWORD: str = "of"



    # Prepro
    INCLUDE: str = "include!"  # TODO: share this variable with include/preprocessor
    MACRO: str = "define!"  # TODO: share this variable with include/preprocessor
    MACRO_EQUALS: str = "..."  # TODO: share this variable with include/preprocessor



    operation = None

    operations: list[dict[str: tuple[str]]] = []



    for line in lines:
        line: tuple[str] = tuple(line.split(TOKEN_SEPERATOR))


        # Define the syntax of the language
        declaration_var: Callable = lambda: len(line) == 2 and line[0] == DECLARATION_VAR and line[1].isalpha() == True
        declaration_const: Callable = lambda: len(line) == 2 and line[0] == DECLARATION_CONST and line[1].isalpha() == True

        declaration_stack_dynamic: Callable = lambda: len(line) == 2 and line[0] == DECLARATION_STACK and line[1].isalpha() == True
        declaration_stack_static: Callable = lambda: len(line) == 4 and line[0] == STACK_STATIC and line[1].isalpha() == True and line[2] == STACK_STATIC_KEYWORD
        stack_push: Callable = lambda: len(line) == 4 and line[0] == STACK_PUSH and line[2] == STACK_PUSH_KEYWORD and line[3].isalpha() == True
        stack_pop: Callable = lambda: len(line) == 3 and line[0] == STACK_POP and line[1] == STACK_POP_KEYWORD and line[2].isalpha() == True

        assignment: Callable = lambda: len(line) == 3 and line[0].isalpha() == True and line[1] == ASSIGNMENT_EQUALS

        prepro_include: Callable = lambda: len(line) == 2 and line[0] == INCLUDE
        prepro_define: Callable = lambda: line[0] == MACRO and MACRO_EQUALS in line and len(line) >= 4 # HACK: does not check for :=



        # Declaring a variable
        if declaration_var() == True:
            operation = op.DECLARATION_VAR

        # Declaring a constant
        elif declaration_const() == True:
            operation = op.DECLARATION_CONST

        # Declaring a dynamic stack
        elif declaration_stack_dynamic() == True:
            operation = op.DECLARATION_STACK_DYNAMIC

            # Declaring a static stack
        elif declaration_stack_static() == True:
            operation = op.DECLARATION_STACK_STATIC

        # Pushing a value onto the stack
        elif stack_push() == True:
            operation = op.STACK_PUSH

        # Poping a value from the stack
        elif stack_pop() == True:
            operation = op.STACK_POP

        # Assignment
        elif assignment() == True:
            operation = op.ASSIGNMENT


        # Ignore preprocessor directives
        elif prepro_include() | prepro_define() == True:
            continue




        # Unknown operation
        else: raise Exception(f"ERROR: unknown operation `{" ".join(line)}`!")


        operations.append({operation: line})

    return tuple(operations)














def get_lines(filename: str) -> tuple[str]:
    with open(filename, "r") as file:
        lines: tuple[str] = tuple(file.readlines())
    return lines



def main() -> None:
    # Take filename as first argument
    if len(sys.argv) < 2:
        print(MESSAGE)
        sys.exit(0)
    else:
        filename: str = sys.argv[1]

    lines: tuple[str] = get_lines(filename)


    """
    simulation flow:
    input file -> preprocessor -> tokenizer -> execution
    """


    # Configure the preprocessor
    Arguments.FLAG_DEFINE_DISABLE = False

    # Run preprocessor directives: Include external libraries
    # lines = prettify_lines(lines)
    # lines = include(lines)

    # Run preprocessor directives: Macros
    # lines = prettify_lines(lines)
    # lines = define(lines)





    # lines = prettify_lines(lines)

    tokens: tuple[tuple[str]] = tokenizer(lines)

    ic(tokens)

    checked_tokens: tuple[tuple[str]] = token_checker(tokens)

    return
    operations = get_operation(lines)
    execute(operations)





if __name__ == '__main__':
    sys.exit(main())
