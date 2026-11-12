
import sys
 
from tabulate import tabulate
 
from DataStructures.List import array_list as al
 
try:
    from App import logic as lg
except ImportError:
    import logic as lg
 
# Límite de recursión sugerido en el enunciado (árboles grandes)
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
 
# Carpeta y prefijo de los archivos de datos (cambiar si la ruta es otra)
DATA_DIR = "Data/Data/"
FILE_PREFIX = "global_sports_footwear_sales-"
 
 
def new_logic():
    """
        Se crea una instancia del controlador
    """
    return lg.new_logic()
 
 
def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")
    print("8- Consultar una orden por su id")
 
 
# ---------------------------------------------------------------------------
# Utilidades de entrada y salida
# ---------------------------------------------------------------------------
 
def ask_float(message):
    """Pide un número decimal hasta que el usuario escriba uno válido."""
    while True:
        text = input(message).strip()
        try:
            return float(text)
        except ValueError:
            print("Valor inválido, escriba un número (ej: 12.5).")
 
 
def ask_int(message):
    """Pide un entero positivo hasta que el usuario escriba uno válido."""
    while True:
        text = input(message).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Valor inválido, escriba un entero positivo.")
 
 
def ask_text(message):
    """Pide un texto no vacío."""
    while True:
        text = input(message).strip()
        if text != "":
            return text
        print("El valor no puede estar vacío.")
 
 
def ask_date(message):
    """Pide una fecha con formato AAAA-MM-DD."""
    while True:
        text = input(message).strip()
        ok = (len(text) == 10 and text[4] == '-' and text[7] == '-' and
              text[0:4].isdigit() and text[5:7].isdigit() and text[8:10].isdigit())
        if ok:
            return text
        print("Formato inválido, use AAAA-MM-DD (ej: 2021-01-31).")
 
 
def show_table(headers, rows):
    """Imprime con tabulate un array_list de filas (cada fila es una lista)."""
    print(tabulate(al.to_py_list(rows), headers=headers, tablefmt="grid",
                   floatfmt=".2f"))
 
 
def is_loaded(control):
    """Verifica que los datos ya estén cargados."""
    if al.size(control['sales']) == 0:
        print("Primero debe cargar la información (opción 0).\n")
        return False
    return True
 
 
def sale_row_short(rec):
    return [rec['order_id'], rec['brand'], rec['model_name'], rec['category'],
            rec['final_price_usd'], rec['country']]
 
 
def sale_row_full(rec):
    return [rec['order_id'], rec['order_date'], rec['brand'], rec['model_name'],
            rec['category'], rec['final_price_usd'], rec['units_sold'],
            rec['revenue_usd'], rec['country'], rec['sales_channel']]
 
 
# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------
 
def load_data(control):
    """
    Carga los datos
    """
    size = input("Tamaño del archivo (test, small, medium, large) [small]: ").strip()
    if size == "":
        size = "small"
    filename = DATA_DIR + FILE_PREFIX + size + ".csv"
 
    try:
        data = lg.load_data(control, filename)
    except FileNotFoundError:
        print("No se encontró el archivo: " + filename + "\n")
        return None
 
    print("\nTiempo de carga: " + str(data['time_ms']) + " ms")
    print("Total de registros cargados: " + str(data['total']))
 
    if data['total'] == 0:
        return data
 
    headers_short = ["order_id", "brand", "model_name", "category",
                     "final_price_usd", "country"]
    rows = al.new_list()
    al.add_last(rows, sale_row_short(data['min_sale']))
    print("\nVenta con menor precio final:")
    show_table(headers_short, rows)
 
    rows = al.new_list()
    al.add_last(rows, sale_row_short(data['max_sale']))
    print("\nVenta con mayor precio final:")
    show_table(headers_short, rows)
 
    headers_full = ["order_id", "Fecha", "Marca", "Modelo", "Categoría",
                    "Precio final (USD)", "Unidades", "Ingreso (USD)",
                    "País", "Canal"]
    rows = al.new_list()
    for i in range(al.size(data['first5'])):
        al.add_last(rows, sale_row_full(al.get_element(data['first5'], i)))
    print("\nPrimeros 5 registros cargados:")
    show_table(headers_full, rows)
 
    rows = al.new_list()
    for i in range(al.size(data['last5'])):
        al.add_last(rows, sale_row_full(al.get_element(data['last5'], i)))
    print("\nÚltimos 5 registros cargados:")
    show_table(headers_full, rows)
    print()
    return data
 
 
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    sale = lg.get_sale(control, id)
    if sale is None:
        print("No existe una orden con el id " + str(id) + ".\n")
        return
 
    # Una fila por atributo, para ver todos los datos de la orden
    rows = al.new_list()
    al.add_last(rows, ["order_id", sale['order_id']])
    al.add_last(rows, ["Fecha de la orden", sale['order_date']])
    al.add_last(rows, ["Marca", sale['brand']])
    al.add_last(rows, ["Modelo", sale['model_name']])
    al.add_last(rows, ["Categoría", sale['category']])
    al.add_last(rows, ["Género", sale['gender']])
    al.add_last(rows, ["Talla", sale['size']])
    al.add_last(rows, ["Color", sale['color']])
    al.add_last(rows, ["Precio base (USD)", sale['base_price_usd']])
    al.add_last(rows, ["Descuento (%)", sale['discount_percent']])
    al.add_last(rows, ["Precio final (USD)", sale['final_price_usd']])
    al.add_last(rows, ["Unidades vendidas", sale['units_sold']])
    al.add_last(rows, ["Ingreso generado (USD)", sale['revenue_usd']])
    al.add_last(rows, ["Método de pago", sale['payment_method']])
    al.add_last(rows, ["Canal de venta", sale['sales_channel']])
    al.add_last(rows, ["País", sale['country']])
    al.add_last(rows, ["Nivel de ingresos del cliente", sale['customer_income_level']])
    al.add_last(rows, ["Calificación del cliente", sale['customer_rating']])
    show_table(["Atributo", "Valor"], rows)
    print()
 
 
