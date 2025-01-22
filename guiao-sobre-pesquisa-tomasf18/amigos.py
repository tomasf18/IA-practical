from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def constraint(amigo1, objetos1, amigo2, objetos2):
    # amigo = "Andre", "Bernardo" ou "Claudio"; 
    # bicicleta = "Andre", "Bernardo" ou "Claudio"; 
    # chapeu = "Andre", "Bernardo" ou "Claudio"
    bicicleta1, chapeu1 = objetos1      
    bicicleta2, chapeu2 = objetos2
    
    if bicicleta1 == chapeu1:
        return False
    
    if amigo1 == bicicleta1 or amigo1 == chapeu1:
        return False
    
    if amigo2 == bicicleta2 or amigo2 == chapeu2:
        return False
    
    if bicicleta1 == bicicleta2:
        return False
    
    if chapeu1 == chapeu2:
        return False
    
    if (chapeu1 == "Claudio" and bicicleta1 != "Bernardo") or (chapeu1 != "Claudio" and bicicleta1 == "Bernardo"):
        return False
    
    if (chapeu2 == "Claudio" and bicicleta2 != "Bernardo") or (chapeu2 != "Claudio" and bicicleta2 == "Bernardo"):
        return False
    
    return True

def make_constraint_graph(amigos):
    constraints = {}
    for amigo1 in amigos:
        for amigo2 in amigos:
            if amigo1 != amigo2:
                constraints[amigo1, amigo2] = constraint
        
    return constraints

def make_domain(amigos):
    domain = {}
    for amigo in amigos:
        domain[amigo] = [(amigo1, amigo2) for amigo1 in amigos for amigo2 in amigos]
        
    return domain

cs = ConstraintSearch(make_domain(amigos), make_constraint_graph(amigos))

print(cs.search())
