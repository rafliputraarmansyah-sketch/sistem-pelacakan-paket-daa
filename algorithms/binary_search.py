
from models.tracking_event import TrackingEvent


class BinarySearcher:
    @staticmethod
    def _boundary(events, target, *, upper):
        low, high = 0, len(events)
        while low < high:
            mid = (low + high) // 2
            current = events[mid].tracking_id
            if current < target or (upper and current == target):
                low = mid + 1
            else:
                high = mid
        return low

    @classmethod
    def find_range(cls, sorted_events: list[TrackingEvent], target: str) -> tuple[int, int]:
        """Return [first, stop) for a list sorted by tracking ID."""
        first = cls._boundary(sorted_events, target, upper=False)
        stop = cls._boundary(sorted_events, target, upper=True)
        return first, stop
