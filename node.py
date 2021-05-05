from utils import quicksort

class Node(object):
    """Used for storing a representation of bayesian network node"""

    def __init__(self, name):
        self.name = name
        self.parents = []
        self.probabilities = [] # list of ConditionalProbability objects

    def __str__(self):  # for easier debugging and visualisation
        return self.name

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
                    return False
                sum_iter = 0
                p_sum = 0
            sum_iter += 1
            p_sum += p.probability

        return True


