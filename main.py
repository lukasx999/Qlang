#!/usr/bin/env python3

import re
import sys
from textwrap import dedent
from typing import Generator, Callable, Any, AnyStr
from pprint import pprint
from copy import deepcopy


# Modules
# from include.preprocessor import macro, include
import include.preprocessor as prepro
from include.stack import Stack




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

        self.DECLARATION_STACK: str = "DECLARATION_STACK"
        self.STACK_PUSH: str = "STACK_PUSH"
        self.STACK_POP: str = "STACK_POP"

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





    def declaration_var(self, *, name: str) -> None:
        if name in self.variables:
            raise Exception("ERROR: variable already exists!")

        if name in self.constants:
            raise Exception(f"ERROR: constant of the name {name} already exists!")

        self.variables[name] = None


    def declaration_const(self, *, name: str) -> None:
        if name in self.constants:
            raise Exception("ERROR: constant already exists!")

        if name in self.variables:
            raise Exception(f"ERROR: variable of the name {name} already exists!")

        self.constants[name] = None



    def declaration_stack(self, *, name: str) -> None:
        assert name not in self.stacks, f"STACK ERROR: stack named `{name}` already exists!"
        self.stacks[name] = Stack()


    def stack_push(self, *, name: str, value: str) -> None:
        assert name in self.stacks, f"STACK ERROR: stack named `{name}` does not exist!"
        stack = self.stacks[name]

        if value.isdigit() == True:
            stack.push(value)

        elif value.isalpha() == True:
            raise NotImplementedError("pushing variables onto the stack is not yet supported!")  # TODO: add this feature



    def stack_pop(self, *, name: str) -> None:
        assert name in self.stacks, f"STACK ERROR: stack named `{name}` does not exist!"
        stack = self.stacks[name]

        stack.pop()




    def assignment(self, *, name: str, value: str | int) -> None:

            # Assign a variable (all the time)
            if name in self.variables:
                if value.isdigit() == True:
                    self.variables[name] = value


                # Assign a variable to another variable/constant
                if value.isalpha() == True:
                    if value in self.variables:
                        assert self.variables[value] != None, f"variable `{value}` has not been defined yet!"
                        self.variables[name] = self.variables[value]

                    elif value in self.constants:
                        assert self.constants[value] != None, f"constant `{value}` has not been defined yet!"
                        self.variables[name] = self.constants[value]

                    else: raise Exception(f"ERROR: variable/const `{value}` has not been defined yet!")



            # Assign a constant (once)
            elif name in self.constants:

                if self.constants[name] == None:
                    if value.isdigit() == True:
                        self.constants[name] = value

                    # Assign a constant to another variable/constant
                    if value.isalpha() == True:
                        if value in self.variables:
                            assert self.variables[value] != None, f"variable `{value}` has not been defined yet!"
                            self.constants[name] = self.variables[value]

                        elif value in self.constants:
                            assert self.variables[value] != None, f"constant `{value}` has not been defined yet!"
                            self.constants[name] = self.constants[value]

                        else: raise Exception(f"ERROR: variable/const `{value}` has not been defined yet!")



                else: raise Exception(f"ERROR: cannot assign value to constant `{name}` which is associated with value {self.constants[name]}! constants can only be assigned once!")


            else: raise Exception(f"ERROR: variable/constant named `{name}` does not exist! declare it using `var/const {name}`!")













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


                # Stack
                case op.DECLARATION_STACK:
                    name = values[1]
                    op.declaration_stack(name=name)


                # Push onto Stack
                case op.STACK_PUSH:
                    value = values[1]
                    name = values[3]
                    op.stack_push(name=name, value=value)


                # Poping from the Stack (no assignment)
                case op.STACK_POP:
                    name = values[2]
                    op.stack_pop(name=name)



                # Assigning value to var/const (can be another var/const)
                case op.ASSIGNMENT:
                    name = values[0]  # var/const name
                    value = values[2]
                    op.assignment(name=name, value=value)













                case _:
                    raise Exception("ERROR: operation has not yet been implemented!")

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

    DECLARATION_STACK: str = "stack"
    STACK_PUSH: str = "push"
    STACK_PUSH_KEYWORD: str = "in"
    STACK_POP: str = "pop"
    STACK_POP_KEYWORD: str = "from"


    # Prepro
    INCLUDE: str = "include!"
    MACRO: str = "macro!"
    MACRO_EQUALS: str = ":="



    operation = None

    operations: list[dict[str: tuple[str]]] = []



    for line in lines:
        line: tuple[str] = tuple(line.split(TOKEN_SEPERATOR))
        print(line)


        # Declaring a variable
        if len(line) == 2 and line[0] == DECLARATION_VAR and line[1].isalpha() == True:
            operation = op.DECLARATION_VAR

        # Declaring a constant
        elif len(line) == 2 and line[0] == DECLARATION_CONST and line[1].isalpha() == True:
            operation = op.DECLARATION_CONST

        # Declaring a stack
        elif len(line) == 2 and line[0] == DECLARATION_STACK and line[1].isalpha() == True:
            operation = op.DECLARATION_STACK

        # Pushing a value onto the stack
        elif len(line) == 4 and line[0] == STACK_PUSH and line[2] == STACK_PUSH_KEYWORD and line[3].isalpha() == True:
            operation = op.STACK_PUSH

        # Poping a value from the stack
        elif len(line) == 3 and line[0] == STACK_POP and line[1] == STACK_POP_KEYWORD and line[2].isalpha() == True:
            operation = op.STACK_POP




        # Assignment
        elif len(line) == 3 and line[0].isalpha() == True and line[1] == ASSIGNMENT_EQUALS:
            operation = op.ASSIGNMENT





        # Ignore preprocessor directives

        # Include
        elif len(line) == 2 and line[0] == INCLUDE:
            continue

        # Macro
        elif line[0] == MACRO and MACRO_EQUALS in line and len(line) >= 4:  # HACK: does not check for :=
            continue                                                        # gets replaced by prepro



        else:
            operation = None

        # Unknown operation
        if operation == None:
            raise Exception(f"ERROR: unknown operation `{" ".join(line)}`!")

        print(operation)

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




    # Configure the preprocessor
    prepro.Arguments.FLAG_MACRO_DISABLE = False


    # Run preprocessor directives: Include external libraries
    lines = prettify_lines(lines)
    lines = prepro.include(lines)


    # Run preprocessor directives: Macros
    lines = prettify_lines(lines)
    lines = prepro.macro(lines)

    operations = get_operation(lines)
    execute(operations)





if __name__ == '__main__':
    sys.exit(main())
