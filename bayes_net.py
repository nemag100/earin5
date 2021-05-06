import json

from constants import NODES, RELATIONS, PARENTS, PROBABILITIES, REQUIRED_KEYS
from node import Node
from utils import check_file, check_json, split_key, ConditionalProbability

class BayesNet:
    """Used for storing a bayesian network representation."""

    def __init__(self):
        self.nodes = {}

    def __str__(self):
        msg = ''
        for node in self.nodes.items():
            msg += '\"' + node[0] + '\" ' + str(node[1])
        return msg

    def load(self, filename):
        self.nodes = self._load_json(filename)
        self.validate()

    def mcmc(self, evidence={}, query=[]):
        """Returns probability estimates for each query,
        based on provided evidence."""
        answer = ""
        for q in query:
            for n in self.nodes:
                pass
        return answer

    def markov_blanket(self):
        pass

    def validate(self):
        if not self.nodes:
            print('No nodes initialized.')
            return False
        for node in self.nodes.values():
            if not node.validate():
                self.nodes = {}
                return False
        return True

    def check_cycles(self):
        """Evaluates to True if the bayesian network graph
        contains cycles, otherwise evaluates to False"""
        pass

    def _load_json(self, filename):
        """Loads json file into the dictionary of nodes."""
        nodes = {}
        if not check_file(filename):
            return nodes
        data = None
        with open(filename, 'r') as file:
            data = json.load(file)
            file.close()
        if not check_json(data, REQUIRED_KEYS):
            return nodes
        for node_name in data[NODES]:
            parents_table = data[RELATIONS][node_name][PARENTS]
            probability_table = data[RELATIONS][node_name][PROBABILITIES]
            probabilities = []
            for item in probability_table.items():
                parents, child = split_key(item[0])
                probability = item[1]
                probabilities.append(ConditionalProbability(parents, child,
                    probability))
            node = Node(parents=parents_table, probabilities=probabilities)
            node.sort()
            valid, err_msg = node.validate()
            if not valid:
                print('Node \"' + node_name + '\" invalid.')
                print(err_msg)
                nodes = {}
                break
            nodes[node_name] = node
        return nodes

def main(args):
    bayes_net = BayesNet()
    bayes_net.load(args[0])
    print(bayes_net)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

