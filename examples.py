import sys
import os
from bayes_net import BayesNet

def alarm_json():
    bayes_net = BayesNet()  
    file = "alarm.json"
    variable_for_markov_blanket = "burglary"
    
    if bayes_net.load(file):
        print(bayes_net)
        
        print('Markov blanket for ' + variable_for_markov_blanket + ':')
        print(bayes_net.markov_blanket(variable_for_markov_blanket))
        
        print('\nProbability of John_calls under condition that burglary is true:')
        answer = bayes_net.mcmc(
            evidence={"burglary":"T"},
            query=["John_calls"]
            )
        print(answer, '\n')

        print('Probability of earthquake under condition that burglary is true'
            + ' and alarm is true:')
        answer = bayes_net.mcmc(
            evidence={"burglary":"T", "alarm":"T"},
            query=["earthquake"]
            )
        print(answer)
    else:
        print("failed to load file")



if __name__ == '__main__':
    alarm_json()