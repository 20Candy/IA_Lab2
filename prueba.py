from graphviz import Source
from collections import defaultdict

class Node:
    def __init__(self, name, parents, cpd):
        self.name = name
        self.parents = parents
        self.cpd = cpd
        
class BayesianNetwork:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):        
        self.nodes.append(node)

    def get_probability(self, node_name, value, evidence):
        node = self.nodes[node_name]
        if not node.parents:
            return node.cpd[value]
        parent_values = [evidence[parent.name] for parent in node.parents]
        return node.cpd[tuple(parent_values)][value]


#is_fully_described takes a BayesianNetwork instance and returns a boolean indicating whether the network is fully described, which is defined as whether all of the nodes have a conditional probability distribution.
def is_fully_described(bayesian_network):
    for node in bayesian_network.nodes:
        if node.cpd is None:
            return False
    return True

#This code defines a function to_dot_string that takes a BayesianNetwork instance and returns a string representation of the network in the DOT language. The function starts by creating an empty string dot_string and adding the opening and closing tags for a directed graph, "digraph {\n" and "}". For each node in the network, the function adds a line to dot_string that defines the node and sets its shape to a circle. Then, for each parent of the node, the function adds a line to dot_string that creates an edge from the parent to the node. Finally, the function returns the dot_string.

def to_dot_string(bayesian_network):
    dot_string = "digraph {\n"
    for node in bayesian_network.nodes:
        dot_string += f"\t{node.name} [shape=circle];\n"
        for parent in node.parents:
            dot_string += f"\t{parent.name} -> {node.name};\n"
    dot_string += "}"
    return dot_string

#getFactors
def getFactors(bayesian_network):
    factors = []
    for node in bayesian_network.nodes:
        factor = dict()
        factor["name"] = node.name
        factor["parents"] = [parent.name for parent in node.parents]
        factor["cpd"] = node.cpd
        factors.append(factor)
    return factors


# Use the enumeration algorithm to perform inference
def enumerate_all(bn, variables, evidence):
    if not variables:
        return 1.0
    Y = variables[0]
    if Y in evidence:
        return bn.get_probability(0, evidence[Y], evidence) * enumerate_all(bn, variables[1:], evidence)
    else:
        return sum(bn.get_probability(0, y, evidence) * enumerate_all(bn, variables[1:], evidence) for y in [True, False])
    
    

def query(bn, query):
    variables = list(query.keys())
    evidence = query
    return enumerate_all(bn, variables, evidence)


# Create nodes
A = Node("A", [], 0.5)
B = Node("B", [A], {"A=True": 0.8, "A=False": 0.2})
C = Node("C", [A], {"A=True": 0.6, "A=False": 0.4})

#n this example, we create three nodes A, B, and C, and a Bayesian network bn. The node A does not have any parents and has a prior probability of 0.5. The nodes B and C have A as their parent, and their conditional probability distributions are represented as dictionaries mapping from the parent node's possible values to the probability of the node taking a certain value given those values. 

# Create Bayesian network
bn = BayesianNetwork()
bn.add_node(A)
bn.add_node(B)
bn.add_node(C)


#--------------------------------------------------------------------
# Check if fully described
print(is_fully_described(bn)) # Output: True

#--------------------------------------------------------------------

# Print DOT string
dot_string = to_dot_string(bn)
print(dot_string)

source = Source(dot_string)
source.render("bn", view=True)

#--------------------------------------------------------------------


#Factors in a Bayesian network represent the conditional probability distributions of the random variables in the network.
# A factor can be represented as a dictionary in which the keys are the variables in the factor and the values are the corresponding probabilities

print(getFactors(bn))

#--------------------------------------------------------------------

#enumeration algotihtm
# Define the query
q = {"A": "True", "B": "True", "C": "True"}

print(query(bn, q))

