import copy
import json
import random

from collections import defaultdict
from random import choice

from constants import NODES, RELATIONS, PARENTS, PROBABILITIES, REQUIRED_KEYS
from node import Node
from utils import check_file, check_json, split_key, quicksort
from utils import ConditionalProbability


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
            return False
        return True

    def mcmc(self, ev={}, query=[], steps=1000):
        """Returns probability estimates for each query,
        based on provided evidence."""
        evidence = copy.copy(ev)
        # list of all nodes for whom there no evidence was provided:
        unknown = [n for n in self.nodes.keys() if n not in evidence.keys()]
        for u in unknown:
            evidence[u] = self.random(u)
        # Set the counters for variables of interest:
        counters = {}
        values_of_interest = lambda q: [v for v in self.nodes[q].values]
        for q in query:
            counters[q] = dict.fromkeys(values_of_interest(q), 0.0)
        # Random walking:
        for s in range(steps):
            x = choice(unknown)  # Draw a node not belonging to evidence
            evidence[x] = self.mb_sampling(x, evidence)
            for q in query:
                counters[q][evidence[q]] += 1
        # Normalize counters to get a probability distribution:
        s = dict.fromkeys(counters.keys(), 0.0)
        for c, v in counters.items():
            for p in v.values():
                s[c] += p
        for c, v in counters.items():
            for k in v.keys():
                counters[c][k] /= s[c]
        return counters

    def markov_blanket(self, node):
        """Returns Markov blanket for a given node."""
        res = []
        # list of all nodes but node from the list them:
        all_but_me = lambda them: [n for n in them if n != node]
        # list of all nodes from the list them that are not in res yet:
        unique = lambda them: [n for n in them if n not in res]
        for parent in self.nodes[node].parents:  # for all node's parents
            res.append(parent)  # add the parent to res
        for child in self.edges[node]:  # for all node's children
            res.append(child)   # add the child to res
            # append res with the child's other parents not added yet:
            res += unique(all_but_me(self.nodes[child].parents))
        return res

    def mb_sampling(self, node, evidence):
        """Returns probability sampled with conditioning on Markov
        blanket."""
        values = quicksort(self.nodes[node].values)
        probabilities = dict.fromkeys(values)
        for value in values:
            probabilities[value] = self.p_value(node, evidence, value)
        s = 0.0
        for value in values:
            s += probabilities[value]
        for value in values:
            probabilities[value] /= s
        random_value = random.random()
        total = 0.0
        for value, probability in probabilities.items():
            total += probability
            if random_value <= total:
                return value

    def p_value(self, node, ev, value):
        """Returns probability for node to take given value."""
        # P(X=x_j|Parents(X)):
        evidence = copy.copy(ev)
        evidence[node] = value
        res = self.p_conditional(node, evidence, value)
        # PI_(Z in Children(X))(P(Z=z_i|Parents(Z))):
        for c in self.edges[node]:
            res *= self.p_conditional(c, evidence, evidence[c])
        return res

    def p_conditional(self, node, evidence, value):
        """Returns conditional probability of node taking its value
        from the evidence list, under condition of parents taking
        values from that list."""
        p_x_c_parents = 0.0  # P(X=x_j|Parents(X))
        e_parents = ''  # evidence for node's parents
        for i, p in enumerate(self.nodes[node].parents):
            if i:
                e_parents += ','
            #print('    ', evidence[p])
            e_parents += evidence[p]
        c1 = lambda p: p.parents == e_parents
        c2 = lambda p: p.child == value
        for p in self.nodes[node].probabilities:
            if c1(p) and c2(p):
                p_x_c_parents = p.probability
                #print(node, value, p.probability)
        return p_x_c_parents

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

    def random(self, node):
        """Returns value drawn from node's values."""
        return self.nodes[node].random()

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
    steps = int(args[2]) if len(args) == 3 else 1000
    bayes_net = BayesNet()
    bayes_net.load(args[0])
    print(bayes_net)
    print('Markov blanket for ' + args[1] + ':')
    print(bayes_net.markov_blanket(args[1]))
    print()
    if args[0] == "alarm.json":
        print('Probability of John_calls under condition'
              + ' that burglary is true:')
        answer = bayes_net.mcmc(evidence={"burglary": "T"},
                                query=["John_calls"], steps=steps)
        print(answer)
        print()
        print('Probability of earthquake under condition that burglary is true'
              + ' and alarm is true:')
        answer = bayes_net.mcmc(evidence={"burglary": "T", "alarm": "T"},
                                query=["earthquake"], steps=steps)
        print(answer)

        """
        jt, jf, et, ef, = 0.0, 0.0, 0.0, 0.0
        print("\nLooking for errors...")
        err_cnt = 0
        for i in range(1000):
            answer = bayes_net.mcmc(evidence={"burglary":"T"},
                query=["John_calls"], steps=steps)
            j = answer["John_calls"]
            jt += j["T"]
            jf += j["F"]
            if j["T"] < j["F"]:
                err_cnt += 1
            answer = bayes_net.mcmc(evidence={"burglary":"T", "alarm":"T"},
                query=["earthquake"], steps=steps)
            e = answer["earthquake"]
            et += e["T"]
            ef += e["F"]
            if e["T"] > e["F"]:
                err_cnt += 1
            if i != 0 and i % 100 == 0:
                print(i, '/ 1000')
        print('jt:', jt/1000, 'jf:', jf/1000)
        print('et:', et/1000, 'ef:', ef/1000)
        print("Errors", err_cnt)
        """

    elif args[0] == "flower.json" or args[0] == "f2.json":
        print('Probability of flower_species under condition'
              + ' that color is red:')
        answer = bayes_net.mcmc(evidence={"color": "red"},
                                query=["flower_species"], steps=steps)
        print(answer)
        print()
        print('Probability of flower_species under condition'
              + ' that color is blue:')
        answer = bayes_net.mcmc(evidence={"color": "blue"},
                                query=["flower_species"], steps=steps)
        print(answer)
        print()
        print('Probability of color under condition'
              + ' that flower_species is rose:')
        answer = bayes_net.mcmc(evidence={"flower_species": "rose"},
                                query=["color"], steps=steps)
        print(answer)
        print()
        print('Probability of color under condition'
              + ' that flower_species is tulip:')
        answer = bayes_net.mcmc(evidence={"flower_species": "tulip"},
                                query=["color"], steps=steps)
        print(answer)
        print()
        print('Probability of color under condition'
              + ' that flower_species is iris:')
        answer = bayes_net.mcmc(evidence={"flower_species": "iris"},
                                query=["color"], steps=steps)
        print(answer)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
