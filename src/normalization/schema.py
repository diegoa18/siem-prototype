from enum import Enum
#DEFINICION DE TAXONOMIA, NORMALIZACION Y ESTRUCTURA DE DATOS

class ParsedFields: #definicion de campos estandar para el diccionario de eventos (plano o anidado)
    #campos basicos
    TIMESTAMP = "@timestamp"  #fecha en formato epoch (float)
    EVENT_ID = "event.id"     #ID unico del evento (si existe)
    EVENT_KIND = "event.kind" #tipo de evento (ej: "event", "alert")
    EVENT_CATEGORY = "event.category" #categoria del evento (ej: "authentication", "process")
    MESSAGE = "message" #mensaje del evento
    
    # Windows
    WIN_SYSTEM_EVENT_ID = "win.system.event_id" #ID original de Windows (ej: 4625)
    WIN_SYSTEM_CHANNEL = "win.system.channel"   #ej: Security, System
    WIN_SYSTEM_COMPUTER = "win.system.computer" #nombre del computador
    WIN_SYSTEM_PROVIDER = "win.system.provider_name" #proveedor del evento
    WIN_SYSTEM_RECORD_NUMBER = "win.system.record_number" #numero de registro
    WIN_SYSTEM_EVENT_DATA = "win.system.event_data" #datos crudos si hacen falta
    
    #especificos de autenticacion windows
    WIN_AUTH_LOGON_TYPE = "win.auth.logon_type" #tipo de logon
    WIN_AUTH_FAILURE_REASON = "win.auth.failure_reason" #razon del fallo
    
    #usuario / cuenta
    USER_NAME = "user.name" #nombre del usuario
    USER_DOMAIN = "user.domain" #dominio del usuario
    USER_ID = "user.id" #SID del usuario
    
    #origen / destino (red)
    SOURCE_IP = "source.ip" #IP del origen
    SOURCE_PORT = "source.port" #puerto del origen
    DEST_IP = "destination.ip" #IP del destino
    DEST_PORT = "destination.port" #puerto del destino
    
    #procesos
    PROCESS_NAME = "process.name" #nombre del proceso
    PROCESS_ID = "process.pid" #ID del proceso
    PROCESS_PATH = "process.executable" #ruta del ejecutable

class EventKind:
    EVENT = "event"
    ALERT = "alert"
    ERROR = "error"

class EventCategory:
    AUTHENTICATION = "authentication"
    PROCESS = "process"
    NETWORK = "network"
    FILE = "file"
    REGISTRY = "registry"
    IAM = "iam" #gestion de identidad y accesos
