from DataStructures.Tree import rbt_node as rn
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
 
RED = rn.RED
BLACK = rn.BLACK
 
 
# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
 
def default_compare(key, element):
    """Compara una llave con la llave de un nodo.
    Retorna 0 si son iguales, 1 si key es mayor, -1 si key es menor."""
    node_key = rn.get_key(element)
    if key == node_key:
        return 0
    elif key > node_key:
        return 1
    return -1
 
 
def is_red(my_node):
    """Versión segura de rbt_node.is_red: un nodo None cuenta como negro."""
    return my_node is not None and rn.is_red(my_node)
 
 
def size_tree(root):
    """Retorna el tamaño del subárbol que cuelga de root (0 si es None)."""
    if root is None:
        return 0
    return root["size"]
 
 
def flip_node_color(node):
    """Invierte el color de un nodo."""
    if is_red(node):
        rn.change_color(node, BLACK)
    else:
        rn.change_color(node, RED)
    return node
 
 
def flip_colors(node):
    """Invierte el color del nodo y de sus dos hijos."""
    flip_node_color(node)
    flip_node_color(node["left"])
    flip_node_color(node["right"])
    return node
 
 
def rotate_left(node_rbt):
    """Rota a la izquierda: el hijo derecho pasa a ser la raíz del subárbol."""
    x = node_rbt["right"]
    node_rbt["right"] = x["left"]
    x["left"] = node_rbt
    x["color"] = node_rbt["color"]
    rn.change_color(node_rbt, RED)
    x["size"] = node_rbt["size"]
    node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])
    return x
 
 
def rotate_right(node_rbt):
    """Rota a la derecha: el hijo izquierdo pasa a ser la raíz del subárbol."""
    x = node_rbt["left"]
    node_rbt["left"] = x["right"]
    x["right"] = node_rbt
    x["color"] = node_rbt["color"]
    rn.change_color(node_rbt, RED)
    x["size"] = node_rbt["size"]
    node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])
    return x
 
 
# ---------------------------------------------------------------------------
# Funciones principales (máscaras) y recursivas
# ---------------------------------------------------------------------------
 
def new_map():
    """Crea una tabla de símbolos ordenada vacía basada en un RBT."""
    return {"root": None, "type": "RBT"}
 
 
def put(my_rbt, key, value):
    """Ingresa la pareja llave-valor. Si la llave existe, reemplaza el valor."""
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    rn.change_color(my_rbt["root"], BLACK)
    return my_rbt
 
 
def insert_node(root, key, value):
    """Inserta recursivamente la pareja y rebalancea al regresar."""
    if root is None:
        return rn.new_node(key, value, RED)
 
    cmp = default_compare(key, root)
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value
 
    # Rebalanceo
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
 
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def get(my_rbt, key):
    """Retorna el valor asociado a key, o None si no existe."""
    return get_node(my_rbt["root"], key)
 
 
def get_node(root, key):
    """Busca recursivamente la llave y retorna su valor (None si no está)."""
    if root is None:
        return None
    cmp = default_compare(key, root)
    if cmp < 0:
        return get_node(root["left"], key)
    elif cmp > 0:
        return get_node(root["right"], key)
    return rn.get_value(root)
 
 
def contains(my_rbt, key):
    """Retorna True si la llave está en el árbol."""
    return get(my_rbt, key) is not None
 
 
def size(my_rbt):
    """Retorna el número de parejas en el árbol."""
    return size_tree(my_rbt["root"])
 
 
def is_empty(my_rbt):
    """Retorna True si el árbol no tiene elementos."""
    return my_rbt["root"] is None
 
 
def key_set(my_rbt):
    """Retorna una lista con todas las llaves, en orden."""
    key_list = sl.new_list()
    key_set_tree(my_rbt["root"], key_list)
    return key_list
 
 
def key_set_tree(root, key_list):
    """Recorrido in-order que agrega las llaves a key_list."""
    if root is not None:
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, rn.get_key(root))
        key_set_tree(root["right"], key_list)
    return key_list
 
 
def value_set(my_rbt):
    """Retorna una lista con todos los valores, en el orden de sus llaves."""
    value_list = sl.new_list()
    value_set_tree(my_rbt["root"], value_list)
    return value_list
 
 
def value_set_tree(root, value_list):
    """Recorrido in-order que agrega los valores a value_list."""
    if root is not None:
        value_set_tree(root["left"], value_list)
        sl.add_last(value_list, rn.get_value(root))
        value_set_tree(root["right"], value_list)
    return value_list
 
 
