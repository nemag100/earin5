import json

from collections import defaultdict

from constants import NODES, RELATIONS, PARENTS, PROBABILITIES, REQUIRED_KEYS
from node import Node
from utils import check_file, check_json, split_key, ConditionalProbability

class BayesNet:
    """Used for storing a bayesian network representation."""

    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)

    def __str__(self):
        msg = ''
        valid, _ = self.validate()
        if not valid:
            return msg
        msg += 'Nodes:\n\n'
        for node in self.nodes.items():
            msg += '\"' + node[0] + '\" ' + str(node[1])
        msg += '\nEdges:\n\n'
        for edge in self.edges.items():
            msg += str(edge) + '\n'
        return msg

    def load(self, filename):
        self.nodes = self._load_json(filename)
        self._connect()
        valid, err_msg = self.validate()
        if not valid:
            print('BayesNet invalid.')
            print(err_msg)

    def mcmc(self, evidence={}, query=[]):
        """Returns probability estimates for each query,
        based on provided evidence."""
        answer = ""
        for q in query:
            for n in self.nodes:
                pass
        return answer

    def markov_blanket(self, node):
        """Returns Markov blanket for a given node."""
        res = []
        # list of all nodes but node from the list them:
        all_but_me = lambda them: [n for n in them if n != node]
        # list of all nodes from the list them that are not in res yet:
        unique = lambda them: [n for n in them if n not in res]
        for parent in self.nodes[node].parents: # for all node's parents
            res.append(parent)  # add the parent to res
        for child in self.edges[node]:  # for all node's children
            res.append(child)   # add the child to res
            # append res with the child's other parents not added yet:
            res += unique(all_but_me(self.nodes[child].parents))
        return res

    def validate(self):
        msg = ''
        if not self.nodes:
            msg += 'No nodes initialized.'
            return False, msg
        for node in self.nodes.items():
            valid, err_msg = node[1].validate()
            if not valid:
                self.nodes = {}
                msg += 'Node \"' + node[0] + '\" invalid.'
                msg += err_msg
                return False, msg
        if self.check_cycles():
            msg += 'Cycles found in graph.'
            return False, msg
        return True, msg

    def check_cycles(self):
        """Evaluates to True if the bayesian network graph
        contains cycles, otherwise evaluates to False."""
        visited = []
        r_stack = []

        def neighbour_cycle(vertex):    # inner function of check_cycles
            """Evaluates to True if any visited neighbour
            is in recursion stack, otherwise evaluates to False."""
            visited.append(vertex)
            r_stack.append(vertex)

            for neighbour in self.edges[vertex]:
                if neighbour not in visited and neighbour_cycle(neighbour):
                    return True
                elif neighbour in r_stack:
                    return True

            r_stack.remove(vertex)
            return False

        for node in self.nodes.keys():
            if node not in visited and neighbour_cycle(node):
                return True
        return False

    def _connect(self):
        """Updates edges dictionary."""
        for node in self.nodes.items():
            for parent in node[1].parents:
                self.edges[parent].append(node[0])

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
            values = []
            for item in probability_table.items():
                parents, child = split_key(item[0])
                probability = item[1]
                probabilities.append(ConditionalProbability(parents, child,
                    probability))
                if child not in values:
                    values.append(child)
            node = Node(parents=parents_table, probabilities=probabilities,
                values=values)
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
    print('Markov blanket for ' + args[1] + ':')
    print(bayes_net.markov_blanket(args[1]))

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

