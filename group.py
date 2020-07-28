

class Group:

    def __init__(self):
        self.persons = []
        self.average_amount = 0
        self.negative_persons = []
        self.positive_persons = []

    def add_person(self, person):
        self.persons.append(person)

    def calculate_average_amount(self):
        # Calculate the amount each person should pay
        for person in self.persons:
            self.average_amount += person.expense
        self.average_amount /= len(self.persons)

    def add_negative_person(self, person):
        self.negative_persons.append(person)

    def add_positive_person(self, person):
        self.positive_persons.append(person)

    def calculate_owings(self):

        total_owings = 0
        for person in self.positive_persons:
            total_owings += person.diff

        for negative_person in self.negative_persons:
            for positive_person in self.positive_persons:

                # Each person with negative difference owes their share of the sum_diff
                # to each person with positive difference
                owes_amount = abs(negative_person.diff * positive_person.diff) / total_owings
                negative_person.owes[positive_person.name] = owes_amount



