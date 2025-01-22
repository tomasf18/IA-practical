

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#

# ======================================================================== #


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + str(self.entity2) + ")" # -> "professor(socrates,filosofia)" vem de: a = Association('socrates','professor','filosofia')
    def __repr__(self):
        return str(self)


# ========================= 3 Possíveis Relações ========================= #

class AssocOne(Relation):
    def __init__(self, e1, assoc, e2):
        Relation.__init__(self, e1, assoc, e2)
        
class AssocNum(Relation):
    def __init__(self, e1, assoc, num):
        Relation.__init__(self, e1, assoc, num)      

# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# ----

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)

#   Exemplo:
#   s = Subtype('homem','mamifero')

# ----
 
# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# ======================================================================== #

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# ======================================================================== #

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
        
    def __str__(self):
        return str(self.declarations)
    
    def insert(self,decl):
        self.declarations.append(decl)
        
    def query_local(self,user=None,e1=None,rel=None,e2=None,rel_type=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2)
                and (rel_type == None or isinstance(d.relation, rel_type)) ]
        return self.query_result
    
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
            
    # ------
    
    def list_associations(self):
        # return sorted(set([d.relation.name for d in self.declarations if not isinstance(d.relation, Member) and not isinstance(d.relation, Subtype)]))
        declarations = self.query_local(rel_type=Association)
        return { d.relation.name for d in declarations } # -> Set to avoid repetitions
    
    def list_objects(self):
        declarations = self.query_local(rel="member")
        return { d.relation.entity1 for d in declarations }
    
    def list_users(self):
        return { d.user for d in self.declarations }

    def list_types(self):
        supertypes = [d.relation.entity2 for d in self.query_local(rel="subtype")]
        subtypes = [d.relation.entity1 for d in self.query_local(rel="subtype")] + supertypes
        types = [d.relation.entity2 for d in self.query_local(rel="member")] + subtypes
        return {type for type in types}

    def list_local_associations(self, e):
        declarations = self.query_local(e1=e, rel_type=Association) + self.query_local(e2=e, rel_type=Association)
        return { d.relation.name for d in declarations }
    
    def list_relations_by_user(self, user):
        return { d.relation.name for d in self.query_local(user=user) }
    
    def associations_by_user(self, user):
        return len({ d.relation.name for d in self.query_local(user=user, rel_type=Association) })
        
    def list_local_associations_by_entity(self, e):
        declarations = [(d.relation.name, d.user) for d in self.query_local(e1=e, rel_type=Association)] + \
                        [(d.relation.name, d.user) for d in self.query_local(e2=e, rel_type=Association)]
        return set(declarations)
    
    def predecessor(self, a, b):
        # Encontrar lista de predecessores de e2 e ver se e1 está lá
        # A lista tem de contemplar o predecessor, o predecessor do predecessor, etc
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=b, rel_type=(Member, Subtype))]
        if a in local_predecessor:
            return True
    
        return any(self.predecessor(a, l) for l in local_predecessor)
    
    # === #
#   Explanation
#   Let's analyze the example where:

#   A is a Member of B
#   B is a Member of D
#   C is a Subtype of E
#   D is a Member of F
#   E is a Subtype of F
#   We want to find the path from A to F using the predecessor_path function.

#   Execution Steps
#   Initial Call: predecessor_path('A', 'F')

#   a is not equal to b, so it queries local predecessors of F and finds D and E.
#   It first tries predecessor_path('A', 'D').
#   Recursive Call: predecessor_path('A', 'D')

#   a is not equal to b, so it queries local predecessors of D and finds B.
#   It calls predecessor_path('A', 'B').
#   Recursive Call: predecessor_path('A', 'B')

#   a is not equal to b, so it queries local predecessors of B and finds A.
#   It calls predecessor_path('A', 'A').
#   Base Case: predecessor_path('A', 'A')

#   a is equal to b, so it returns ['A'].
#   The recursive calls then return:

#   predecessor_path('A', 'B') returns ['A', 'B'].
#   predecessor_path('A', 'D') returns ['A', 'B', 'D'].
#   predecessor_path('A', 'F') returns ['A', 'B', 'D', 'F'].
#   Now, let's consider the second local predecessor E for F:

#   Initial Call: predecessor_path('A', 'F')

#   After finding the path through D, it tries predecessor_path('A', 'E').
#   Recursive Call: predecessor_path('A', 'E')

#   a is not equal to b, so it queries local predecessors of E and finds C.
#   It calls predecessor_path('A', 'C').
#   Recursive Call: predecessor_path('A', 'C')

