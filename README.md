# earin5
**EARIN exercise 5** *by Jakub Szwed, Arkadiusz Zdanowski*

**Usage example:**

```console
python main.py -f alarm.json -e "{'burglary':'T', 'alarm':'T'}" -q "['earthquake']" -s 10000
```

The above should give the following results:

```console
File loaded successfully.
evidence = {'burglary':'T', 'alarm':'T'}
query = ['earthquake']
steps = 10000

The probability of: ['earthquake']
Given that: {'burglary': 'T', 'alarm': 'T'}
Obtained in 10000 steps is:
{'earthquake': {'T': 0.0233, 'F': 0.9767}}
```

For help, type:

```console
python main.py --help
```
