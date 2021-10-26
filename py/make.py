from abc import abstractmethod


class Make():

    @abstractmethod
    def __new__(cls):
        return super().__new__(cls)

    def save(self=None):
        return 'save is called'

    def take(self=None):
        return 'taker script'

    def exec(query):
        print(f'"{query}" executed')  