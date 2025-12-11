#TAXONOMIA UNIVERSAL PARA TODAS LAS REGLAS
class RuleCategory: #categorias de alto nivel para las reglas (MITRE ATT&CK)

    INITIAL_ACCESS = "Initial Access" #acceso inicial
    EXECUTION = "Execution" #ejecucion
    PERSISTENCE = "Persistence" #persistencia
    PRIVILEGE_ESCALATION = "Privilege Escalation" #escalada de privilegios
    DEFENSE_EVASION = "Defense Evasion" #evasión de defensa
    CREDENTIAL_ACCESS = "Credential Access" #acceso a credenciales
    DISCOVERY = "Discovery" #descubrimiento
    LATERAL_MOVEMENT = "Lateral Movement" #movimiento lateral
    COLLECTION = "Collection" #coleccion
    EXFILTRATION = "Exfiltration" #exfiltracion
    COMMAND_AND_CONTROL = "Command and Control" #comando y control
    IMPACT = "Impact" #impacto

class RuleSeverity: #gravedad de la regla
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RuleStatus: #estado de la regla
    STABLE = "stable"
    TESTING = "testing"
    DEPRECATED = "deprecated"