def get_min(my_rbt):
    """Retorna la llave más pequeña (None si el árbol está vacío)."""
    return rn.get_key(get_min_node(my_rbt["root"]))
 
 
def get_min_node(root):
    """Retorna el nodo con la llave más pequeña del subárbol."""
    if root is None:
        return None
    if root["left"] is None:
        return root
    return get_min_node(root["left"])
 
 
def get_max(my_rbt):
    """Retorna la llave más grande (None si el árbol está vacío)."""
    return rn.get_key(get_max_node(my_rbt["root"]))
 
 
def get_max_node(root):
    """Retorna el nodo con la llave más grande del subárbol."""
    if root is None:
        return None
    if root["right"] is None:
        return root
    return get_max_node(root["right"])
 
 
def left_key(my_rbt):
    """Llave más pequeña del árbol (alias de get_min)."""
    return get_min(my_rbt)
 
 
def right_key(my_rbt):
    """Llave más grande del árbol (alias de get_max)."""
    return get_max(my_rbt)
 
 
def height(my_rbt):
    """Retorna la altura del árbol."""
    return height_tree(my_rbt["root"])
 
 
def height_tree(root):
    """Altura del subárbol contada en aristas: un árbol vacío o de un solo
    nodo tiene altura 0; en otro caso 1 + máx(alturas de los hijos)."""
    if root is None:
        return 0
    if root["left"] is None and root["right"] is None:
        return 0
    return 1 + max(height_tree(root["left"]), height_tree(root["right"]))
 
 
def keys(my_rbt, key_initial, key_final):
    """Retorna las llaves en el rango [key_initial, key_final]."""
    key_list = al.new_list()
    keys_range(my_rbt["root"], key_initial, key_final, key_list)
    return key_list
 
 
def keys_range(root, key_initial, key_final, list_key):
    """Recorrido in-order, podando ramas fuera del rango."""
    if root is None:
        return list_key
    key = rn.get_key(root)
    if key_initial < key:
        keys_range(root["left"], key_initial, key_final, list_key)
    if key_initial <= key <= key_final:
        al.add_last(list_key, key)
    if key < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)
    return list_key
 
 
def values(my_rbt, key_initial, key_final):
    """Retorna los valores cuyas llaves están en [key_initial, key_final]."""
    value_list = al.new_list()
    values_range(my_rbt["root"], key_initial, key_final, value_list)
    return value_list
 
 
def values_range(root, key_initial, key_final, list_values):
    """Recorrido in-order, podando ramas fuera del rango."""
    if root is None:
        return list_values
    key = rn.get_key(root)
    if key_initial < key:
        values_range(root["left"], key_initial, key_final, list_values)
    if key_initial <= key <= key_final:
        al.add_last(list_values, rn.get_value(root))
    if key < key_final:
        values_range(root["right"], key_initial, key_final, list_values)
    return list_values
 
 
# ---------------------------------------------------------------------------
# Balanceo y eliminación
# ---------------------------------------------------------------------------
 
def balance(root):
    """Restaura las propiedades del RBT en el nodo y actualiza su tamaño."""
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
 
def move_red_left(root):
    """Asume que root es rojo y root.left y root.left.left son negros;
    hace que root.left o uno de sus hijos sea rojo."""
    flip_colors(root)
    if is_red(root["right"]["left"]):
        root["right"] = rotate_right(root["right"])
        root = rotate_left(root)
        flip_colors(root)
    return root
 
 
def move_red_right(root):
    """Asume que root es rojo y root.right y root.right.left son negros;
    hace que root.right o uno de sus hijos sea rojo."""
    flip_colors(root)
    if is_red(root["left"]["left"]):
        root = rotate_right(root)
        flip_colors(root)
    return root
 
 
def delete_min(my_rbt):
    """Elimina la pareja con la llave más pequeña."""
    if my_rbt["root"] is None:
        return my_rbt
    root = my_rbt["root"]
    if not is_red(root["left"]) and not is_red(root["right"]):
        rn.change_color(root, RED)
    my_rbt["root"] = delete_min_tree(root)
    if my_rbt["root"] is not None:
        rn.change_color(my_rbt["root"], BLACK)
    return my_rbt
 
 
