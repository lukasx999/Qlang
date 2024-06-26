#!/usr/bin/env python3

import re
import sys
from textwrap import dedent
from typing import Generator, Callable, Any, AnyStr
from pprint import pprint

# Modules
from preprocessor import macro



"""
A calculator language called q
"""



MESSAGE: str = dedent("""\
                      Q - a primitive calculator language
                      usage: qlang <filename.q>\
                      """)
COMMENT_CHAR: str = "#"
LINE_SEPERATOR: str = " "




def prettify_lines(lines: tuple[str]) -> tuple[str]:
    # Remove comments and newline chars
    new: list[str] = [re.sub(f"{COMMENT_CHAR}.*$|\n", "", line) for line in lines]

    # Remove blank lines and trailing whitespace
    new = [line.strip() for line in new if bool(re.search("^$", line)) == False]

    return tuple(new)



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
        self.ASSIGNMENT: str = "ASSIGNMENT"

        # None means that var has not been defined yet
        self.variables: dict[str: int | None] = {}
        self.constants: dict[str: int | None] = {}


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








        # else:
        #     raise Exception("ERROR: input value!")













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



# Returns a dict containing a statement and the equivalent instruction
def get_operation(lines: tuple[str]) -> tuple[dict[str: tuple[str]]]:

    op = Operations()



    DECLARATION_VAR: str = "var"
    DECLARATION_CONST: str = "const"
    ASSIGNMENT_EQUALS: str = "="



    operation = None

    operations: list[dict[str: tuple[str]]] = []

    """
    {[let x]: decl_var}
    """


    for line in lines:
        line: tuple[str] = tuple(line.split(LINE_SEPERATOR))

        # Declaring a variable
        if len(line) == 2 and line[0] == DECLARATION_VAR and line[1].isalpha() == True:
            operation = op.DECLARATION_VAR

        # Declaring a constant
        elif len(line) == 2 and line[0] == DECLARATION_CONST and line[1].isalpha() == True:
            operation = op.DECLARATION_CONST

        # Assignment
        elif len(line) == 3 and line[0].isalpha() == True and line[1] == ASSIGNMENT_EQUALS:
            operation = op.ASSIGNMENT



        else:
            operation = None


        # Unknown operation
        if operation == None:
            raise Exception(f"ERROR: unknown operation `{" ".join(line)}`!")

        print(operation)

        operations.append({operation: line})

    return tuple(operations)








def main() -> None:
    # Take filename as first argument
    if len(sys.argv) < 2:
        print(MESSAGE)
        sys.exit(0)
    else:
        filename: str = sys.argv[1]


    with open(filename, "r") as file:
        lines: tuple[str] = tuple(file.readlines())

    lines = prettify_lines(lines)

    lines = macro(lines)  # Preprocessor


    operations = get_operation(lines)
    execute(operations)





if __name__ == '__main__':
    sys.exit(main())
