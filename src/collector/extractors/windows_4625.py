def extract(record, parsed):
    inserts = record.StringInserts or []

    def g(i):
        try:
            return inserts[i]
        except Exception:
            return None

    #A PARTIR DE LOS LOGS EN JSONL
    source_ip = g(18) or g(17) or g(16) or g(5) or None
    source_port = g(19) or g(6) or None
    account_name = g(5) or g(0) or parsed.get("account_name")
    account_domain = g(6) or g(1) or parsed.get("account_domain")
    logon_type = g(10) or g(2) or parsed.get("logon_type")
    failure_reason = g(8) or g(7) or parsed.get("failure_reason")

    #NORMALIZACION DE IP
    if source_ip in (None, "-", ""):
        source_ip = None

    parsed.update({
        "source_ip": source_ip,
        "source_port": source_port,
        "account_name": account_name,
        "account_domain": account_domain,
        "logon_type": logon_type,
        "failure_reason": failure_reason,
        "message": inserts if inserts else parsed.get("message")
    })

    return parsed
