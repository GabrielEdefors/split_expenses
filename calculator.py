from group import Group

def calculate_transactions(group: Group):

    # Calculate the amount each person should pay
    amount = 0
    for person in group.persons:
        amount += person.amount
    amount /= len(group.persons)

    positive_difference = dict()
    negative_difference = dict()
    sum_diff = 0
    for key, value in expenses.items():

        # Store all differences to the amount
        diff = value - amount

        if diff >= 0:
            positive_difference[key] = diff
            sum_diff += diff

        else:
            negative_difference[key] = diff


    # Each person with negative difference owes their share of the sum_diff to each person with positive difference