#   a is not equal to b, so it queries local predecessors of C and finds no predecessors related to A.
#   Since no path is found, it returns None.
#   The recursive calls then return:

#   predecessor_path('A', 'C') returns None.
#   predecessor_path('A', 'E') returns None.
#   Thus, the function finds only one possible path from A to F:

#   ['A', 'B', 'D', 'F']
#   If we call predecessor_path('D', 'A'), the function will work as follows:

#   Initial Call: predecessor_path('D', 'A')
#   a is not equal to b, so it queries local predecessors of A and finds no predecessors related to D.
#   Since no path is found, it returns None.
#   Therefore, there is no path from D to A.
    
    def predecessor_path(self, a, b):
        if a == b:
            return [a]
        
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=b, rel_type=(Member, Subtype))]
        for l in local_predecessor:
            path = self.predecessor_path(a, l)
            if path:
                return path + [b]
        
        return None
    
    # === #
    
    def query(self, e, assoc=None):

        local_declarations = self.query_local(e1=e, rel=assoc, rel_type=Association)                            # Todas as declarações locais do tipo Association
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=e, rel_type=(Member, Subtype))]    # Dá-me diretamente os meus predecessores locais (a quem esou ligado diretamente, mas ainda nao da recursicamente, pais dos meus pais, etc)
        
        for predecessor in local_predecessor:                                                                   # Para cada predecessor, vou fazer o query até ao ultimo predecessor
            local_declarations.extend(self.query(predecessor, assoc))                                           # Obtenho todas as declarações locais dos meus predecessores, dos predecessores dos meus predecessores, etc, e dou append às minhas
        # Neste exemplo só estou a obter relações herdadas do tipo Associations
        return local_declarations

    def query2(self, e, assoc=None):
        local_declarations = self.query_local(e1=e, rel=assoc)                                                  # Dá-me todas as relações locais, ao contrário do query, que restringe a apenas Association
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=e, rel_type=(Member, Subtype))]    # Subo a arvore de forma diferente a linha acima
        # Neste exemplo já nao estou a fazer apenas as associacoes, estou a fazer tudo
        
        # Depois, uso query para que todas as herdadas sejam só Association
        for predecessor in local_predecessor:
            local_declarations.extend(self.query(predecessor, assoc))
            
        return local_declarations
    
    def query_cancel(self, e, assoc):
        local_declarations = self.query_local(e1=e, rel=assoc, rel_type=Association)                            # Dá-me todas as relações locais
        local_predecessor = [d.relation.entity2 for d in self.query_local(e1=e, rel_type=(Member, Subtype))]    # Subo a arvore de forma diferente a linha acima
        
        local_assocs = [d.relation.name for d in local_declarations]
        
        for predecessor in local_predecessor:
            predecessor_declarations = self.query_cancel(predecessor, assoc)
            local_declarations.extend(d for d in predecessor_declarations if d.relation.name not in local_assocs) # Filtrar as associações que ainda não tenho
            
        return local_declarations
    
    def query_down(self, type, assoc, first = True):     # Ele só quer as dos descendentes, não quer o próprio (não quero ter o Mamifero, quero filtrar o local do proprio)
        # Esta flag só é executada a primeira vez, depois passamos como false 
        local_declarations = [] if first else self.query_local(e1=type, rel=assoc) # De cima para baixo, em vez de ir pela entidade 2, vou pela entidade 1 (inverti a ordem)
        local_descendents = [d.relation.entity1 for d in self.query_local(e2=type, rel_type=(Member, Subtype))]
        
        for descendent in local_descendents:
            local_declarations.extend([d for d in self.query_down(descendent, assoc, False)]) # Não preciso de filtrar nada
            
        return local_declarations
    
    def query_induce(self, type, assoc):
        descendents_declarations = self.query_down(type, assoc)
        
        # Counter retorna uma lista de tuplos, o primeiro elemento é o mais comum
        # print(Counter([d.relation.entity2 for d in descendents_declarations]))  # Counter({1.75: 2, 1.2: 1, 1.85: 1})
        # print(Counter([d.relation.entity2 for d in descendents_declarations]).most_common(1))   # [(1.75, 2)]
        
        most_common = Counter([d.relation.entity2 for d in descendents_declarations]).most_common(1)
        
        if len(most_common):
            return most_common[0][0]
        
        return None
    
    
    def query_local_assoc(self, e, assoc):        
        local_declarations_associations = self.query_local(e1=e, rel=assoc)
        test_decl = local_declarations_associations[0]
        
        if isinstance(test_decl.relation, Association):
            n = list(Counter([d.relation.entity2 for d in local_declarations_associations]).items())
            tuples = []
            total = sum([val[1] for val in n])
            freq = 0
            for tup in n:
                if freq >= 0.75: break
                tuples.append((tup[0], tup[1]/total))
                freq += tup[1]/total
                
            return tuples
        
        elif isinstance(test_decl.relation, AssocOne):
            n = list(Counter([d.relation.entity2 for d in local_declarations_associations]).items())
            most_common = n[0]
            total = sum([val[1] for val in n])
            return (most_common[0], most_common[1]*100/total)
        
        elif isinstance(test_decl.relation, AssocNum):
            total = sum(d.relation.entity2 for d in local_declarations_associations)
            n = len(local_declarations_associations)
            return total/n
            
            
    def query_assoc_value(self, e, assoc):
        local_declarations_associations = self.query_local(e1=e, rel=assoc)
        diff_assoc_values = { d.relation.entity2 for d in local_declarations_associations }
        local_predecessors = [d.relation.entity2 for d in self.query_local(e1=e, rel_type=(Member, Subtype))]    
        
        if len(local_declarations_associations) == 1: return diff_assoc_values[0]
        
        # -----------------------
        
        diff_assoc_values = []
        
        total_local_decl = len(local_declarations_associations)
        local_assoc_values_counters = list(Counter([d.relation.entity2 for d in local_declarations_associations]).items()) # Counter({1.75: 2, 1.2: 1, 1.85: 1})
        percentages1 = {} # {V: %}
        
        for counter in local_assoc_values_counters:
            diff_assoc_values.append(counter[0])
            percentages1[counter[0]] = counter[1]*100/total_local_decl
        
        # print("percentages1: ", percentages1)

        # -----------------------
        
        inherited_decl = []
        
        for predecessor in local_predecessors: # Only inherited declarations, not local (I've dealt with the locals above)
            inherited_decl.extend(self.query(predecessor, assoc))
        
        # print(inherited_decl)
        
        total_inherited_decl = len(inherited_decl)
        inherited_assoc_values_counters = list(Counter([d.relation.entity2 for d in inherited_decl]).items())
        percentages2 = {}
        
        for counter in inherited_assoc_values_counters:
            diff_assoc_values.append(counter[0])
            percentages2[counter[0]] = counter[1]*100/total_inherited_decl
            
        # print("percentages2: ", percentages2)
            
        funct_values = {}
        
        for key in diff_assoc_values:
            funct_values[key] = (percentages1.get(key, 0) + percentages2.get(key, 0)) / 2  # ".get(key, 0)" in case key doesn't exist in one of the dicts (default = 0)
            
        # print(funct_values)
        
        return max(funct_values, key=funct_values.get)  # Return the key which corresponds to the max val (this is, the value which maximizes the function)
    
    # Eu acho que ao fazer com valores default já estou a tratar do 3º ponto
            
        
    # -----------------
    # Solução do sor:

    # O segundo ponto nao está nos testes de codigO
    def query_assoc_value_sor(self, E, A):
        local_decl = self.query_local(e1=E, e2=A)
        
        local_hist = Counter([d.relation.entity2 for d in local_decl]).most_common()
        
        if local_hist and local_hist[0][1] == len(local_decl):  # 1º ponto
            return local_hist[0][0]
        
        inher_decl = [h for h in self.query(E, A) if h not in local_decl]
        
        inher_hist = Counter([d.relation.entity2 for d in inher_decl]).most_common() # most common ordena pelo mais comum
        
        # 3º ponto
        if not local_decl:
            return inher_hist[0][0]     
        if not inher_decl:
            return local_hist[0][0]
        
        # Se nao tiver locais, devolve os herdados, se nao tiver herdados, devolve os locais
        
        # Neste ponto já passa os testes, mas como é que eu posso maxizar o v?
        
        
        # Se tiver:
        # Local 1m50 4vezes
        # Herdado - 0vezes
        
        # Local 1m80 2vezes
        # Herdado 1m80 3vezes
        
        # Para maxizar, tenho de pegar na quantidade de vezes que aparece, somar os dois, e depois ordená-los (fazer uma composição dos dois)
        # 2º Ponto
        f = {v: t for v, t in local_hist} # Chave como entidade e os valores são
        for v, t in inher_hist:
            f[v] += f.get(v, 0) + t
            
        return sorted(f.items(), key=lambda x: -x[1])[0] #sorted devolve uma lista de tuplos    
            