def print_data_menu(control):
    """Pide un id y llama a print_data."""
    if not is_loaded(control):
        return
    order_id = ask_text("order_id a consultar: ")
    print_data(control, order_id)
 
 
# ---------------------------------------------------------------------------
# Requerimientos
# ---------------------------------------------------------------------------
 
def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    if not is_loaded(control):
        return
    brand = ask_text("Marca a analizar (ej: Nike): ")
    disc_lo = ask_float("Descuento mínimo (%): ")
    disc_hi = ask_float("Descuento máximo (%): ")
 
    result = lg.req_1(control, brand, disc_lo, disc_hi)
 
    print("\nTiempo de ejecución: " + str(result['time_ms']) + " ms")
    print("Total de órdenes: " + str(result['total']))
    print("Costo total final: " + str(round(result['total_cost'], 2)) + " USD")
 
    if result['total'] == 0:
        print("No hay órdenes que cumplan el filtro.\n")
        return
    if result['total'] > 10:
        print("Se muestran las 5 primeras y las 5 últimas órdenes.")
 
    headers = ["order_id", "Fecha", "Marca", "Modelo", "Categoría", "País",
               "Canal", "Descuento (%)", "Precio final (USD)"]
    rows = al.new_list()
    for i in range(al.size(result['rows'])):
        r = al.get_element(result['rows'], i)
        al.add_last(rows, [r['order_id'], r['order_date'], r['brand'],
                           r['model_name'], r['category'], r['country'],
                           r['sales_channel'], r['discount_percent'],
                           r['final_price_usd']])
    show_table(headers, rows)
    print()
 
 
def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    if not is_loaded(control):
        return
    country = ask_text("País a analizar (ej: USA): ")
    rating_lo = ask_float("Calificación mínima: ")
    rating_hi = ask_float("Calificación máxima: ")
 
    result = lg.req_2(control, country, rating_lo, rating_hi)
 
    print("\nTiempo de ejecución: " + str(result['time_ms']) + " ms")
    print("Total de órdenes: " + str(result['total']))
    print("Costo total final: " + str(round(result['total_cost'], 2)) + " USD")
 
    if result['total'] == 0:
        print("No hay órdenes que cumplan el filtro.\n")
        return
    if result['total'] > 10:
        print("Se muestran las 5 primeras y las 5 últimas órdenes.")
 
    headers = ["order_id", "Fecha", "Marca", "Modelo", "País", "Canal",
               "Calificación", "Precio final (USD)", "Ingreso total (USD)"]
    rows = al.new_list()
    for i in range(al.size(result['rows'])):
        r = al.get_element(result['rows'], i)
        al.add_last(rows, [r['order_id'], r['order_date'], r['brand'],
                           r['model_name'], r['country'], r['sales_channel'],
                           r['customer_rating'], r['final_price_usd'],
                           r['revenue_usd']])
    show_table(headers, rows)
    print()
 
 
