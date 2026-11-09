from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
import random


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea una nueva tabla de símbolos (map) sin elementos, usando separate
    chaining para el manejo de colisiones.

    :param num_elements: Número de elementos que se desean almacenar en la tabla.
    :type num_elements: int
    :param load_factor: Factor de carga límite de la tabla antes de hacer un rehash.
    :type load_factor: float
    :param prime: Número primo utilizado para el cálculo del hash.
    :type prime: int

    :return: Tabla recién creada.
    :rtype: map
    """
    capacity = mf.next_prime(int(num_elements / load_factor))
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)

    table = lt.new_list()
    for _ in range(capacity):
        bucket = lt.new_list()
        lt.add_last(table, bucket)

    my_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
    }
    return my_map


def put(my_map, key, value):
    """
    Inserta una pareja llave-valor en la tabla. Si la llave ya existe,
    se actualiza su valor.

    :param my_map: Tabla de hash.
    :type my_map: map
    :param key: Llave a insertar.
    :type key: any
    :param value: Valor asociado a la llave.
    :type value: any

    :return: Tabla modificada.
    :rtype: map
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)

    pos = lt.is_present(bucket, key, mf.default_compare)
    entry = me.new_map_entry(key, value)

    if pos == -1:
        lt.add_last(bucket, entry)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        if my_map["current_factor"] >= my_map["limit_factor"]:
            rehash(my_map)
    else:
        lt.change_info(bucket, pos, entry)

    return my_map


def contains(my_map, key):
    """
    Verifica si una llave existe dentro de la tabla.

    :param my_map: Tabla de hash.
    :type my_map: map
    :param key: Llave a buscar.
    :type key: any

    :return: True si la llave existe, False en caso contrario.
    :rtype: bool
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = lt.is_present(bucket, key, mf.default_compare)
    return pos != -1


def get(my_map, key):
    """
    Retorna el valor asociado a una llave dentro de la tabla.

    :param my_map: Tabla de hash.
    :type my_map: map
    :param key: Llave a buscar.
    :type key: any

    :return: Valor asociado a la llave, o None si no existe.
    :rtype: any
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = lt.is_present(bucket, key, mf.default_compare)

    if pos == -1:
        return None

    entry = lt.get_element(bucket, pos)
    return me.get_value(entry)


def remove(my_map, key):
    """
    Elimina una pareja llave-valor de la tabla, si existe.

    :param my_map: Tabla de hash.
    :type my_map: map
    :param key: Llave a eliminar.
    :type key: any

    :return: Valor que tenía la llave eliminada, o None si no existía.
    :rtype: any
    """
    hash_value = mf.hash_value(my_map, key)
    bucket = lt.get_element(my_map["table"], hash_value)
    pos = lt.is_present(bucket, key, mf.default_compare)

    if pos == -1:
        return None

    entry = lt.get_element(bucket, pos)
    value = me.get_value(entry)
    lt.delete_element(bucket, pos)

    my_map["size"] -= 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return value


def size(my_map):
    """
    Retorna el número de entradas en el mapa.

    :param my_map: Mapa del cual se desea obtener el tamaño.
    :type my_map: map

    :return: Número de entradas en el mapa.
    :rtype: int
    """
    return my_map["size"]


def is_empty(my_map):
    """
    Indica si el mapa está vacío.

    :param my_map: Mapa a validar.
    :type my_map: map

    :return: True si el mapa no tiene entradas, False en caso contrario.
    :rtype: bool
    """
    return my_map["size"] == 0


def key_set(my_map):
    """
    Retorna una lista (array_list) con todas las llaves almacenadas en el mapa.

    :param my_map: Mapa del cual se desean obtener las llaves.
    :type my_map: map

    :return: Lista con las llaves del mapa.
    :rtype: array_list
    """
    keys = lt.new_list()
    for pos in range(my_map["capacity"]):
        bucket = lt.get_element(my_map["table"], pos)
        for bucket_pos in range(lt.size(bucket)):
            entry = lt.get_element(bucket, bucket_pos)
            lt.add_last(keys, me.get_key(entry))
    return keys


def value_set(my_map):
    """
    Retorna una lista (array_list) con todos los valores almacenados en el mapa.

    :param my_map: Mapa del cual se desean obtener los valores.
    :type my_map: map

    :return: Lista con los valores del mapa.
    :rtype: array_list
    """
    values = lt.new_list()
    for pos in range(my_map["capacity"]):
        bucket = lt.get_element(my_map["table"], pos)
        for bucket_pos in range(lt.size(bucket)):
            entry = lt.get_element(bucket, bucket_pos)
            lt.add_last(values, me.get_value(entry))
    return values


def rehash(my_map):
    """
    Amplía la capacidad de la tabla (al siguiente primo mayor al doble de
    la capacidad actual) y reinserta todas las entradas existentes.

    :param my_map: Tabla de hash.
    :type my_map: map

    :return: Tabla modificada.
    :rtype: map
    """
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = lt.new_list()
    for _ in range(new_capacity):
        bucket = lt.new_list()
        lt.add_last(new_table, bucket)

    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0

    for pos in range(old_capacity):
        old_bucket = lt.get_element(old_table, pos)
        for bucket_pos in range(lt.size(old_bucket)):
            entry = lt.get_element(old_bucket, bucket_pos)
            key = me.get_key(entry)
            value = me.get_value(entry)
            put(my_map, key, value)

    return my_map