
import sys
import re



if __name__ == '__main__':
    print("Do not run this module as a script! Bad things are bound to happen!")
    sys.exit(1)




# Preprocessor
def macro(lines: tuple[str]) -> tuple[str]:
    MACRO: str = "macro"
    EQUALS: str = ":="
    WHITESPACE: str = " "
    FLAG_MACRO_ACCEPT_WHITESPACE: bool = True
    FLAG_MACRO_ENFORCE_UPPER: bool = False
    FLAG_MACRO_ENFORCE_NO_DIGITS: bool = False
    FLAG_MACRO_DISABLE: bool = False


    # Disable macro system entirely
    if FLAG_MACRO_DISABLE == True:
        print(f"MACRO INFO: macros have been manually disabled! enforced by `FLAG_MACRO_DISABLE`")
        return lines



    macros: dict[str: str] = {}

    # Fill dict with macro values
    for line in lines:
        line = tuple(line.split(WHITESPACE))
        if line[0] == MACRO and line[2] == EQUALS:
            name: str = line[1]

            if FLAG_MACRO_ACCEPT_WHITESPACE == True:
                # Accepts statements divided by whitespace
                value: str = WHITESPACE.join(line[3:])
            else:
                value: str = line[3]


            # Checks
            if FLAG_MACRO_ENFORCE_UPPER == True:
                assert name.isupper() == True, f"MACRO ERROR: name of macro `{name}` must be uppercase! enforced by `FLAG_MACRO_ENFORCE_UPPER`"

            if FLAG_MACRO_ENFORCE_NO_DIGITS == True:
                assert line[1].isalpha() == True, f"MACRO ERROR: name of macro `{name}` cannot be a digit! enforced by `FLAG_MACRO_ENFORCE_NO_DIGITS`"


            assert name not in macros, f"MACRO ERROR: macro called `{name}` already exists!"

            macros[name] = value


    # Remove macro statements
    new: list[str] = [re.sub(f"^{MACRO} .* {EQUALS} .*$", "", line) for line in lines]

    # Remove blank lines
    new = [line.strip() for line in new if bool(re.search("^$", line)) == False]



    # Sort by size (longest key first)
    keys = list(macros.keys())
    keys.sort(reverse=True)
    sorted_macros: dict[str: str] = {key: macros[key] for key in keys}


    # if no macros are used, return the given list
    if sorted_macros == {}:
        return lines


    new2: list[str] = []
    for line in new:
        i = 0
        for name, value in sorted_macros.items():

            if bool(re.search(name, line)) == False:
                i += 1
                if i == len(sorted_macros):
                    new2.append(line)

            if bool(re.search(name, line)) == True:
                rep: str = re.sub(name, value, line)
                new2.append(rep)
                break


    return new2
