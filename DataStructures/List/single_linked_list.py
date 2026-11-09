from heapq import merge


def new_list():
    """
    Crea una lista (single_linked_list) vacía.
    """
    my_list = {
        'first': None,
        'last': None,
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
    new_node = {
        'info': element,
        'next': my_list['first']
    }
    my_list['first'] = new_node
    if my_list['size'] == 0:
        my_list['last'] = new_node
    my_list['size'] += 1
    return my_list
 
 
def add_last(my_list, element):
    """
    Agrega un elemento al final de la lista.
    """
    new_node = {
        'info': element,
        'next': None
    }
    if my_list['size'] == 0:
        my_list['first'] = new_node
    else:
        my_list['last']['next'] = new_node
    my_list['last'] = new_node
    my_list['size'] += 1
    return my_list
 
 
def first_element(my_list):
    """
    Retorna el primer elemento de la lista (sin eliminarlo).
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['first']['info']
 
 
def last_element(my_list):
    """
    Retorna el último elemento de la lista (sin eliminarlo).
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['last']['info']
 
 
def get_element(my_list, pos):
    """
    Retorna el elemento en la posición dada (sin eliminarlo).
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    node = my_list['first']
    for _ in range(pos):
        node = node['next']
    return node['info']
 
 
def delete_element(my_list, pos):
    """
    Elimina el elemento en la posición dada.
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
 
    if pos == 0:
        my_list['first'] = my_list['first']['next']
        if my_list['size'] == 1:
            my_list['last'] = None
    else:
        prev_node = my_list['first']
        for _ in range(pos - 1):
            prev_node = prev_node['next']
        prev_node['next'] = prev_node['next']['next']
        if pos == my_list['size'] - 1:
            my_list['last'] = prev_node
 
    my_list['size'] -= 1
    return my_list
 
 
def remove_first(my_list):
    """
    Elimina y retorna el primer elemento de la lista.
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    removed_info = my_list['first']['info']
    my_list['first'] = my_list['first']['next']
    if my_list['size'] == 1:
        my_list['last'] = None
    my_list['size'] -= 1
    return removed_info
 
 
def remove_last(my_list):
    """
    Elimina y retorna el último elemento de la lista.
    """
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
 
    if my_list['size'] == 1:
        removed_info = my_list['first']['info']
        my_list['first'] = None
        my_list['last'] = None
        my_list['size'] -= 1
        return removed_info
 
    current_node = my_list['first']
    while current_node['next'] != my_list['last']:
        current_node = current_node['next']
 
    removed_info = my_list['last']['info']
    current_node['next'] = None
    my_list['last'] = current_node
    my_list['size'] -= 1
    return removed_info
 
 
def insert_element(my_list, element, pos):
    """
    Inserta un elemento en la posición dada (0 <= pos <= size(my_list)).
    """
    if pos < 0 or pos > my_list['size']:
        raise Exception('IndexError: list index out of range')
 
    if pos == 0:
        add_first(my_list, element)
    elif pos == my_list['size']:
        add_last(my_list, element)
    else:
        new_node = {
            'info': element,
            'next': None
        }
        prev_node = my_list['first']
        for _ in range(pos - 1):
            prev_node = prev_node['next']
        new_node['next'] = prev_node['next']
        prev_node['next'] = new_node
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
    temp = my_list['first']
    pos = 0
    while temp is not None:
        if cmp_function(element, temp['info']) == 0:
            return pos
        temp = temp['next']
        pos += 1
    return -1
 
 
def change_info(my_list, pos, new_info):
    """
    Cambia la información del elemento en la posición dada.
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    node = my_list['first']
    for _ in range(pos):
        node = node['next']
    node['info'] = new_info
    return my_list
 
 
def exchange(my_list, pos_1, pos_2):
    """
    Intercambia la información de los elementos en las posiciones dadas.
    """
    if (pos_1 < 0 or pos_1 >= my_list['size'] or
            pos_2 < 0 or pos_2 >= my_list['size']):
        raise Exception('IndexError: list index out of range')
 
    if pos_1 == pos_2:
        return my_list
 
    node_1 = my_list['first']
    for _ in range(pos_1):
        node_1 = node_1['next']
 
    node_2 = my_list['first']
    for _ in range(pos_2):
        node_2 = node_2['next']
 
    node_1['info'], node_2['info'] = node_2['info'], node_1['info']
    return my_list
 
 
def sub_list(my_list, pos, num_elements):
    """
    Retorna una sublista que contiene num_elements elementos a partir
    de la posición pos.
    """
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
 
    new_sub_list = new_list()
 
    current_node = my_list['first']
    for _ in range(pos):
        current_node = current_node['next']
 
    for _ in range(num_elements):
        if current_node is None:
            break
        add_last(new_sub_list, current_node['info'])
        current_node = current_node['next']
 
    return new_sub_list
 
 
def adjacents(my_list, element):
    """
    Retorna una lista de Python con el elemento siguiente al elemento
    dado (si existe). Si el elemento dado no existe, retorna None.
    """
    current_node = my_list['first']
    while current_node is not None:
        if current_node['info'] == element:
            if current_node['next'] is not None:
                return [current_node['next']['info']]
            return []
        current_node = current_node['next']
    return None
 
 
def to_py_list(my_list):
    """
    Retorna los elementos de la lista (en orden) en una lista de Python.
    """
    result = []
    current_node = my_list['first']
    while current_node is not None:
        result.append(current_node['info'])
        current_node = current_node['next']
    return result

def get_node_array(my_list):
    """
    Recorre la lista enlazada UNA vez (O(n)) y devuelve un arreglo con las
    referencias a cada nodo, en orden. Esto nos da acceso "tipo array" por
    posición para poder aplicar los algoritmos clásicos sin degradar su
    complejidad.
    """
    nodes = []
    current = my_list['first']
    while current is not None:
        nodes.append(current)
        current = current['next']
    return nodes

#Ordenamientos iterativos
 
def default_sort_criteria(element1,element2):
    """
    Función de comparación por defecto
    """
    return  element1<element2
 
def insertion_sort(my_list, sort_criteria):
    """
    Ordena la lista simplemente enlazada usando el algoritmo de
    ordenamiento por inserción.
    """
    nodes = get_node_array(my_list)
    for i in range(1, len(nodes)):
        j = i
        while j >= 1 and sort_criteria(nodes[j]['info'], nodes[j - 1]['info']):
            nodes[j]['info'], nodes[j - 1]['info'] = nodes[j - 1]['info'], nodes[j]['info']
            j -= 1
    return my_list
 
 
def insertion_sort_h(my_list, sort_criteria, h):
    """
    Ordena la lista simplemente enlazada usando el algoritmo de
    ordenamiento por inserción con salto h (usado por shell sort).
    """
    nodes = get_node_array(my_list)
    for i in range(h, len(nodes)):
        j = i
        while j >= h and sort_criteria(nodes[j]['info'], nodes[j - h]['info']):
            nodes[j]['info'], nodes[j - h]['info'] = nodes[j - h]['info'], nodes[j]['info']
            j -= h
    return my_list
 
 
def shell_sort(my_list, sort_criteria):
    """
    Ordena la lista simplemente enlazada usando el algoritmo shell sort.
    """
    n = my_list['size']
    h = n // 2
    while h >= 1:
        insertion_sort_h(my_list, sort_criteria, h)
        h = h // 2
    return my_list
 
 
def selection_sort(my_list, sort_criteria):
    """
    Ordena la lista simplemente enlazada usando el algoritmo de
    ordenamiento por selección.
    """
    nodes = get_node_array(my_list)
    for i in range(len(nodes)):
        min_index = i
        for j in range(i + 1, len(nodes)):
            if sort_criteria(nodes[j]['info'], nodes[min_index]['info']):
                min_index = j
        nodes[i]['info'], nodes[min_index]['info'] = nodes[min_index]['info'], nodes[i]['info']
    return my_list
 
#ordenamientos recursivos 
 
def merge_sort(my_list, sort_criteria):
    """
    Ordena la lista usando el algoritmo de ordenamiento merge sort.
    """
    if size(my_list) <= 1:
        return my_list
 
    mid = size(my_list) // 2
    left_half = sub_list(my_list, 0, mid)
    right_half = sub_list(my_list, mid, size(my_list) - mid)
 
    left_sorted = merge_sort(left_half, sort_criteria)
    right_sorted = merge_sort(right_half, sort_criteria)
 
    return merge(left_sorted, right_sorted, sort_criteria)
 
 
def partition(nodes, low, high, sort_criteria):
    """
    Particiona el arreglo de nodos nodes[low..high] usando el nodo en
    'high' como pivote (esquema de Lomuto), comparando por su campo 'info'.
    Retorna la posición final del pivote dentro del arreglo de nodos.
    """
    pivot = nodes[high]['info']
    i = low - 1  # frontera de los nodos ya acomodados a la izquierda
 
    for j in range(low, high):
        if sort_criteria(nodes[j]['info'], pivot):
            i += 1
            nodes[i]['info'], nodes[j]['info'] = nodes[j]['info'], nodes[i]['info']
 
    nodes[i + 1]['info'], nodes[high]['info'] = nodes[high]['info'], nodes[i + 1]['info']  # el pivote queda en su posición final
    return i + 1
 
 
def quick_sort_rec(nodes, low, high, sort_criteria):
    """
    Ordena recursivamente el arreglo de nodos entre las posiciones
    low y high (ambas inclusive).
    """
    if low < high:
        pivot_index = partition(nodes, low, high, sort_criteria)
        quick_sort_rec(nodes, low, pivot_index - 1, sort_criteria)
        quick_sort_rec(nodes, pivot_index + 1, high, sort_criteria)
 
 
def quick_sort(my_list, sort_criteria):
    """
    Ordena la lista simplemente enlazada usando el algoritmo de
    ordenamiento quick sort.
    """
    nodes = get_node_array(my_list)
    quick_sort_rec(nodes, 0, len(nodes) - 1, sort_criteria)
    return my_list