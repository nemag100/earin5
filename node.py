from constants import PARENTS, PROBABILITIES
from utils import indent, quicksort

class Node():
    """Used for storing a representation of bayesian network node"""

    def __init__(self, parents=[], probabilities=[]):
        self.parents = parents
        self.probabilities = probabilities  # list of
                                            # ConditionalProbability
                                            # objects

    def __str__(self):
        n_distinct_children = self.n_distinct_children()
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
                if not (i + 1) % n_distinct_children == 0:
                    msg += ' '
                else:
                    msg += '\n' + indent(n=2)
            msg += str(probability)
        msg += indent() + '\n}'
        msg += '\n'
        return msg

    def get_probability(self, events):
        """Returns probabilities of given events chain."""
        return self.probabilities[events]

    def sort(self):
        """Sorts probabilities by their children values, then by their
        parents values, in alphabetical order"""
        self.probabilities = quicksort(self.probabilities)

    def n_distinct_children(self):
        """Returns number of distinct child values across
        the probabilities list."""
        distinct_children = []
        for p in self.probabilities:
            if p.child not in distinct_children:
                distinct_children.append(p)
        return len(distinct_children)

    def validate(self):
        """Evaluates to True if the node has defined probabilities
        and the probability tables are correct, according to notation
        and requirements from EARIN Exercise 5. Otherwise evaluates
        to False."""
        self.sort()

        sum_iter = 0
        p_sum = 0
        n_distinct_children = self.n_distinct_children()

        for p in self.probabilities:
            if not p.validate():
                return False
            if sum_iter == n_distinct_children:
                if p_sum != 1:
                    print('Total probability exceeds 1.0.')
                    return False
                sum_iter = 0
                p_sum = 0
            sum_iter += 1
            p_sum += p.probability

        return True


