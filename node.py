class Node(object):
    """Used for storing a representation of bayesian network node"""

    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []
        self.probabilities = {}

    def __str__(self):  # for easier debugging and visualisation
        return self.name

    def get_probability(events):
        """Returns probabilities of given events chain."""
        return self.probabilities[events]
