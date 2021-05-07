import sys
import ast
import argparse
from bayes_net import BayesNet

class Interface:
    '''Container for user input data'''
    def __init__(self, bayes_net):
        self.evidence = {}
        self.query = []
        self.steps = 1000
        self.bayes_net = bayes_net

def create_bayes_net_from_file(args):
    bayes_net = BayesNet()

    if bayes_net.load(args['file']):
        print("File loaded successfully.")
        return bayes_net
    else:
        print("File load error. Program exit.")
        sys.exit(-1)

def parse_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-f",
        "--file",
        required=True,
        help="json file containing byesian network description"
    )
    ap.add_argument(
        "-e",
        "--evidence",
        required=False,
        help='''for example: "{'burglary':'T', 'alarm': 'T'}"'''
    )
    
    ap.add_argument(
        "-q",
        "--query",
        required=False,
        help='''for example: "['John_calls']"'''
    )
    
    ap.add_argument(
        "-s",
        "--steps",
        required=False,
        help='for example: -s 123456'
    )
    return vars(ap.parse_args())

def print_menu():
    menu = (
            'Available commands:\n'
            '\tmarkov <variable_name>      = print Markov blanket\n'
            '\tevidence <name> <value>     = add evidence with value\n'
            '\tremove_evidence <name>      = remove evidence\n'
            '\tprint_evidence              = shows currently added evidence\n'
            '\tquery <name>                = return probability distribution\n'
            '\tprint_query                 = prints query\n'
            '\tremove_query <name>         = removes query with given name\n'
            '\tsteps <number>              = sets number of steps, default 1000\n'
            '\tnetwork                     = prints the network loaded from file\n'
            '\tMCMC or mcmc                = mcmc using evidence, query, steps\n'
            '\texit                        = exits the program\n'
            '\thelp                        = displays this message\n'
        )
    print(menu)

def get_user_input():
    return input("Input your command:").split()

def markov(variable, interface):
    print("markov blanket for", variable, ":")
    print(interface.bayes_net.markov_blanket(variable))

def print_evidence(interface):
    print(interface.evidence)

def evidence(name, value, interface):
    if name not in interface.bayes_net.nodes.keys():
        raise ValueError(name, "is not a valid evidence node")
    interface.evidence[name] = value

def remove_evidence(name, interface):
    del interface.evidence[name]

def query(name, interface):
    interface.query.append(name)
    
def remove_query(name, interface):
    interface.query.remove(name)
    
def print_query(interface):
    print(interface.query)
    
def steps(number_of_steps, interface):
    interface.steps = int(number_of_steps)

def network(interface):
    print(interface.bayes_net)

def exit(interface):
    sys.exit(0)

def help(interface):
    print_menu()

def mcmc(interface):
    MCMC(interface)

def MCMC(interface):
    answer = interface.bayes_net.mcmc(
        ev=interface.evidence,
        query=interface.query,
        steps=interface.steps
        )
    print("The probability of:", interface.query)
    print("Given that:", interface.evidence)
    print("Obtained in", interface.steps, "steps is:")
    print(answer)

def call_selected_function(user_input, interface):
    try:
        globals()[user_input[0]](*user_input[1:], interface)

    except TypeError as error_message:
        print("Something went wrong: ", error_message)
    except SystemExit:
        sys.exit(0)
    except KeyError as error_message:
        print("Key not found!", error_message)
    except ValueError as error_message:
        print("Wrong value!", error_message)
    except:
        print("Unexpected error: ", sys.exc_info()[0])
    else:
        print("Command accepted.")




if __name__ == '__main__':

    args = parse_arguments()
    bayes_net = create_bayes_net_from_file(args)
    interface = Interface(bayes_net)
    try:
        if args['evidence']:
            print("evidence=",args['evidence'])
            interface.evidence = ast.literal_eval(args['evidence'])
        if args['query']:
            print("query=",args['query'])
            interface.query = ast.literal_eval(args['query'])
        if args['steps']:
            print("steps=",args['steps'])
            print()
            interface.steps = int(args['steps'])
        mcmc(interface)
    except: KeyError
    
    if len(args) > 1:
        sys.exit(0)
    else:
        print_menu()
    
    

    while(True):

        user_input = get_user_input()
        options = ["markov",
                   "evidence",
                   "print_evidence",
                   "remove_evidence",
                   "query",
                   "steps",
                   "network",
                   "mcmc",
                   "MCMC",
                   "exit",
                   "remove_query",
                   "print_query",
                   "help"]

        if user_input[0] is not None and user_input[0] in options:
           # if check_arguments(user_input):
                call_selected_function(user_input, interface)
        else:
            print("Wrong input")







