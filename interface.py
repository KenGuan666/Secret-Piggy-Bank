
class Interface:
    pass

class TerminalInterface(Interface):

    def display(self, text):
        print(text)
    
    def display_and_await_input(self, text):
        print(text)
        return input()

def createNewInterface():
    return TerminalInterface()
