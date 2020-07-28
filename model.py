from PyQt5.QtCore import *
from person import Person
from group import Group


class Model(QObject):
    """Class for the top level of the program

    """

    # Establish signals
    show_result = pyqtSignal(str, )

    def __init__(self):
        super().__init__()

        self.group = Group()

    def calculate_owings(self):

        self.group.calculate_average_amount()
        for person in self.group.persons:
            person.calculate_diff(self.group.average_amount)

            if person.diff < 0:
                self.group.add_negative_person(person)
            else:
                self.group.add_positive_person(person)

        self.group.calculate_owings()

        for person in self.group.negative_persons:
            print(person.name)
            for key, value in person.owes.items():
                print(key, value)

    def register_expense(self, name, amount):
        self.group.add_person(Person(name, float(amount)))

