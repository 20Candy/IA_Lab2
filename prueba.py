from graphviz import Source
from collections import defaultdict
import itertools


class Node:
    def __init__(self, name, parents, cpd, values):
        self.name = name
        self.parents = parents if parents else []
        self.cpd = cpd
        self.values = values

        
class BayesianNetwork:
    def __init__(self):
        self.nodes = []
        self.variable_values = {}
        self.variables = []
    
    def add_node(self, node):
        self.nodes.append(node)
        self.variable_values[node.name] = node.values
        self.variables.append(node.name)

    def get_node(self, name):
        return [node for node in self.nodes if node.name == name][0]
    
    def get_parents(self, name):
        return [node for node in self.nodes if name in [parent.name for parent in node.parents]]

    def get_children(self, name):
        return [node for node in self.nodes if node.name in [parent.name for parent in self.get_parents(name)]]

    def probability(self, variable, evidence):
        node = self.get_node(variable)
        if not node.parents:
            return node.cpd
        else:
            parent_values = [evidence[parent.name] for parent in node.parents]
            parent_values_string = ", ".join([f"{parent.name}={value}" for parent, value in zip(node.parents, parent_values)])
            return node.cpd[parent_values_string]



def is_fully_described(bn):
    for node in bn.nodes:
        if not node.parents:
            if node.cpd not in [0, 1]:
                return False
        else:
            parent_values = list(itertools.product(*[bn.variable_values[parent.name] for parent in node.parents]))
            parent_values_string = ", ".join([f"{parent.name}={value}" for parent, value in zip(node.parents, parent_values)])
            if node.cpd[parent_values_string] not in [0, 1]:
                return False
    return True

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


#create enuumeration_ask using addition and marginalization
def enumeration_ask(X, e, bn):
    Q = defaultdict(float)
    for xi in bn.variable_values[X.name]:
        e[X] = xi
        Q[xi] = enumerate_all(bn.variables, e, bn)
    normalize(Q)
    return Q

def enumerate_all(variables, e, bn):
    if not variables:
        return 1.0
    Y = variables[0]
    if Y in e:
        return bn.probability(Y, e) * enumerate_all(variables[1:], e, bn)
    else:
        return sum(bn.probability(Y, {**e, Y: y}) * enumerate_all(variables[1:], e, bn) for y in bn.variable_values[Y])
    
def normalize(Q):
    total = sum(Q.values())
    for key in Q:
        Q[key] /= total


# Create nodes
#Name, parents, cpd, values
A = Node("Earthquake", [], 0.001, ["True", "False"])
B = Node("Burglary", [], 0.002, ["True", "False"])
C = Node("Alarm", [A, B], {"A=True, B=True": 0.95, "A=True, B=False": 0.94, "A=False, B=True": 0.29, "A=False, B=False": 0.001}, ["True", "False"])
D = Node("JohnCalls", [C], {"C=True": 0.9, "C=False": 0.1}, ["True", "False"])
E = Node("MaryCalls", [C], {"C=True": 0.7, "C=False": 0.3}, ["True", "False"])


# Create Bayesian network
bn = BayesianNetwork()
bn.add_node(A)
bn.add_node(B)
bn.add_node(C)
bn.add_node(D)
bn.add_node(E)


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


print("\nIniciso3. Factores")
print(getFactors(bn))

#--------------------------------------------------------------------

print("\nIniciso4. Algoritmo de enumeracion")

probability = enumeration_ask(E, {A: True},bn)
print(probability)

