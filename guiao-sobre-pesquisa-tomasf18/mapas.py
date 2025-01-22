from constraintsearch import *

regions_a = ['A', 'B', 'C', 'D', 'E']
regions_b = ['A', 'B', 'C', 'D', 'E', 'F']
regions_c = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
colors = ['red', 'blue', 'green', 'yellow', 'white']

# Construir um grafo de restrições:
# - Em cada nó do grafo está uma variável
# - Um arco dirigido liga um nó i a um nó j se o valor da variável de j impõe
# restrições ao valor da variável de i.
# - Um arco (i,j) é consistente se, para cada valor da variável i, existe um valor
# da variável j que não viola as restrições.

mapa_a = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C'],
    'C': ['B', 'D', 'E'],
    'D': ['A', 'C', 'E'],
}

mapa_b = {
    'A': ['B', 'D', 'E'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'E', 'F'],
    'D': ['A', 'E', 'F'],
    'E': ['A', 'B', 'C', 'D', 'F'],
    'F': ['C', 'D', 'E'],
}

mapa_c = {
    'A': ['B', 'D', 'E', 'F'],
    'B': ['A', 'C', 'F'],
    'C': ['B', 'D', 'F', 'G'],
    'D': ['A', 'C', 'E', 'G'],
    'E': ['A', 'D', 'F', 'G'],
    'F': ['A', 'B', 'C', 'E', 'G'],
    'G': ['C', 'D', 'E', 'F'],
}

def constraint(regiao1, cor1, regiao2, cor2):
    return cor1 != cor2

def make_constraint_graph(mapa):
    constraints = {}
    for regiao1 in mapa:
        for regiao2 in mapa[regiao1]:
            constraints[regiao1, regiao2] = constraint
    return constraints

# - O nó inicial da árvore de pesquisa é composto por todas as
# variáveis e todos os valores possíveis para cada uma delas

def make_domain(regions, colors):
    return {r: colors for r in regions} # -> O domínio de cada variável é uma lista de valores possíveis (neste caso, cores)

cs_a = ConstraintSearch(make_domain(regions_a, colors), make_constraint_graph(mapa_a))

print("Mapa A:")
print(cs_a.search())
print()

cs_b = ConstraintSearch(make_domain(regions_b, colors), make_constraint_graph(mapa_b))

print("Mapa B:")
print(cs_b.search())
print()

cs_c = ConstraintSearch(make_domain(regions_c, colors), make_constraint_graph(mapa_c))

print("Mapa C:")
print(cs_c.search())
print()

