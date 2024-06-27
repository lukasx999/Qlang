

class StackError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)




class Stack:
    def __init__(self, size=None) -> None:
        self.stack = []
        self.size: int | None = size

    def push(self, value: int) -> None:
        if self.size == None:
            self.stack.append(value)
        else:

            if len(self.stack) == self.size:
                raise StackError("exceeding stack size!")
            else:
                self.stack.append(value)





    def pop(self) -> int:
        try:
            return self.stack.pop()
        except IndexError:
            raise StackError("cannot pop from empty stack!")



    def __repr__(self) -> str:
        return str(self.stack)
