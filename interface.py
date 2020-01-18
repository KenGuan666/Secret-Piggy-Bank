
class Interface:
    pass

class TerminalInterface(Interface):

    def display(self, text):
        print(text)
    
    def display_and_await_input(self, text):
        self.display(text)
        return self.await_input()

    def await_input(self):
        return str.lower(input()).strip()

def createNewInterface():
    return TerminalInterface()
