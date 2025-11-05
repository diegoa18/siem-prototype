def parse_event(record):
    return {
        "event_id": record.EventID,
        "source": record.SourceName,
        "time_generated": str(record.TimeGenerated),
        "computer": record.ComputerName,
        "category": record.EventCategory,
        "message": record.StringInserts,
    }