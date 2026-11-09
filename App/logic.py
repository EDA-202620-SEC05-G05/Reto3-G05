import csv
import math
import time
 
from DataStructures.List import array_list as al
from DataStructures.Map import map_separate_chaining as mp
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Priority_queue import priority_queue as pq
 
csv.field_size_limit(2147483647)
 
 
# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
 
def get_time():
    """Tiempo actual en milisegundos."""
    return float(time.perf_counter() * 1000)
 
 
def delta_time(start, end):
    """Diferencia en milisegundos."""
    return round(end - start, 3)
 
 
def parse_id(text):
    """Si el order_id es numérico lo vuelve int; si no, lo deja como str."""
    text = text.strip()
    if text.isdigit():
        return int(text)
    return text
 
 
def build_record(row):
    """Convierte una fila del CSV en un registro con tipos numéricos."""
    return {
        'order_id': parse_id(row['order_id']),
        'order_date': row['order_date'].strip(),
        'brand': row['brand'].strip(),
        'model_name': row['model_name'].strip(),
        'category': row['category'].strip(),
        'gender': row['gender'].strip(),
        'size': row['size'].strip(),
        'color': row['color'].strip(),
        'base_price_usd': float(row['base_price_usd']),
        'discount_percent': float(row['discount_percent']),
        'final_price_usd': float(row['final_price_usd']),
        'units_sold': int(float(row['units_sold'])),
        'revenue_usd': float(row['revenue_usd']),
        'payment_method': row['payment_method'].strip(),
        'sales_channel': row['sales_channel'].strip(),
        'country': row['country'].strip(),
        'customer_income_level': row['customer_income_level'].strip(),
        'customer_rating': float(row['customer_rating']),
    }
 
 
def first_and_last(lst, limit=10, shown=5):
    """Si la lista tiene más de 'limit' elementos retorna los primeros y
    últimos 'shown'; si no, retorna la lista completa."""
    n = al.size(lst)
    if n <= limit:
        return lst
    out = al.new_list()
    for i in range(shown):
        al.add_last(out, al.get_element(lst, i))
    for i in range(n - shown, n):
        al.add_last(out, al.get_element(lst, i))
    return out
 
 
def index_by_date(tree, rec):
    """Agrega rec a un RBT cuya llave es la fecha y cuyo valor es un
    array_list con todas las ventas de esa fecha."""
    bucket = rbt.get(tree, rec['order_date'])
    if bucket is None:
        bucket = al.new_list()
        rbt.put(tree, rec['order_date'], bucket)
    al.add_last(bucket, rec)
 
 
def get_or_create_tree(table, key):
    """Retorna el RBT asociado a key en el mapa 'table' (lo crea si no existe)."""
    tree = mp.get(table, key)
    if tree is None:
        tree = rbt.new_map()
        mp.put(table, key, tree)
    return tree
 
 
def index_record(catalog, rec):
    """Inserta un registro en todos los índices del catálogo."""
    index_by_date(catalog['by_date'], rec)
    index_by_date(get_or_create_tree(catalog['by_income'], rec['customer_income_level']), rec)
    index_by_date(get_or_create_tree(catalog['by_country'], rec['country']), rec)
    tree = get_or_create_tree(catalog['by_brand_discount'], rec['brand'])
    key = (rec['discount_percent'], rec['order_date'], rec['order_id'])
    rbt.put(tree, key, rec)
 
 
# ---------------------------------------------------------------------------
# Catálogo y carga de datos
# ---------------------------------------------------------------------------
 
def new_logic():
    """Crea el catálogo con todas las estructuras e índices."""
    return {
        'sales': al.new_list(),
        # RBT: fecha -> array_list de ventas
        'by_date': rbt.new_map(),
        # map: marca -> RBT con llave (descuento, fecha, order_id)
        'by_brand_discount': mp.new_map(7, 4.0),
        # map: nivel de ingresos -> RBT (fecha -> array_list de ventas)
        'by_income': mp.new_map(3, 4.0),
        # map: país -> RBT (fecha -> array_list de ventas)
        'by_country': mp.new_map(31, 4.0),
    }
 
 
def load_data(catalog, filename):
    """
    Carga el CSV una sola vez, construye los índices y retorna un diccionario
    con: time_ms, total, min_sale, max_sale, first5, last5.
    """
    start = get_time()
    min_sale = None
    max_sale = None
 
    with open(filename, encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rec = build_record(row)
            al.add_last(catalog['sales'], rec)
            index_record(catalog, rec)
 
            price = rec['final_price_usd']
            # menor precio final: ante empate, el más reciente
            if (min_sale is None or price < min_sale['final_price_usd'] or
                    (price == min_sale['final_price_usd'] and
                     rec['order_date'] > min_sale['order_date'])):
                min_sale = rec
            # mayor precio final: ante empate, el más antiguo
            if (max_sale is None or price > max_sale['final_price_usd'] or
                    (price == max_sale['final_price_usd'] and
                     rec['order_date'] < max_sale['order_date'])):
                max_sale = rec
 
    sales = catalog['sales']
    total = al.size(sales)
    shown = min(5, total)
    first5 = al.new_list()
    last5 = al.new_list()
    for i in range(shown):
        al.add_last(first5, al.get_element(sales, i))
    for i in range(total - shown, total):
        al.add_last(last5, al.get_element(sales, i))
 
    end = get_time()
    return {
        'time_ms': delta_time(start, end),
        'total': total,
        'min_sale': min_sale,
        'max_sale': max_sale,
        'first5': first5,
        'last5': last5,
    }


# Req 1 
# ---------------------------------------------------------------------------
 
def req_1(catalog, brand, discount_lo, discount_hi):
    """
    Órdenes de una marca con descuento en [discount_lo, discount_hi].
    Orden: descuento asc, luego fecha asc (lo da la llave del RBT).
    Retorna: time_ms, total, total_cost, rows (array_list; solo 5+5 si hay más de 10).
    """
    start = get_time()
    tree = mp.get(catalog['by_brand_discount'], brand)
    found = al.new_list()
    if tree is not None:
        # El 2do elemento ("" o el máximo unicode) nunca empata con una fecha
        # real, así que el 3er elemento de la cota no se llega a comparar.
        low_key = (discount_lo, "", 0)
        high_key = (discount_hi, "\U0010ffff", 0)
        found = rbt.values(tree, low_key, high_key)
 
    total_cost = 0.0
    for i in range(al.size(found)):
        total_cost += al.get_element(found, i)['final_price_usd']
 
    rows = first_and_last(found)
    end = get_time()
    return {
        'time_ms': delta_time(start, end),
        'total': al.size(found),
        'total_cost': total_cost,
        'rows': rows,
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
