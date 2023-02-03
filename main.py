from pomegranate import BayesianNetwork, DiscreteDistribution, Node

# Crea distribuciones de probabilidad para cada nodo
A_distribution = DiscreteDistribution({'A1': 0.5, 'A2': 0.5})
B_distribution = DiscreteDistribution({'B1': 0.7, 'B2': 0.3})
C_distribution = DiscreteDistribution({'C1': 0.4, 'C2': 0.6})

# Crea una red bayesiana básica
model = BayesianNetwork()
A = Node(A_distribution, name="A")
B = Node(B_distribution, name="B")
C = Node(C_distribution, name="C")
model.add_node(A)
model.add_node(B)
model.add_node(C)
model.add_edge(A, B)
model.add_edge(B, C)
model.bake()

# Verifica si la red bayesiana está completamente descrita
if model.structure:
    print("La red bayesiana está completamente descrita.")
else:
    print("La red bayesiana no está completamente descrita.")
