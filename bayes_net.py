class BayesNet(object):
    """Used for storing a bayesian network representation."""

    def __init__(self):
        self.nodes = []

    def check_cycles(self):
        """Evaluates to True if the bayesian network graph
        contains cycles, otherwise evaluates to False"""
        pass

    def mcmc(self, evidence={}, query=[]):
        """Returns probability estimates for each query,
        based on provided evidence."""
        answer = ""
        for q in query:
            for n in nodes:
                pass
        return answer
