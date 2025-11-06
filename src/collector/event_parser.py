def safe_value(value):
    try:
        return str(value)
    except:
        return None

def parse_event(record):
    return {
        "event_id": safe_value(record.EventID),
        "record_number": safe_value(record.RecordNumber),
        "source": safe_value(record.SourceName),
        "time_generated": safe_value(record.TimeGenerated),
        "category": safe_value(record.EventCategory),
        "computer": safe_value(record.ComputerName),
        "message": safe_value(record.StringInserts),
        "event_type": safe_value(record.EventType),
        "event_type_name": safe_value(getattr(record, "EventTypeName", None)),
    }