def delete_min_tree(root):
    """Elimina recursivamente el nodo con la llave más pequeña."""
    if root["left"] is None:
        return None
    if not is_red(root["left"]) and not is_red(root["left"]["left"]):
        root = move_red_left(root)
    root["left"] = delete_min_tree(root["left"])
    return balance(root)
 
 
def delete_max(my_rbt):
    """Elimina la pareja con la llave más grande."""
    if my_rbt["root"] is None:
        return my_rbt
    root = my_rbt["root"]
    if not is_red(root["left"]) and not is_red(root["right"]):
        rn.change_color(root, RED)
    my_rbt["root"] = delete_max_tree(root)
    if my_rbt["root"] is not None:
        rn.change_color(my_rbt["root"], BLACK)
    return my_rbt
 
 
def delete_max_tree(root):
    """Elimina recursivamente el nodo con la llave más grande."""
    if is_red(root["left"]):
        root = rotate_right(root)
    if root["right"] is None:
        return None
    if not is_red(root["right"]) and not is_red(root["right"]["left"]):
        root = move_red_right(root)
    root["right"] = delete_max_tree(root["right"])
    return balance(root)
 
 
def remove(my_rbt, key):
    """Elimina la pareja con la llave dada (si existe)."""
    if not contains(my_rbt, key):
        return my_rbt
    root = my_rbt["root"]
    if not is_red(root["left"]) and not is_red(root["right"]):
        rn.change_color(root, RED)
    my_rbt["root"] = remove_key(root, key)
    if my_rbt["root"] is not None:
        rn.change_color(my_rbt["root"], BLACK)
    return my_rbt
 
 
def remove_key(root, key):
    """Elimina recursivamente la llave del subárbol (debe existir)."""
    if default_compare(key, root) < 0:
        if not is_red(root["left"]) and not is_red(root["left"]["left"]):
            root = move_red_left(root)
        root["left"] = remove_key(root["left"], key)
    else:
        if is_red(root["left"]):
            root = rotate_right(root)
        if default_compare(key, root) == 0 and root["right"] is None:
            return None
        if not is_red(root["right"]) and not is_red(root["right"]["left"]):
            root = move_red_right(root)
        if default_compare(key, root) == 0:
            min_node = get_min_node(root["right"])
            root["key"] = min_node["key"]
            root["value"] = min_node["value"]
            root["right"] = delete_min_tree(root["right"])
        else:
            root["right"] = remove_key(root["right"], key)
    return balance(root)
 
 
# ---------------------------------------------------------------------------
# Consultas por orden: floor, ceiling, rank, select
# ---------------------------------------------------------------------------
 
def floor(my_rbt, key):
    """Mayor llave menor o igual a key (None si no existe)."""
    return floor_key(my_rbt["root"], key)
 
 
def floor_key(root, key):
    if root is None:
        return None
    cmp = default_compare(key, root)
    if cmp == 0:
        return root["key"]
    if cmp < 0:
        return floor_key(root["left"], key)
    candidate = floor_key(root["right"], key)
    if candidate is not None:
        return candidate
    return root["key"]
 
 
def ceiling(my_rbt, key):
    """Menor llave mayor o igual a key (None si no existe)."""
    return ceiling_key(my_rbt["root"], key)
 
 
def ceiling_key(root, key):
    if root is None:
        return None
    cmp = default_compare(key, root)
    if cmp == 0:
        return root["key"]
    if cmp > 0:
        return ceiling_key(root["right"], key)
    candidate = ceiling_key(root["left"], key)
    if candidate is not None:
        return candidate
    return root["key"]
 
 
def rank(my_rbt, key):
    """Número de llaves estrictamente menores que key."""
    return rank_key(my_rbt["root"], key)
 
 
def rank_key(root, key):
    if root is None:
        return 0
    cmp = default_compare(key, root)
    if cmp < 0:
        return rank_key(root["left"], key)
    if cmp > 0:
        return 1 + size_tree(root["left"]) + rank_key(root["right"], key)
    return size_tree(root["left"])
 
 
def select(my_rbt, pos):
    """Llave de rango pos (0 = la más pequeña); None si pos es inválida."""
    return select_key(my_rbt["root"], pos)
 
 
def select_key(root, pos):
    if root is None:
        return None
    left_size = size_tree(root["left"])
    if left_size > pos:
        return select_key(root["left"], pos)
    if left_size < pos:
        return select_key(root["right"], pos - left_size - 1)
    return root["key"]