def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass
 
 
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    if not is_loaded(control):
        return
    date_lo = ask_date("Fecha inicial (AAAA-MM-DD): ")
    date_hi = ask_date("Fecha final (AAAA-MM-DD): ")
    income = ask_text("Nivel de ingresos (Low, Medium, High): ")
    n = ask_int("Cantidad N de marcas a mostrar: ")
 
    result = lg.req_4(control, date_lo, date_hi, income, n)
 
    print("\nTiempo de ejecución: " + str(result['time_ms']) + " ms")
    print("Total de marcas consideradas: " + str(result['total_brands']))
 
    if result['n'] == 0:
        print("No hay órdenes que cumplan el filtro.\n")
        return
 
    headers = ["Marca", "# Órdenes", "Precio final prom. (USD)",
               "Ingreso prom. (USD)", "order_id", "Fecha", "Modelo", "País",
               "Canal", "Precio final (USD)", "Ingreso (USD)"]
    rows = al.new_list()
    for i in range(al.size(result['brands'])):
        b = al.get_element(result['brands'], i)
        o = b['best']
        al.add_last(rows, [b['brand'], b['count'], b['avg_price'],
                           b['avg_revenue'], o['order_id'], o['order_date'],
                           o['model_name'], o['country'], o['sales_channel'],
                           o['final_price_usd'], o['revenue_usd']])
    print("Orden con mayor ingreso generado por marca:")
    show_table(headers, rows)
    print()
 
 
def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    if not is_loaded(control):
        return
    country = ask_text("País (ej: Germany): ")
    date_lo = ask_date("Fecha inicial (AAAA-MM-DD): ")
    date_hi = ask_date("Fecha final (AAAA-MM-DD): ")
    n = ask_int("Cantidad N de marcas a mostrar: ")
 
    result = lg.req_5(control, country, date_lo, date_hi, n)
 
    print("\nTiempo de ejecución: " + str(result['time_ms']) + " ms")
    print("Total de marcas consideradas: " + str(result['total_brands']))
 
    if result['n'] == 0:
        print("No hay órdenes que cumplan el filtro.\n")
        return
 
    headers = ["Marca", "# Órdenes", "Calificación prom.", "Ingreso prom. (USD)",
               "order_id", "Fecha", "Modelo", "País", "Canal",
               "Unidades", "Calificación"]
    rows = al.new_list()
    for i in range(al.size(result['brands'])):
        b = al.get_element(result['brands'], i)
        o = b['best']
        al.add_last(rows, [b['brand'], b['count'], b['avg_rating'],
                           b['avg_revenue'], o['order_id'], o['order_date'],
                           o['model_name'], o['country'], o['sales_channel'],
                           o['units_sold'], o['customer_rating']])
    print("Orden con más unidades vendidas por marca:")
    show_table(headers, rows)
    print()
 
 
def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    if not is_loaded(control):
        return
    date_lo = ask_date("Fecha inicial (AAAA-MM-DD): ")
    date_hi = ask_date("Fecha final (AAAA-MM-DD): ")
    price_lo = ask_float("Precio base mínimo (USD): ")
    price_hi = ask_float("Precio base máximo (USD): ")
    n = ask_int("Cantidad N de marcas a mostrar: ")
 
    result = lg.req_6(control, date_lo, date_hi, price_lo, price_hi, n)
 
    print("\nTiempo de ejecución: " + str(result['time_ms']) + " ms")
    print("Total de marcas en el filtro: " + str(result['total_brands']))
 
    if result['n'] == 0:
        print("No hay órdenes que cumplan el filtro.\n")
        return
 
    headers = ["Marca", "# Órdenes", "Descuento prom. (%)",
               "Desv. estándar (pp)", "order_id", "Fecha", "Modelo", "País",
               "Canal", "Descuento (%)"]
    rows = al.new_list()
    for i in range(al.size(result['brands'])):
        b = al.get_element(result['brands'], i)
        o = b['closest']
        al.add_last(rows, [b['brand'], b['count'], b['avg_discount'], b['std'],
                           o['order_id'], o['order_date'], o['model_name'],
                           o['country'], o['sales_channel'],
                           o['discount_percent']])
    print("Orden con descuento más cercano al promedio de la marca:")
    show_table(headers, rows)
    print()
 
 
# Se crea la lógica asociado a la vista
control = new_logic()
 
 
# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n').strip()
        if not inputs.isdigit():
            print("Opción errónea, vuelva a elegir.\n")
            continue
        option = int(inputs)
        if option == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif option == 1:
            print_req_1(control)
 
        elif option == 2:
            print_req_2(control)
 
        elif option == 3:
            print_req_3(control)
 
        elif option == 4:
            print_req_4(control)
 
        elif option == 5:
            print_req_5(control)
 
        elif option == 6:
            print_req_6(control)
 
        elif option == 7:
            working = False
            print("\nGracias por utilizar el programa")
 
        elif option == 8:
            print_data_menu(control)
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
 
 
if __name__ == "__main__":
    main()