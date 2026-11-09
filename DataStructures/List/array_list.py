def new_list():
    """
    Crea una lista (array_list) vacía.
    """
    my_list = {
        'elements': [],
        'size': 0,
    }
    return my_list
 
 
def is_empty(my_list):
    """
    Retorna True si la lista está vacía, False en caso contrario.
    """
    return my_list['size'] == 0
 
 
def size(my_list):
    """
    Retorna el tamaño de la lista.
    """
    return my_list['size']
 
 
def add_first(my_list, element):
    """
    Agrega un elemento al inicio de la lista.
    """
    my_list['elements'].insert(0, element)
    my_list['size'] += 1
    return my_list
 
 
def add_last(my_list, element):
    """
    Agrega un elemento al final de la lista.
    """
    my_list['elements'].append(element)
    my_list['size'] += 1
    return my_list
 
 
def first_element(my_list):
    """
    Retorna el primer elemento de la lista (sin eliminarlo).
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][0]
 
 
def last_element(my_list):
    """
    Retorna el último elemento de la lista (sin eliminarlo).
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][my_list['size'] - 1]
 
 
def get_element(my_list, pos):
    """
    Retorna el elemento en la posición dada (sin eliminarlo).
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][pos]
 
 
def delete_element(my_list, pos):
    """
    Elimina el elemento en la posición dada.
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    my_list['elements'].pop(pos)
    my_list['size'] -= 1
    return my_list
 
 
def remove_first(my_list):
    """
    Elimina y retorna el primer elemento de la lista.
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    removed = my_list['elements'].pop(0)
    my_list['size'] -= 1
    return removed
 
 
def remove_last(my_list):
    """
    Elimina y retorna el último elemento de la lista.
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    removed = my_list['elements'].pop(my_list['size'] - 1)
    my_list['size'] -= 1
    return removed
 
 
def insert_element(my_list, element, pos):
    """
    Inserta un elemento en la posición dada.
    """
    my_list['elements'].insert(pos, element)
    my_list['size'] += 1
    return my_list
 
 
def default_function(element_1, element_2):
    """
    Función de comparación por defecto (a modo de ejemplo).
    """
    if element_1 > element_2:
        return 1
    elif element_1 < element_2:
        return -1
    return 0
 
 
def is_present(my_list, element, cmp_function):
    """
    Retorna la posición del elemento si está presente en la lista
    (usando cmp_function para comparar), o -1 si no está presente.
    """
    for pos in range(my_list['size']):
        info = my_list['elements'][pos]
        if cmp_function(element, info) == 0:
            return pos
    return -1
 
 
def change_info(my_list, pos, new_info):
    """
    Cambia la información del elemento en la posición dada.
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    my_list['elements'][pos] = new_info
    return my_list
 
 
def exchange(my_list, pos_1, pos_2):
    """
    Intercambia la información de los elementos en las posiciones dadas.
    """
    my_list['elements'][pos_1], my_list['elements'][pos_2] = \
        my_list['elements'][pos_2], my_list['elements'][pos_1]
    return my_list
 
 
def sub_list(my_list, pos_i, num_elements):
    """
    Retorna una sublista que inicia en pos_i y contiene num_elements elementos.
    """
    if pos_i < 0 or pos_i >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    sublist = {
        'elements': my_list['elements'][pos_i: pos_i + num_elements],
        'size': len(my_list['elements'][pos_i: pos_i + num_elements]),
    }
    return sublist
 
 
def to_py_list(my_list):
    """
    Retorna los elementos de la lista en una lista nativa de Python.
    """
    return my_list['elements']

#ordenamientos iterativos

def default_sort_criteria(element_1, element_2):
    """
    Criterio de ordenamiento por defecto (a modo de ejemplo).
    """
    return element_1 < element_2

def insertion_sort(my_list, sort_criteria):
    """
    Ordena la lista usando el algortimo de ordenamiento inserccion
    """
    for i in range(1, size(my_list)):
        j = i
        while j >= 1 and sort_criteria(j,j-1):
            exchange(my_list,j,j-1)
            j-=1
    return my_list

def insertion_sort_h(my_list, sort_criteria, h):
    """
    Ordena la lista usando el algortimo de ordenamiento inserccion con elemento h
    """
    for i in range(h, size(my_list)):
        j = i
        while j >= h and sort_criteria(j,j-h):
            exchange(my_list,j,j-h)
            j -= h
    return my_list

def shell_sort(my_list, sort_criteria):
    """
    Ordena la lista usando el algortimo de ordenamiento shell con elemento h
    """
    h = size(my_list) // 2
    while h >= 1:
        insertion_sort_h(my_list, sort_criteria, h)
        h = h // 2
    return my_list

def selection_sort(my_list, sort_criteria):
   """
   Ordena la lista usando el algoritmo de ordenamiento por selección.
   """
   for i in range(my_list['size']):
       min_index = i
       for j in range(i + 1, my_list['size']):
           if sort_criteria(my_list['elements'][j], my_list['elements'][min_index]):
               min_index = j
       exchange(my_list, i, min_index)
   return my_list

#ordenamientos recursivos

def merge_sort(my_list, sort_criteria):
    """
    Ordena la lista usando el algoritmo de ordenamiento de merge sort.
    """
    if my_list['size'] <= 1:
        return my_list

    mid = my_list['size'] // 2
    left_half = sub_list(my_list, 0, mid)
    right_half = sub_list(my_list, mid, my_list['size'])

    left_sorted = merge_sort(left_half, sort_criteria)
    right_sorted = merge_sort(right_half, sort_criteria)

    i = j = k = 0
    while i < left_sorted['size'] and j < right_sorted['size']:
        if sort_criteria(left_sorted['elements'][i], right_sorted['elements'][j]):
            my_list['elements'][k] = left_sorted['elements'][i]
            i += 1
        else:
            my_list['elements'][k] = right_sorted['elements'][j]
            j += 1
        k += 1

    while i < left_sorted['size']:
        my_list['elements'][k] = left_sorted['elements'][i]
        i += 1
        k += 1

    while j < right_sorted['size']:
        my_list['elements'][k] = right_sorted['elements'][j]
        j += 1
        k += 1

    return my_list

def partition(my_list, low, high, sort_criteria):
    """
    Particiona el sublista my_list[low..high] usando el último elemento (high)
    como pivote 
    Todo lo que sea "menor" (según sort_criteria) que el pivote queda a su
    izquierda, y lo demás a su derecha. Retorna la posición final del pivote.
    """
    pivot = my_list['elements'][high]
    i = low - 1  
 
    for j in range(low, high):
        if sort_criteria(my_list['elements'][j], pivot):
            i += 1
            exchange(my_list, i, j)
 
    exchange(my_list, i + 1, high)  # el pivote queda en su posición final
    return i + 1
 
 
def quick_sort_rec(my_list, low, high, sort_criteria):
    """
    Ordena recursivamente el sublista my_list[low..high].
    """
    if low < high:
        pivot_index = partition(my_list, low, high, sort_criteria)
        quick_sort_rec(my_list, low, pivot_index - 1, sort_criteria)
        quick_sort_rec(my_list, pivot_index + 1, high, sort_criteria)
    return my_list
 
 
def quick_sort(my_list, sort_criteria):
    """
    Ordena la lista usando el algoritmo de ordenamiento quick sort.
    """
    quick_sort_rec(my_list, 0, my_list['size'] - 1, sort_criteria)
    return my_list