

class Person:

    def __init__(self, name, expense):
        self.name = name
        self.expense = expense
        self.diff = 0.0
        self.owes = dict()

    def calculate_diff(self, amount):
        self.diff = self.expense - amount
