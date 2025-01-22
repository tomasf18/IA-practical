import math

'''
ATENÇÃO: NO EXAME ESCRITO SAI SEMPRE UMA PERGUNTA DESTAS PARA ESCREVER A PAPEL E LÁPIS
'''

#Exercicio 4.1
impar = lambda x: x%2 != 0

#Exercicio 4.2
positivo = lambda x: x>0

#Exercicio 4.3
comparar_modulo = lambda x, y: abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x, y: (math.hypot(x, y), math.asin(y/math.hypot(x, y)))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z: h(f(x, y), g(y, z))

#Exercicio 4.6
def quantificador_universal(lista, f):
	if lista == []:
		return True

	if f(lista[0]):
		return quantificador_universal(lista[1:], f)
	else:
		return False


#Exercicio 4.7
def quantificador_existencial(lista, f):
	if lista == []:
		return False

	if f(lista[0]):
		return True
	else:
		return quantificador_existencial(lista[1:], f)


#Exercicio 4.8
def subconjunto(lista1, lista2):
	if lista1 == []:
		return True

	if lista1[0] in lista2:
		return subconjunto(lista1[1:], lista2)
	else:
		return False

#Exercicio 4.9
def menor_ordem(lista, f):

	if len(lista) == 1:
		return lista[0]

	menor = menor_ordem(lista[1:], f)
	menor_temp = lista[0] if f(lista[0], lista[1]) else lista[1]
  
	if f(menor_temp, menor):
		menor = menor_temp
  
	return menor
	

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):

	if len(lista) == 1:
		return lista[0], []

	menor, resto = menor_e_resto_ordem(lista[1:], f)
	menor_temp = lista[0] 
  
	if f(menor_temp, menor):
		resto += [menor]
		menor = menor_temp
	else:
		resto += [menor_temp]

 
	return menor, resto


#Exercicio 4.11
def dois_menores_ordem(lista, f):

    if len(lista) == 2:
        return (lista[0], lista[1], []) if f(lista[0], lista[1]) else (lista[1], lista[0], [])

    men1, men2, resto = dois_menores_ordem(lista[1:], f)
    menor_temp = lista[0]

    if f(menor_temp, men1):
        resto = [men2] + resto
        men1, men2 = menor_temp, men1 
    elif f(menor_temp, men2):
        resto = [men2,] + resto
        men2 = menor_temp
    else:
        resto = [menor_temp] + resto

    return men1, men2, resto



# def ordenar_seleccao(lista, ordem):

# 	if len(lista) == 1:
# 		return [lista[0]]

# 	ret = ordenar_seleccao(lista[1:], ordem)
	
# 	if ordem(lista[0], ret[0]):
# 		ret = [lista[0]] + ret
# 	else:
# 		ret = ret[0] + ordenar_seleccao(ret[1:], ordem)
  
# 	return ret

#Exercicio 5.2 #-> Muito bom
def ordenar_seleccao(lista, ordem):
    if lista == []:
        return []
    
    menor, resto = menor_e_resto_ordem(lista, ordem)
    
    return [menor] + ordenar_seleccao(resto, ordem)