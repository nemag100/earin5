class ConditionalProbability():
    """Used for storing atomized key values and corresponding
    probabilities."""

    def __init__(self, parents, child, probability):
        self.parents = parents
        self.child = child
        self.probability = probability

    def __eq__(self):
        return self.child == other.child and self.parents == other.parents

    def __lt__(self, other):
        if not self.child == other.child:
            return self.child < other.child
        else:
            return self.parents < other.parents

    def __gt__(self, other):
        if not self.child == other.child:
            return self.child > other.child
        else:
            return self.parents > other.parents

    def validate(self):
        """Evaluates to True if the probability is defined."""
        return False if not self.probability else True

def quicksort(array):
    """Sorts the array by means of the the quicksort algorithm."""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for a in array:
            if a < pivot:
                less.append(a)
            elif a == pivot:
                equal.append(a)
            elif a > pivot:
                greater.append(a)
        return quicksort(less) + equal + quicksort(greater)
    return array

def split_key(key):
    """Splits the key of probabilities dictionary according to notation
    proposed in EARIN Exercise 5. Returned values:
        parents - string of parent key values separated by commas,
                  empty string when no parents are present;
        child   - string of child key value."""
    child = key.split(',')[-1]
    cut = len(child) + 1
    parents = key[:-cut]
    return parents, child

def main():
    """demo"""

    boolean_values = "T,T,F"
    color_values = "blue,green,yellow,red,blue"
    single_value = "single"

    print(boolean_values)
    split_booleans = split_key(boolean_values)
    if not split_booleans[0]:
        print('>>no parents<<')
    print(split_booleans[0])
    print(split_booleans[1])

    print(color_values)
    split_colors = split_key(color_values)
    if not split_colors[0]:
        print('>>no parents<<')
    print(split_colors[0])
    print(split_colors[1])

    print(single_value)
    split_single = split_key(single_value)
    if not split_single[0]:
        print('>>no parents<<')
    print(split_single[0])
    print(split_single[1])

if __name__ == '__main__':
    main()
