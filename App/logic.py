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
    mp.put(catalog['by_id'], rec['order_id'], rec)
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
        # map: order_id -> venta (para print_data)
        'by_id': mp.new_map(1000, 4.0),
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
 
 
def get_sale(catalog, order_id):
    """Retorna la venta con ese order_id, o None si no existe."""
    return mp.get(catalog['by_id'], parse_id(str(order_id)))
 
 
# ---------------------------------------------------------------------------
# Req 1 (individual)
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


# ---------------------------------------------------------------------------
# Req 4 (grupal)
# ---------------------------------------------------------------------------
 
def req_4(catalog, date_lo, date_hi, income_level, n):
    """
    Top N marcas con más órdenes en [date_lo, date_hi] para un nivel de
    ingresos. Orden: órdenes desc, luego marca asc.
    Por marca: count, avg_price, avg_revenue y la orden de mayor ingreso
    (ante empate, la más reciente).
    """
    start = get_time()
    stats = mp.new_map(7, 4.0)
    tree = mp.get(catalog['by_income'], income_level)
 
    if tree is not None:
        buckets = rbt.values(tree, date_lo, date_hi)
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            for j in range(al.size(bucket)):
                rec = al.get_element(bucket, j)
                st = mp.get(stats, rec['brand'])
                if st is None:
                    st = {'brand': rec['brand'], 'count': 0, 'sum_price': 0.0,
                          'sum_rev': 0.0, 'best': rec}
                    mp.put(stats, rec['brand'], st)
                st['count'] += 1
                st['sum_price'] += rec['final_price_usd']
                st['sum_rev'] += rec['revenue_usd']
                best = st['best']
                if (rec['revenue_usd'] > best['revenue_usd'] or
                        (rec['revenue_usd'] == best['revenue_usd'] and
                         rec['order_date'] > best['order_date'])):
                    st['best'] = rec
 
    heap = pq.new_heap(True)
    values = mp.value_set(stats)
    for i in range(al.size(values)):
        st = al.get_element(values, i)
        # min-heap: (-órdenes, marca) => más órdenes primero, luego alfabético
        pq.insert(heap, (-st['count'], st['brand']), st)
 
    result = al.new_list()
    while al.size(result) < n and not pq.is_empty(heap):
        st = pq.remove(heap)
        al.add_last(result, {
            'brand': st['brand'],
            'count': st['count'],
            'avg_price': st['sum_price'] / st['count'],
            'avg_revenue': st['sum_rev'] / st['count'],
            'best': st['best'],
        })
 
    end = get_time()
    return {
        'time_ms': delta_time(start, end),
        'total_brands': mp.size(stats),
        'n': al.size(result),
        'brands': result,
    }
 
 
# ---------------------------------------------------------------------------
# Req 5 (grupal)
# ---------------------------------------------------------------------------
 
def req_5(catalog, country, date_lo, date_hi, n):
    """
    Top N marcas con mejor calificación promedio en un país y rango de fechas.
    Orden: calificación desc, luego marca asc.
    Por marca: count, avg_rating, avg_revenue y la orden con más unidades
    (ante empate, la de mayor order_id).
    """
    start = get_time()
    stats = mp.new_map(7, 4.0)
    tree = mp.get(catalog['by_country'], country)
 
    if tree is not None:
        buckets = rbt.values(tree, date_lo, date_hi)
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            for j in range(al.size(bucket)):
                rec = al.get_element(bucket, j)
                st = mp.get(stats, rec['brand'])
                if st is None:
                    st = {'brand': rec['brand'], 'count': 0, 'sum_rating': 0.0,
                          'sum_rev': 0.0, 'best': rec}
                    mp.put(stats, rec['brand'], st)
                st['count'] += 1
                st['sum_rating'] += rec['customer_rating']
                st['sum_rev'] += rec['revenue_usd']
                best = st['best']
                if (rec['units_sold'] > best['units_sold'] or
                        (rec['units_sold'] == best['units_sold'] and
                         rec['order_id'] > best['order_id'])):
                    st['best'] = rec
 
    heap = pq.new_heap(True)
    values = mp.value_set(stats)
    for i in range(al.size(values)):
        st = al.get_element(values, i)
        avg_rating = st['sum_rating'] / st['count']
        st['avg_rating'] = avg_rating
        # min-heap: (-promedio, marca) => mejor calificada primero, luego alfabético
        pq.insert(heap, (-avg_rating, st['brand']), st)
 
    result = al.new_list()
    while al.size(result) < n and not pq.is_empty(heap):
        st = pq.remove(heap)
        al.add_last(result, {
            'brand': st['brand'],
            'count': st['count'],
            'avg_rating': st['avg_rating'],
            'avg_revenue': st['sum_rev'] / st['count'],
            'best': st['best'],
        })
 
    end = get_time()
    return {
        'time_ms': delta_time(start, end),
        'total_brands': mp.size(stats),
        'n': al.size(result),
        'brands': result,
    }
 
 
