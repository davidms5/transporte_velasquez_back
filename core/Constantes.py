from typing import Final
class Constantes:
    
    ADMIN: Final = "admin"
    OPERATOR: Final = "operator"
    SUPERVISOR: Final = "supervisor"
    BILLING: Final = "billing"
    
    def __setattr__(self, name, value):
        raise TypeError("No puedes modificar una constante")