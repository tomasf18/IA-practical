# Pesquisa para resolucao de problemas de atribuicao
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2019
#


class ConstraintSearch:

    # variables_domains é um dicionário com o domínio de cada variável; -> O domínio de cada variável é uma lista de valores possíveis
    # constaints e' um dicionário com a restrição aplicável a cada aresta;
    def __init__(self,variables_domains,constraints: dict):
        
        # 1) Inicialização: o nó inicial da árvore de pesquisa é composto por todas as variáveis e todos os valores possíveis para cada uma delas
        self.variables_domains = variables_domains
        self.constraints = constraints
        self.calls = 0

    # variables_domains é um dicionário com os domínios **actuais** de cada variável
    # (ver acetato "Pesquisa com propagacao de restricoes em problemas de atribuicao - algoritmo")
    # def search_without_propagation(self, variables_domains: dict = None):
    #     self.calls += 1 
        
    #     if variables_domains == None: 
    #         variables_domains = self.variables_domains

    #     # 2) Se alguma variavel tiver lista de valores vazia, falha
    #     if any([lista_valores_variavel == [] for lista_valores_variavel in variables_domains.values()]):
    #         return None

    #     # 3) Se todas as variáveis têm exactamente um valor possível, tem-se uma solução -> retornar com sucesso
    #     if all([len(lista_valores_variavel) == 1 for lista_valores_variavel in list(variables_domains.values())]):
    #         # se valores violam restricoes, falha
    #         # ( verificacao desnecessaria se for feita a propagacao
    #         #   de restricoes )
    #         for (var1, var2) in self.constraints:
    #             constraint = self.constraints[var1,var2]
    #             if not constraint(var1,variables_domains[var1][0],var2,variables_domains[var2][0]):
    #                 return None 
    #         return { v:lista_valores_variavel[0] for (v,lista_valores_variavel) in variables_domains.items() } # Retorna um dicionarion do tipo {variável:valor_único}
       
    #     # continuação da pesquisa
    #     # 4) Expansão 
    #     # ( falta fazer a propagacao de restricoes )
        
    #     # 1. Escolher arbitrariamente uma variável Vk 
    #     for var in variables_domains.keys():
    #         if len(variables_domains[var]) > 1:
                
    #             # e, de entre os valores possíveis, um dado valor Xkl - 
    #             for val in variables_domains[var]:
    #                 new_variables_domains = dict(variables_domains) # copiar o dicionário
    #                 # descartar os restantes valores possíveis dessa variável
    #                 new_variables_domains[var] = [val]
    #                 # fazer nova pesquisa com a nova atribuição
    #                 solution = self.search_without_propagation(new_variables_domains)
                    
    #                 # alguma pesquisa há de encontrar uma solução, se existir
    #                 if solution != None:
    #                     return solution
                    
    #     return None
    
# =============================== #
    
    def search(self, variables_domains: dict = None):
        self.calls += 1 
        
        if variables_domains == None: 
            variables_domains = self.variables_domains  # Nó inicial: composto por todas as variáveis e todos os valores possíveis para cada uma delas

        if any([lista_valores_variavel == [] for lista_valores_variavel in variables_domains.values()]):
            return None

        if all([len(lista_valores_variavel) == 1 for lista_valores_variavel in list(variables_domains.values())]):
            return { v:lista_valores_variavel[0] for (v,lista_valores_variavel) in variables_domains.items() } # Retorna um dicionarion do tipo {variável:valor_único}
       
        solution = self.expand(variables_domains)
                
        return solution
    
    
    def expand(self, variables_domains):
        for var in variables_domains.keys():
            if len(variables_domains[var]) <= 1: continue       # Se já so existe 1 valor possível para 'var', então tem de ser esse até ao final, senão não existe solução para 'var'
                
            for val in variables_domains[var]:
                new_variables_domains = dict(variables_domains) # Cópia do atual, para alterar so os values da key "var"
                new_variables_domains[var] = [val]
                
                new_variables_domains_with_propagation = self.propagate(new_variables_domains, var, val)
                
                if new_variables_domains_with_propagation:
                    solution = self.search(new_variables_domains_with_propagation)
                    if solution != None:
                        return solution
        return None
                    


    def propagate(self, new_variables_domains: dict, variable, value):
        for var, var_domain in new_variables_domains.items():
            if var == variable:                 # Não propaga para si própria, porque é ela que está a assumir um valor, as outras é que têm de se adaptar
                continue
            
            for pair_of_vars, constrain in self.constraints.items():
                if (not pair_of_vars in [(var, variable), (variable, var)]):        # Só me interessam relações com a variable passada no argumento
                    continue
                
                new_variables_domains[var] = [val for val in var_domain if constrain(variable, value, var, val)]
                
                if new_variables_domains[var] == []:    # Não há solução para variable
                    return None
                
        return new_variables_domains
                
