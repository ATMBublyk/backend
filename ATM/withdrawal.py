class Withdrawal:
    count = 0

    def __init__(self):
        self.count += 1
        self.__id = self.count
        self.__date = None
        self.__amount = 0
