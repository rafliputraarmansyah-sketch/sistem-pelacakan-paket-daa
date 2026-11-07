from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TrackingEvent:
    event_id: int
    tracking_id: str
    event_time: datetime
    status: str

    @property
    def sort_key(self):
        return self.tracking_id, self.event_time
