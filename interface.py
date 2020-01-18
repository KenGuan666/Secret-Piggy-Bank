class Interface:
    pass

class TerminalInterface(Interface):

    def display(self, text):
        print(text)
    
    def display_and_await_input(self, text):
        self.display(text)
        return self.await_input()

    def display_and_await_input_with_check(self, text, func):
        self.display(text)
        return self.await_input_with_check(func)

    def await_input(self):
        return str.lower(input()).strip()

    def await_input_with_check(self, func):
        while True:
            response = self.await_input()
            check = func(response)
            if check:
                self.display(check)
            else:
                return response

def createNewInterface():
    return TerminalInterface()
