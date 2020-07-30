from PyQt5.QtCore import *
from person import Person
from group import Group
from enum import Enum


class Model(QObject):
    """Class for the top level logic of the program
    """

    # Establish signals
    show_result = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # Currency
        self.currency = "kr"

        self.group = Group()

    def compute(self):
        """This methods performs the actual computations
        """
        if len(self.group.persons) < 2:
            raise TooFewPersonsError()

        else:

            # Calculate the average amount
            self.group.calculate_average_amount()

            # Calculate the difference to this amount for each person
            for person in self.group.persons:
                person.calculate_diff(self.group.average_amount)

                if person.diff < 0:
                    self.group.add_negative_person(person)
                else:
                    self.group.add_positive_person(person)

            # Now calculate what the persons with negative difference owes each person with positive difference
            self.group.calculate_owings()

            # Emit a signal to display result
            self.emit_result()

    def emit_result(self):
        message = []

        for i, neg_person in enumerate(self.group.negative_persons):
            for pos_person_name, pos_person_value in neg_person.owes.items():
                message.append(f"{neg_person.name} should pay {pos_person_name} {int(pos_person_value)} {self.currency}")

        self.show_result.emit(message)

    def register_expense(self, name, amount):
        self.group.add_person(Person(name, float(amount)))

    def reset_group(self):
        self.group = Group()

    def set_currency(self, currency: Enum):

        if currency.name == "SEK":
            self.currency = 'kr'
        elif currency.euro == "euro":
            self.currency = "€"
        else:
            self.currency = "$"


class TooFewPersonsError(ValueError):

    def __init__(self):
        pass


class Currency(Enum):
    """Provides different currencies"""

    SEK = 1
    euro = 2
    dollar = 3

