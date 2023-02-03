from pomegranate import BayesianNetwork, DiscreteDistribution, Node

def is_completely_described(bayesian_network):
    # Verifica si todos los nodos tienen una distribución de probabilidad asociada
    for node in bayesian_network.model:
        if not node.distribution:
            return False

    # Verifica si todas las relaciones entre nodos están definidas
    for node in bayesian_network.model:
        for parent in node.parents:
            if node not in parent.children:
                return False

    # Verifica si todas las probabilidades condicionales están definidas
    for node in bayesian_network.model:
        if isinstance(node.distribution, DiscreteDistribution):
            for parent in node.parents:
                if (node.distribution.parameters[parent.name] is None):
                    return False

    return True

# Crear distribuciones de probabilidad para los nodos
d1 = DiscreteDistribution({'A': 0.5, 'B': 0.5})
d2 = DiscreteDistribution({'A': 0.2, 'B': 0.8})
d3 = DiscreteDistribution({'A|B': 0.5, 'A|not B': 0.7, 'not A|B': 0.3, 'not A|not B': 0.1})

# Crear nodos
node1 = Node(d1, name="node1")
node2 = Node(d2, name="node2")
node3 = Node(d3, name="node3")

# Definir relaciones entre nodos
bayesian_network = BayesianNetwork()
bayesian_network.add_node(node1)
bayesian_network.add_node(node2)
bayesian_network.add_node(node3)

bayesian_network.add_edge(node1, node2)
bayesian_network.add_edge(node2, node3)

# Verificar si está completamente descrita
if is_completely_described(bayesian_network):
    print("La red bayesiana está completamente descrita.")
else:
    print("La red bayesiana no está completamente descrita.")
