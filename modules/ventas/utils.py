def filtrar_facturas_no_duplicadas(facturas_manuales, facturas_db_set):
    return [f for f in facturas_manuales if f["numero_factura"] not in facturas_db_set]
