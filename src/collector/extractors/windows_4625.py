from src.common.schema import ParsedFields

#EXTRACTOR ESPECIFICO PARA EVENTO 4625 (FALLO DE INICIO DE SESION)
def extract(record, parsed): #record es el evento, parsed es el diccionario que se va a llenar
    inserts = record.StringInserts or []

    #funcion auxiliar para obtener indice seguro
    def g(i):
        try:
            return inserts[i]
        except (IndexError, TypeError):
            return None

    #mapeo basado en indices tipicos del evento 4625    
    source_ip = g(18) or g(17) or g(16) or g(19) #se busca la ip en varias posiciones
    source_port = g(19) or g(20) #puerto suele estar al lado de la ip
    
    #nombre de cuenta y dominio
    t_account_name = g(5) or g(0)
    t_account_domain = g(6) or g(1)
    
    logon_type = g(10) or g(2)
    failure_reason = g(8) or g(7)

    #limpiar ip
    if source_ip in (None, "-", "", "::1", "127.0.0.1"):
         if source_ip in (None, "-", ""):
             source_ip = None

    #llenar campos estandar en el diccionario
    parsed[ParsedFields.USER_NAME] = t_account_name
    parsed[ParsedFields.USER_DOMAIN] = t_account_domain
    parsed[ParsedFields.SOURCE_IP] = source_ip
    parsed[ParsedFields.SOURCE_PORT] = source_port
    
    #campos especificos de autenticacion
    parsed[ParsedFields.WIN_AUTH_LOGON_TYPE] = logon_type
    parsed[ParsedFields.WIN_AUTH_FAILURE_REASON] = failure_reason
    
    #categorias generales
    parsed[ParsedFields.EVENT_CATEGORY] = "authentication"
    parsed[ParsedFields.EVENT_KIND] = "event"

    return parsed
