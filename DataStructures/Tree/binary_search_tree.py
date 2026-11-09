from DataStructures.Tree import bst_node as bs
from DataStructures.List import single_linked_list as sll
 
 
def new_map():
    """Crea una tabla de símbolos ordenada vacía basada en un BST."""
    my_bst = {"root": None}
    return my_bst
 
 
def default_compare(key, element):
    """
    Compara una llave con la llave de un nodo.
    Retorna 0 si son iguales, 1 si key es mayor, -1 si key es menor.
    """
    node_key = bs.get_key(element)
    if key == node_key:
        return 0
    elif key > node_key:
        return 1
    return -1
 
 
def size_tree(root):
    """Retorna el tamaño del subárbol con raíz en root (0 si es None)."""
    if root is None:
        return 0
    return root["size"]
 
 
def size(my_bst):
    """Retorna el número de nodos del árbol."""
    return size_tree(my_bst["root"])
 
 
def insert_node(root, key, value):
    """Inserta (o actualiza) recursivamente la pareja llave-valor y retorna la raíz del subárbol."""
    if root is None:
        return bs.new_node(key, value)
 
    cmp = default_compare(key, root)
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
 
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def put(my_bst, key, value):
    """Agrega una pareja llave-valor al árbol. Si la llave existe, actualiza el valor."""
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst
 
 
def get_node(root, key):
    """Busca recursivamente la llave y retorna el nodo encontrado, o None si no existe."""
    if root is None:
        return None
 
    cmp = default_compare(key, root)
    if cmp < 0:
        return get_node(root["left"], key)
    elif cmp > 0:
        return get_node(root["right"], key)
    return root
 
 
def get(my_bst, key):
    """Retorna el valor asociado a la llave, o None si no existe."""
    node = get_node(my_bst["root"], key)
    return bs.get_value(node)
 
 
def contains(my_bst, key):
    """Informa si la llave está en el árbol."""
    return get_node(my_bst["root"], key) is not None
 
 
def is_empty(my_bst):
    """Informa si el árbol está vacío."""
    return my_bst["root"] is None
 
 
def key_set(my_bst):
    """Retorna una lista con todas las llaves (inorder)."""
    llaves = sll.new_list()
    if my_bst is not None and my_bst["root"] is not None:
        key_set_tree(my_bst["root"], llaves)
    return llaves
 
 
def key_set_tree(node, my_list):
    if node is None:
        return my_list
    key_set_tree(node["left"], my_list)
    sll.add_last(my_list, bs.get_key(node))
    key_set_tree(node["right"], my_list)
    return my_list
 
 
def value_set(my_bst):
    """Retorna una lista con todos los valores (inorder)."""
    valores = sll.new_list()
    if my_bst is not None and my_bst["root"] is not None:
        value_set_tree(my_bst["root"], valores)
    return valores
 
 
def value_set_tree(node, my_list):
    if node is None:
        return my_list
    value_set_tree(node["left"], my_list)
    sll.add_last(my_list, bs.get_value(node))
    value_set_tree(node["right"], my_list)
    return my_list
 
 
def get_min(my_bst):
    """Retorna la llave mínima del árbol, o None si está vacío."""
    if my_bst is None or my_bst["root"] is None:
        return None
    return bs.get_key(get_min_node(my_bst["root"]))
 
 
def get_min_node(root):
    """Retorna el nodo con la llave mínima del subárbol."""
    if root is None:
        return None
    if root["left"] is None:
        return root
    return get_min_node(root["left"])
 
 
def get_max(my_bst):
    """Retorna la llave máxima del árbol, o None si está vacío."""
    if my_bst is None or my_bst["root"] is None:
        return None
    return bs.get_key(get_max_node(my_bst["root"]))
 
 
def get_max_node(root):
    """Retorna el nodo con la llave máxima del subárbol."""
    if root is None:
        return None
    if root["right"] is None:
        return root
    return get_max_node(root["right"])
 
 
def delete_min(my_bst):
    if my_bst is not None and my_bst["root"] is not None:
        my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst
 
 
def delete_min_tree(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def delete_max(my_bst):
    if my_bst is not None and my_bst["root"] is not None:
        my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst
 
 
def delete_max_tree(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"] = delete_max_tree(root["right"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def height(my_bst):
    """Retorna la altura del árbol (0 si está vacío)."""
    if my_bst["root"] is None:
        return 0
    return height_tree(my_bst["root"])


def height_tree(root):
    """Altura en aristas: un nodo hoja tiene altura 0."""
    if root is None:
        return -1
    return 1 + max(height_tree(root["left"]), height_tree(root["right"]))
 
 
def keys(my_bst, key_initial, key_final):
    """Retorna las llaves en el rango [key_initial, key_final]."""
    my_list = sll.new_list()
    if my_bst is not None and my_bst["root"] is not None:
        keys_range(my_bst["root"], key_initial, key_final, my_list)
    return my_list
 
 
def keys_range(root, key_initial, key_final, list_key):
    if root is None:
        return list_key
    cmplo = default_compare(key_initial, root)
    cmphi = default_compare(key_final, root)
    if cmplo < 0:
        keys_range(root["left"], key_initial, key_final, list_key)
    if cmplo <= 0 and cmphi >= 0:
        sll.add_last(list_key, bs.get_key(root))
    if cmphi > 0:
        keys_range(root["right"], key_initial, key_final, list_key)
    return list_key
 
 
def values(my_bst, key_initial, key_final):
    """Retorna los valores con llave en el rango [key_initial, key_final]."""
    my_list = sll.new_list()
    if my_bst is not None and my_bst["root"] is not None:
        values_range(my_bst["root"], key_initial, key_final, my_list)
    return my_list
 
 
def values_range(root, key_initial, key_final, list_value):
    if root is None:
        return list_value
    cmplo = default_compare(key_initial, root)
    cmphi = default_compare(key_final, root)
    if cmplo < 0:
        values_range(root["left"], key_initial, key_final, list_value)
    if cmplo <= 0 and cmphi >= 0:
        sll.add_last(list_value, bs.get_value(root))
    if cmphi > 0:
        values_range(root["right"], key_initial, key_final, list_value)
    return list_value