# ---------------------------------------------------------------------------
# Req 6 (grupal)
# ---------------------------------------------------------------------------
 
def req_6(catalog, date_lo, date_hi, price_lo, price_hi, n):
    """
    Top N marcas más consistentes en descuentos (menor desviación estándar
    poblacional de discount_percent) en un rango de fechas y de precio base.
    Orden: desviación asc, luego promedio de descuento asc.
    Por marca: count, avg_discount, std y la orden cuyo descuento es más
    cercano al promedio (ante empate, el menor order_id).
    """
    start = get_time()
 
    # Filtro por fechas (RBT) y por precio base
    filtered = al.new_list()
    buckets = rbt.values(catalog['by_date'], date_lo, date_hi)
    for i in range(al.size(buckets)):
        bucket = al.get_element(buckets, i)
        for j in range(al.size(bucket)):
            rec = al.get_element(bucket, j)
            if price_lo <= rec['base_price_usd'] <= price_hi:
                al.add_last(filtered, rec)
 
    # Pasada 1: cantidad y promedio de descuento por marca
    stats = mp.new_map(7, 4.0)
    for i in range(al.size(filtered)):
        rec = al.get_element(filtered, i)
        st = mp.get(stats, rec['brand'])
        if st is None:
            st = {'brand': rec['brand'], 'count': 0, 'sum_disc': 0.0}
            mp.put(stats, rec['brand'], st)
        st['count'] += 1
        st['sum_disc'] += rec['discount_percent']
 
    values = mp.value_set(stats)
    for i in range(al.size(values)):
        st = al.get_element(values, i)
        st['mean'] = st['sum_disc'] / st['count']
        st['sq_dev'] = 0.0
        st['closest'] = None
        st['closest_diff'] = None
 
    # Pasada 2: suma de desvíos al cuadrado y orden más cercana al promedio
    for i in range(al.size(filtered)):
        rec = al.get_element(filtered, i)
        st = mp.get(stats, rec['brand'])
        dev = rec['discount_percent'] - st['mean']
        st['sq_dev'] += dev * dev
        diff = abs(dev)
        if (st['closest'] is None or diff < st['closest_diff'] or
                (diff == st['closest_diff'] and
                 rec['order_id'] < st['closest']['order_id'])):
            st['closest'] = rec
            st['closest_diff'] = diff
 
    heap = pq.new_heap(True)
    for i in range(al.size(values)):
        st = al.get_element(values, i)
        st['std'] = math.sqrt(st['sq_dev'] / st['count'])
        pq.insert(heap, (st['std'], st['mean'], st['brand']), st)
 
    result = al.new_list()
    while al.size(result) < n and not pq.is_empty(heap):
        st = pq.remove(heap)
        al.add_last(result, {
            'brand': st['brand'],
            'count': st['count'],
            'avg_discount': st['mean'],
            'std': st['std'],
            'closest': st['closest'],
        })
 
    end = get_time()
    return {
        'time_ms': delta_time(start, end),
        'total_brands': mp.size(stats),
        'n': al.size(result),
        'brands': result,
    }
 
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
