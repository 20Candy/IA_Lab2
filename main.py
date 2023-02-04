import itertools
from graphviz import Source

class Node:
    def __init__(self, name, values, parents=None, probability=None):
        self.name = name
        self.values = values
        self.parents = parents if parents else []
        self.probability = probability

    def add_parent(self, parent):
        self.parents.append(parent)

class BayesianNetwork:
    def __init__(self):
        self.nodes = {}
        self.variables = []

    def add_node(self, node):
        self.nodes[node.name] = node


    def calculate_probability(self, node, values):
        parent_values = [values[parent.name] for parent in node.parents]
        # Obtener la probabilidad a partir de una tabla de probabilidades o cálculo empírico
        probability = ...
        return probability

    def is_complete(self):
        for node in self.nodes.values():
            if not node.parents:
                return False
            for parent_values in itertools.product(*[parent.values for parent in node.parents]):
                if not self.calculate_probability(node, dict(zip([parent.name for parent in node.parents], parent_values))):
                    return False

    def to_dot_string(self):
        dot_string = "digraph {\n"
        for node in self.nodes.values():
            dot_string += f"\t{node.name} [shape=circle];\n"
            for parent in node.parents:
                dot_string += f"\t{parent.name} -> {node.name};\n"
        dot_string += "}"
        return dot_string

    def enumeration_ask(self, X, e):
        Q = {}
        for xi in X.values:
            e[X.name] = xi
            Q[xi] = self.enumerate_all(self.variables, e)
        return self.normalize(Q)

    def enumerate_all(self, variables, e):
        if not variables:
            return 1.0
        Y = variables[0]
        if Y in e:
            return self.probability(Y, e) * self.enumerate_all(variables[1:], e)
        else:
            return sum(self.probability(Y, self.extend(e, Y, yv)) * self.enumerate_all(variables[1:], e) for yv in Y.values)

    def normalize(self, Q):
        total = sum(Q.values())
        for key in Q:
            Q[key] /= total
        return Q

    def extend(self, e, Y, yv):
        e2 = e.copy()
        e2[Y] = yv
        return e2

    def probability(self, Y, e):
        if not Y.parents:
            return Y.probability
        else:
            return Y.probability[e[Y.name]][e[Y.parents[0].name]]

    # def factores(self):

    #     factores = []

    #     #crear un diccionario que contenga nombre del nodo, probabilidad y probabilidad condicional
    #     for node in self.nodes.values():

    #         diccionario = {}

    #         if(node.probability != None):
    #             diccioanrio = ({"name": node, "probabilityTrue": node.probability, "probabilityFalse": 1- node.probability})
    #         else:
    #             diccioanrio = ({"name": node})
                 
    #         if node.parents:

    #             # if(node.probability != None):
    #             #     diccioanrio = ({"name": node, "probabilityTrue": node.probability, "probabilityFalse": 1- node.probability})
    #             # else:
    #             #     diccioanrio = ({"name": node})

    #             # for parent in node.parents:
    #             #     diccioanrio[parent.name] = node.probability
    #             #     diccioanrio[parent.name] = 1- node.probability 


    #         # factores.append(diccioanrio)      

    
# Ejemplo de uso
bn = BayesianNetwork()

#Crear red bayesiana con ejemplo de una alarma puede sonar por dos razones: un terremoto o un robo. Si suena la alarma,Juan o Maria llaman

earthquake = Node("Earthquake", [True, False], [],0.001)
burglary = Node("Burglary", [True, False],[], 0.002)
alarm = Node("Alarm", [True, False], [earthquake, burglary])
callJuan = Node("CallJuan", [True, False], [alarm], 0.9)
callMaria = Node("CallMaria", [True, False], [alarm], 0.7)

bn.add_node(earthquake)
bn.add_node(burglary)
bn.add_node(alarm)
bn.add_node(callJuan)
bn.add_node(callMaria)

#estabalcer probabilidades para cada nodo y probabilidad condicional
bn.nodes


# Verificar que este complemtante descrita
print("Is complete:", bn.is_complete())

# Str
dot_string =bn.to_dot_string()
print(dot_string)
source = Source(dot_string)
source.render("bn", view=True)

#factores: tabla de probabilidades y probabilidad condicional para cada nodo
# print(bn.factores())

#enumeration algorithm
probability = bn.enumeration_ask(callMaria, {earthquake: True})
print(probability)

