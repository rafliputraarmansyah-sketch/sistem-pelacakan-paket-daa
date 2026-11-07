from models.tracking_event import TrackingEvent


class MergeSorter:
    @classmethod
    def sort(cls, events: list[TrackingEvent]) -> list[TrackingEvent]:
        if len(events) < 2:
            return events.copy()
        middle = len(events) // 2
        return cls._merge(cls.sort(events[:middle]), cls.sort(events[middle:]))

    @staticmethod
    def _merge(left, right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i].sort_key <= right[j].sort_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
