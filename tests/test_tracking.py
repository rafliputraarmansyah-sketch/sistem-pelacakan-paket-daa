import unittest
from datetime import datetime

from algorithms.binary_search import BinarySearcher
from algorithms.merge_sort import MergeSorter
from main import build_demo_service
from services.tracking_service import TrackingService


class TrackingTests(unittest.TestCase):
    def setUp(self):
        self.service = build_demo_service()

    def test_initial_data(self):
        events = self.service.list_events()
        self.assertEqual(len(events), 200)
        self.assertEqual(len({event.event_id for event in events}), 200)
        self.assertEqual(len({event.tracking_id for event in events}), 52)

    def test_sample(self):
        self.assertEqual([e.event_id for e in self.service.track_package(" r002 ")], [4, 7, 2])

    def test_boundaries(self):
        ordered = MergeSorter.sort(self.service.list_events())
        for resi, expected in [("R000", (0, 0)), ("R001", (0, 2)), ("R002", (2, 5)),
                               ("R004", (7, 8)), ("R052", (196, 200)), ("R999", (200, 200))]:
            with self.subTest(resi=resi):
                self.assertEqual(BinarySearcher.find_range(ordered, resi), expected)

    def test_empty(self):
        self.assertEqual(TrackingService().track_package("R002"), [])

    def test_crud_and_stability(self):
        service = self.service
        stamp = datetime(2026, 11, 8, 7)
        one = service.create_event("R002", stamp, "Paket tiba")
        two = service.create_event("R002", stamp, "Paket diserahkan")
        self.assertEqual(service.track_package("R002")[-2:], [one, two])
        service.update_event(one.event_id, "R105", stamp, "Koreksi nomor resi")
        self.assertEqual(len(service.track_package("R105")), 1)
        service.delete_event(two.event_id)
        self.assertEqual(len(service.track_package("R002")), 3)
        self.assertGreater(service.create_event("R006", stamp, "Baru").event_id, two.event_id)

    def test_invalid_update_preserves_record(self):
        old = self.service.get_event(7)
        with self.assertRaises(ValueError):
            self.service.update_event(7, "R002", old.event_time, " ")
        self.assertEqual(old, self.service.get_event(7))
        with self.assertRaises(ValueError):
            self.service.delete_event(999)
