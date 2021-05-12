import random
from random import choice

from constants import PARENTS, PROBABILITIES
from utils import indent, quicksort


class Node:
    """Used for storing a representation of bayesian network node"""

    def __init__(self, parents=[], probabilities=[], values=[]):
        self.parents = parents  # list of Node's parents
        # list of ConditionalProbability objects for conditional
        # probabilities of events in Node:
        self.probabilities = probabilities
        self.values = values    # list of Node's possible values

    def __str__(self):
        n_values = len(self.values)
        msg = '{\n'
        msg += indent() + '\"' + PARENTS + '\": ['
        for i, parent in enumerate(self.parents):
            if i:
                msg += ','
            msg += '\"' + parent + '\"'
        msg += '],\n'
        msg += indent() + '\"' + PROBABILITIES + '\": {\n' + indent(n=2)
        for i, probability in enumerate(self.probabilities):
            if i:
                msg += ','
                if not (i) % n_values == 0:
                    msg += ' '
                else:
                    msg += '\n' + indent(n=2)
            msg += str(probability)
        msg += '\n' + indent() + '}\n}\n'
        return msg

    def get_probability(self, events):
        """Returns probabilities of given events chain."""
        return self.probabilities[events]

    def random(self):
        """Returns value drawn from self.values."""
        return choice(self.values)

    def _r(self):
        s = 0.0
        totals = dict.fromkeys(self.values, 0.0)
        for p in self.probabilities:
            totals[p.child] += p.probability
            s += p.probability
        for k in totals.keys():
            totals[k] /= s

        random_value = random.random()
        total = 0.0
        for value, probability in totals.items():
            total += probability
            if random_value <= total:
                return value

    def sort(self):
        """Sorts probabilities by their children values, then by their
        parents values, in alphabetical order"""
        self.probabilities = quicksort(self.probabilities)

    def validate(self):
        """Evaluates to True if the node has defined probabilities
        and the probability tables are correct, according to notation
        and requirements from EARIN Exercise 5. Otherwise evaluates
        to False."""
        self.sort()

        msg = ''

        sum_iter = 0
        p_sum = 0
        n_values = len(self.values)

        if not self.probabilities:
            msg += 'No probabilities assigned.'
            return False, msg

        for p in self.probabilities:
            sum_iter += 1
            p_sum += p.probability
            if sum_iter == n_values:
                if p_sum != 1:
                    msg += ('In parent probability(-ies) \"' + p.parents
                            + '\" total probability is not 1.0.\n'
                            + 'Total probability: ' + str(p_sum))
                    return False, msg
                sum_iter = 0
                p_sum = 0

        return True, msg
