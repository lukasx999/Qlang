
import sys
import re



if __name__ == '__main__':
    print("Do not run this module as a script! Bad things are bound to happen!")
    sys.exit(1)


# Preprocessor directives have a trailing bang



class Arguments:

    # Include
    QLANG_FILE_EXTENSION = "q"
    FLAG_INCLUDE_ENFORCE_TOP: str = True

    # Macro
    FLAG_MACRO_ACCEPT_WHITESPACE: bool = True
    FLAG_MACRO_ENFORCE_UPPER: bool = False
    FLAG_MACRO_ENFORCE_NO_DIGITS: bool = False
    FLAG_MACRO_DISABLE: bool = False




def _read(*, filename: str) -> list[str]:
    with open(filename, "r") as file:
        lines: list[str] = file.readlines()
    return lines




def include(lines: tuple[str]) -> tuple[str]:

    INCLUDE: str = "include!"
    WHITESPACE: str = " "


    # Dont run include directive if there are none
    i = 0


    streak = False
    stop = False

    for line in lines:
        if bool(re.search(f"^{INCLUDE} .*$", line)) == True:
            streak = True

        else:
            i += 1
            stop = True
            streak = False


    if Arguments.FLAG_INCLUDE_ENFORCE_TOP == True:
        assert stop == True and streak == False, "INCLUDE ERROR: all include statements must be at the top! enforced by `FLAG_INCLUDE_ENFORCE_TOP`"



    if i == len(lines):
        return lines




    new_lines: list[str] = []

    main_lines: list[str] = list(lines)

    for line in main_lines:
        line: tuple[str] = line.split(WHITESPACE)

        if len(line) == 2 and line[0] == INCLUDE:
            filename: str = f"{line[1]}.{Arguments.QLANG_FILE_EXTENSION}"
            extern_lines: list[str] = _read(filename=filename)

            for line in extern_lines:
                new_lines.append(line)

            for line in main_lines:
                new_lines.append(line)



    return new_lines




# Preprocessor
def macro(lines: tuple[str]) -> tuple[str]:
    MACRO: str = "define!"
    EQUALS: str = "..."  # Used to be :=
    WHITESPACE: str = " "


    # Disable macro system entirely
    if Arguments.FLAG_MACRO_DISABLE == True:
        print(f"MACRO INFO: macros have been manually disabled! enforced by `FLAG_MACRO_DISABLE`")
        return lines



    macros: dict[str: str] = {}

    # Fill dict with macro values
    for line in lines:
        line = tuple(line.split(WHITESPACE))
        if line[0] == MACRO and line[2] == EQUALS:
            name: str = line[1]

            if Arguments.FLAG_MACRO_ACCEPT_WHITESPACE == True:
                # Accepts statements divided by whitespace
                value: str = WHITESPACE.join(line[3:])
            else:
                value: str = line[3]


            # Checks
            if Arguments.FLAG_MACRO_ENFORCE_UPPER == True:
                assert name.isupper() == True, f"MACRO ERROR: name of macro `{name}` must be uppercase! enforced by `FLAG_MACRO_ENFORCE_UPPER`"

            if Arguments.FLAG_MACRO_ENFORCE_NO_DIGITS == True:
                assert line[1].isalpha() == True, f"MACRO ERROR: name of macro `{name}` cannot be a digit! enforced by `FLAG_MACRO_ENFORCE_NO_DIGITS`"


            assert name not in macros, f"MACRO ERROR: macro called `{name}` already exists!"

            macros[name] = value



    # Remove macro statements
    # new: list[str] = [re.sub(f"^{MACRO} .* {EQUALS} .*$", "", line) for line in lines]
    # Remove blank lines
    # new = [line.strip() for line in new if bool(re.search("^$", line)) == False]





    # Sort by size (longest key first)
    keys = list(macros.keys())
    keys.sort(reverse=True)
    sorted_macros: dict[str: str] = {key: macros[key] for key in keys}


    # if no macros are used, return the given list
    if sorted_macros == {}:
        return lines


    new: list[str] = []
    for line in lines:
        i = 0
        for name, value in sorted_macros.items():

            if bool(re.search(name, line)) == False:
                i += 1
                if i == len(sorted_macros):
                    new.append(line)

            if bool(re.search(name, line)) == True:
                rep: str = re.sub(name, value, line)
                new.append(rep)
                break


    return new

