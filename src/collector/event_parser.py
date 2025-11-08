def safe_value(value):
    try:
        return str(value)
    except:
        return None

def parse_event(record):
    inserts = record.StringInserts if record.StringInserts else []
    parsed = {
        "event_id": safe_value(record.EventID),
        "record_number": safe_value(record.RecordNumber),
        "source": safe_value(record.SourceName),
        "time_generated": safe_value(record.TimeGenerated),
        "category": safe_value(record.EventCategory),
        "computer": safe_value(record.ComputerName),
        "message": safe_value(inserts),
        "event_type": safe_value(record.EventType),
        "event_type_name": safe_value(getattr(record, "EventTypeName", None)),
    }

    #INFORMACION EXTRA UTIL PARA EVENTO 4625
    if record.EventID == 4625:
        parsed.update({
            "account_name": inserts[0] if len(inserts) > 0 else None,
            "account_domain": inserts[1] if len(inserts) > 1 else None,
            "logon_type": inserts[2] if len(inserts) > 2 else None,
            "source_ip": inserts[5] if len(inserts) > 5 else None,
            "source_port": inserts[6] if len(inserts) > 6 else None,
        })

    return parsed