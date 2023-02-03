from graphviz import Source
from collections import defaultdict

class Node:
    def __init__(self, name, parents, cpd, values):
        self.name = name
        self.parents = parents
        self.cpd = cpd
        self.values = values

        
class BayesianNetwork:
    def __init__(self):
        self.nodes = []
        self.variable_values = {}

    def add_node(self, node):        
        self.nodes.append(node)
        self.variable_values[node.name] = node.values
        self.variables.append(node.name)


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

def enumeration_ask(X, e, bn):
    Q = {}
    for xi in bn.variable_values[X]:
        e[X] = xi
        Q[xi] = enumerate_all(bn.variables, e, bn)
    return normalize(Q)

def enumerate_all(variables, e, bn):
    if len(variables) == 0:
        return 1.0
    Y = variables[0]
    if Y in e:
        return bn.probability(Y, e) * enumerate_all(variables[1:], e, bn)
    else:
        sum = 0
        for yi in bn.variable_values[Y]:
            e[Y] = yi
            sum += bn.probability(Y, e) * enumerate_all(variables[1:], e, bn)
        del e[Y]
        return sum

def normalize(Q):
    total = sum(Q.values())
    for key in Q:
        Q[key] /= total
    return Q




# Create nodes
A = Node("A", [], 0.5, ["True", "False"])
B = Node("B", [A], {"A=True": 0.8, "A=False": 0.2}, ["True", "False"])
C = Node("C", [A], {"A=True": 0.6, "A=False": 0.4}, ["True", "False"])


#n this example, we create three nodes A, B, and C, and a Bayesian network bn. The node A does not have any parents and has a prior probability of 0.5. The nodes B and C have A as their parent, and their conditional probability distributions are represented as dictionaries mapping from the parent node's possible values to the probability of the node taking a certain value given those values. 

# Create Bayesian network
bn = BayesianNetwork()
bn.add_node(A)
bn.add_node(B)
bn.add_node(C)


#--------------------------------------------------------------------
# Check if fully described

print("Iniciso 1. Verificar si es completamente descrita")
descrita = is_fully_described(bn)

if(descrita):
    print("Es completamente descrita")

else:
    print("No es completamente descrita")


#--------------------------------------------------------------------

print("\nIniciso2. Representacion en String")
# Print DOT string
dot_string = to_dot_string(bn)
print(dot_string)

source = Source(dot_string)
source.render("bn", view=True)

#--------------------------------------------------------------------

#Factors in a Bayesian network represent the conditional probability distributions of the random variables in the network.
# A factor can be represented as a dictionary in which the keys are the variables in the factor and the values are the corresponding probabilities

print("\nIniciso3. Factores")
print(getFactors(bn))

#--------------------------------------------------------------------

print("\nIniciso4. Algoritmo de enumeracion")
#enumeration algotihtm
# Define the query
query = {"A": "True", "B": "True", "C": "True"}

result = enumeration_ask("A", query, bn)
print(result)

