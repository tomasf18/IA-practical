#Exercicio 1.1
def comprimento(lista):
    if lista == []:
        return 0
    return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	return lista[0] + soma(lista[1:])
 
#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False

	return lista[0] == elem or existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
	if l1 == []:
		return l2
	l2[0:0] = [l1[-1]]
	return concat(l1[:-1], l2)
    
#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return []
	return [lista[-1]] + inverte(lista[:-1])

#Exercicio 1.6
def capicua(lista):
	if lista == [] or len(lista) == 1:
		return True
	return lista[0] == lista[-1] and capicua(lista[1:-1])
		
    
#Exercicio 1.7
def concat_listas(lista):
    if lista == []:
        return []
    return concat(lista[0], concat_listas(lista[1:]))
    
#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []
	if lista[0] == original:    
		lista[0] = novo
	return [lista[0]] + substitui(lista[1:], original, novo)

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	if lista1 == []:
		return lista2
	
	if lista2 == []:
		return lista1

	# If this happens, element idx 0 off list2 appears beffore all list1
	if lista2[0] <= lista1[0]:
		return [lista2[0]] + fusao_ordenada(lista1, lista2[1:])

	# else, the opposite happens
	return [lista1[0]] + fusao_ordenada(lista1[1:], lista2) 
  

#Exercicio 1.10
def lista_subconjuntos(lista):
	if lista == []:
		return [[]]

	sub_result = lista_subconjuntos(lista[1:])

	def combinar(elem, lista):
		if lista == []:
			return []
		return [[elem] + lista[0]] + combinar(elem, lista[1:])

	return sub_result + combinar(lista[0], sub_result)
		
		
	

#Exercicio 2.1
def separar(lista):
    if lista == []:
        return ([], [])

    a = lista[0][0]
    b = lista[0][1]
    aabb = separar(lista[1:])
    
    return ([a] + aabb[0], [b] + aabb[1])
    
 
    
#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []:
		return ([], 0)

	ret = remove_e_conta(lista[1:], elem)
	if lista[0] == elem:
		return (ret[0], ret[1] + 1)
	else:
		return ([lista[0]] + ret[0], ret[1])


#Exercício 2.3
def par_elem_cont(lista):
	if lista == []:
		return []

	lista_sem_elem, contagem = remove_e_conta(lista, lista[0])

	return [(lista[0], contagem)] + par_elem_cont(lista_sem_elem)
	
 

#Exercicio 3.1
def cabeca(lista):
	if lista == []:
		return None

	return lista[0]

#Exercicio 3.2
def cauda(lista):
	if lista == []:
		return None

	return lista[1:]

#Exercicio 3.3
def juntar(l1, l2): # -> É uma função de zip!!
	if len(l1) != len(l2):
		return None
	if l1 == [] or l2 == []:
		return []

	return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])
 

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None

	men = menor(lista[1:])
	menor_temp = lista[0]
 
	if men == None or menor_temp <= men:
		return menor_temp
	return men
	

#Exercicio 3.5
def menor_lista(lista):
    if lista == []:
        return None, []
    
    men, resto = menor_lista(lista[1:])
    menor_temp = lista[0]

    if men == None or menor_temp <= men:
        return menor_temp, [men] + resto if men != None else resto
    return men, [menor_temp] + resto

# #Exercicio 3.5 v2
# def menor_lista(lista):
#     if lista == []:
#         return None, []
    
#     men = menor(lista)
    
#     return (men, remove_e_conta(lista, men)[0])
    
    
#Exercicio 3.6
def max_min(lista):
	if lista == []:
		return None
	
	if len(lista) == 1:
		return lista[0], lista[0]

	max, min = max_min(lista[1:])
	menor_temp = lista[0]
	maior_temp = lista[0]
 
	if min == None or menor_temp <= min:
		min = menor_temp
	
	if max == None or maior_temp >= max:
		max = maior_temp
	  
	return max, min


#Exercicio 3.7
def dois_menores(lista):
    if len(lista) == 0:
        return None, None, []

    if len(lista) == 1:
        return lista[0], None, []

    men1, men2, resto = dois_menores(lista[1:])
    menor_temp = lista[0]

    if men1 is None or menor_temp < men1:
        men1, men2 = menor_temp, men1 
    elif men2 is None or menor_temp < men2:
        men2 = menor_temp

    resto = remove_e_conta(lista, men1)[0]
    resto = remove_e_conta(resto, men2)[0]

    return men1, men2, resto


#Exercício 3.8
def media_mediana(lista):
    if lista == []:
        return None, None
    
    tamanho_lista = len(lista)
    
    soma_elem = soma(lista)
    media = soma_elem/tamanho_lista
    
    if tamanho_lista % 2 == 0:
        mediana = (lista[(tamanho_lista // 2) - 1] + lista[(tamanho_lista // 2)]) / 2
    else:
        mediana = lista[tamanho_lista // 2]
        
    return media, mediana
        

	
