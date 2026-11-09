from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import pq_entry as pqe


def default_compare_higher_value(father_node, child_node):
    """True si el nodo padre tiene MAYOR prioridad (valor mayor) que el hijo."""
    return pqe.get_priority(father_node) > pqe.get_priority(child_node)


def default_compare_lower_value(father_node, child_node):
    """True si el nodo padre tiene MENOR prioridad (valor menor) que el hijo."""
    return pqe.get_priority(father_node) < pqe.get_priority(child_node)


def new_heap(is_min_pq=True):
    """Crea una cola de prioridad indexada orientada a menor (por defecto) o mayor."""
    if is_min_pq:
        cmp_function = default_compare_lower_value
    else:
        cmp_function = default_compare_higher_value

    return {
        "elements": lt.new_list(),
        "size": 0,
        "cmp_function": cmp_function,
    }


def priority(my_heap, parent, child):
    """True si 'parent' debe estar por encima de 'child' en el heap."""
    return my_heap["cmp_function"](parent, child)


def exchange(my_heap, pos1, pos2):
    """Intercambia las entradas de las posiciones pos1 y pos2 (base 1)."""
    elements = my_heap["elements"]
    entry1 = lt.get_element(elements, pos1 - 1)
    entry2 = lt.get_element(elements, pos2 - 1)
    lt.change_info(elements, pos1 - 1, entry2)
    lt.change_info(elements, pos2 - 1, entry1)
    return my_heap


def size(my_heap):
    """Número de elementos en la cola de prioridad."""
    return my_heap["size"]


def is_empty(my_heap):
    """True si la cola de prioridad no tiene elementos."""
    return size(my_heap) == 0


def swim(my_heap, pos):
    """Sube el elemento en 'pos' (base 1) hasta restaurar el orden del heap."""
    elements = my_heap["elements"]
    while pos > 1:
        parent_pos = pos // 2
        parent = lt.get_element(elements, parent_pos - 1)
        child = lt.get_element(elements, pos - 1)
        if priority(my_heap, child, parent):
            exchange(my_heap, parent_pos, pos)
            pos = parent_pos
        else:
            break
    return my_heap


def insert(my_heap, priority_value, value):
    """Inserta una nueva entrada (priority_value, value) y reordena con swim."""
    entry = pqe.new_pq_entry(priority_value, value)
    lt.add_last(my_heap["elements"], entry)
    my_heap["size"] += 1
    swim(my_heap, my_heap["size"])
    return my_heap


# ---------------------------------------------------------------------------
# Punto 3.1.2 (release final)
# ---------------------------------------------------------------------------

def sink(my_heap, pos):
    """Baja el elemento en 'pos' (base 1) hasta restaurar el orden del heap."""
    elements = my_heap["elements"]
    n = size(my_heap)
    while 2 * pos <= n:
        child_pos = 2 * pos
        # Elegir el hijo con mayor prioridad (izquierdo o derecho)
        if child_pos < n:
            left = lt.get_element(elements, child_pos - 1)
            right = lt.get_element(elements, child_pos)  # posición child_pos + 1
            if priority(my_heap, right, left):
                child_pos += 1
        current = lt.get_element(elements, pos - 1)
        child = lt.get_element(elements, child_pos - 1)
        # Si el hijo no tiene más prioridad que el padre, el orden ya es correcto
        if not priority(my_heap, child, current):
            break
        exchange(my_heap, pos, child_pos)
        pos = child_pos
    return my_heap


def remove(my_heap):
    """
    Elimina y retorna el VALOR de la entrada con mayor prioridad (la raíz).
    Retorna None si la cola está vacía.
    """
    if is_empty(my_heap):
        return None

    elements = my_heap["elements"]
    first = lt.get_element(elements, 0)
    n = size(my_heap)

    # Mover la última entrada a la raíz, eliminarla del final y reordenar
    exchange(my_heap, 1, n)
    lt.remove_last(elements)
    my_heap["size"] -= 1

    if not is_empty(my_heap):
        sink(my_heap, 1)

    return pqe.get_value(first)


def get_first_priority(my_heap):
    """
    Retorna el VALOR de la entrada con mayor prioridad sin eliminarla.
    Retorna None si la cola está vacía.
    """
    if is_empty(my_heap):
        return None
    return pqe.get_value(lt.get_element(my_heap["elements"], 0))


def is_present_value(my_heap, value):
    """
    Busca 'value' en la cola. Retorna su posición (base 1) si está presente,
    o -1 si no se encuentra.
    """
    elements = my_heap["elements"]
    for pos in range(1, size(my_heap) + 1):
        entry = lt.get_element(elements, pos - 1)
        if pqe.get_value(entry) == value:
            return pos
    return -1


def contains(my_heap, value):
    """True si 'value' está en la cola de prioridad."""
    return is_present_value(my_heap, value) != -1


def improve_priority(my_heap, new_priority, value):
    """
    Si 'value' está en la cola y 'new_priority' es MEJOR que su prioridad
    actual (según el tipo de heap), actualiza la prioridad y sube la entrada
    con swim. Si no está presente o no mejora, no hace nada.
    """
    pos = is_present_value(my_heap, value)
    if pos == -1:
        return my_heap

    entry = lt.get_element(my_heap["elements"], pos - 1)
    candidate = pqe.new_pq_entry(new_priority, value)

    if priority(my_heap, candidate, entry):
        pqe.set_priority(entry, new_priority)
        swim(my_heap, pos)
    return my_heap