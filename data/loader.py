import csv
from datetime import datetime
from pathlib import Path

from services.tracking_service import TrackingService


def build_demo_service():
    service = TrackingService()
    path = Path(__file__).with_name("dummy_events.csv")
    with path.open(encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            service.create_event(row["tracking_id"], datetime.fromisoformat(row["event_time"]), row["status"])
    return service
