from datetime import datetime

from algorithms.binary_search import BinarySearcher
from algorithms.merge_sort import MergeSorter
from models.tracking_event import TrackingEvent


class TrackingService:
    def __init__(self):
        self._events: list[TrackingEvent] = []
        self._next_id = 1

    @staticmethod
    def _tracking_id(value):
        clean = value.strip().upper()
        if not clean:
            raise ValueError("Nomor resi wajib diisi.")
        return clean

    def _make_event(self, event_id, tracking_id, event_time, status):
        if not isinstance(event_time, datetime) or event_time.tzinfo is not None:
            raise ValueError("Gunakan tanggal dan jam lokal tanpa zona waktu.")
        status = status.strip()
        if not status:
            raise ValueError("Status pengiriman wajib diisi.")
        return TrackingEvent(event_id, self._tracking_id(tracking_id), event_time, status)

    def _index(self, event_id):
        for index, event in enumerate(self._events):
            if event.event_id == event_id:
                return index
        raise ValueError(f"Catatan dengan ID {event_id} tidak ditemukan.")

    def create_event(self, tracking_id, event_time, status):
        event = self._make_event(self._next_id, tracking_id, event_time, status)
        self._events.append(event)
        self._next_id += 1
        return event

    def list_events(self):
        return self._events.copy()

    def get_event(self, event_id):
        return self._events[self._index(event_id)]

    def track_package(self, tracking_id):
        target = self._tracking_id(tracking_id)
        ordered = MergeSorter.sort(self._events)
        first, stop = BinarySearcher.find_range(ordered, target)
        return ordered[first:stop]

    def update_event(self, event_id, tracking_id, event_time, status):
        index = self._index(event_id)
        event = self._make_event(event_id, tracking_id, event_time, status)
        self._events[index] = event
        return event

    def delete_event(self, event_id):
        return self._events.pop(self._index(event_id))
