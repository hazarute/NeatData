"""
Timestamp Utilities
===================
Zaman damgası işlemleri.
"""

from datetime import datetime


def get_iso_timestamp() -> str:
    """
    ISO 8601 formatında zaman damgası döner.
    
    Returns:
        str: ISO 8601 formatında zaman (örn: 2025-11-24T15:30:00)
    """
    return datetime.utcnow().isoformat(timespec='seconds')
