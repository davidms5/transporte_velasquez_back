from rest_framework.pagination import PageNumberPagination

class CustomPaginator(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size' #esto es util para especificar en las query params, qué paginacion modificar
    max_page_size = 100
    
#class RutasPaginator(PageNumberPagination): TODO: para implementar despues
#    page_query_param = 'page_rutas'
#    page_size_query_param = 'page_size_rutas'
#    page_size = 10
#    max_page_size = 100
#
#class AsignacionesPaginator(PageNumberPagination):
#    page_query_param = 'page_asignaciones'
#    page_size_query_param = 'page_size_asignaciones'
#    page_size = 5
#    max_page_size = 50
#
#class HorariosPaginator(PageNumberPagination):
#    page_query_param = 'page_horarios'
#    page_size_query_param = 'page_size_horarios'
#    page_size = 3
#    max_page_size = 30