from datetime import datetime

from services.tracking_service import TrackingService


TIME_FORMAT = "%Y-%m-%d %H:%M"


class AdminCLI:
    def __init__(self, service: TrackingService):
        self.service = service

    @staticmethod
    def _show(events):
        if not events:
            print("Belum ada catatan pengiriman.")
            return
        print(f"{'ID':<5} {'Nomor resi':<14} {'Tanggal dan waktu':<19} Status")
        print("-" * 72)
        for event in events:
            stamp = event.event_time.strftime(TIME_FORMAT)
            print(f"{event.event_id:<5} {event.tracking_id:<14} {stamp:<19} {event.status}")

    @staticmethod
    def _time(text):
        try:
            return datetime.strptime(text.strip(), TIME_FORMAT)
        except ValueError:
            raise ValueError("Tanggal atau waktu tidak valid. Contoh: 2026-11-07 09:20.") from None

    @staticmethod
    def _id():
        try:
            return int(input("Masukkan ID catatan: "))
        except ValueError:
            raise ValueError("ID catatan harus berupa bilangan bulat.") from None

    def create(self):
        resi = input("Nomor resi: ")
        stamp = self._time(input("Tanggal dan waktu (contoh 2026-11-07 09:20): "))
        status = input("Status pengiriman: ")
        event = self.service.create_event(resi, stamp, status)
        print(f"Catatan ID {event.event_id} untuk resi {event.tracking_id} berhasil ditambahkan.")

    def list_all(self):
        self._show(self.service.list_events())

    def track(self):
        resi = input("Masukkan nomor resi yang ingin dilacak: ").strip().upper()
        history = self.service.track_package(resi)
        if not history:
            print(f"Nomor resi {resi} tidak ditemukan.")
            return
        print(f"Riwayat paket {resi} — jumlah catatan: {len(history)}")
        self._show(history)

    def update(self):
        current = self.service.get_event(self._id())
        self._show([current])
        print("Tekan Enter untuk mempertahankan nilai lama.")
        resi = input(f"Nomor resi [{current.tracking_id}]: ").strip()
        stamp = input(f"Tanggal dan waktu [{current.event_time:{TIME_FORMAT}}]: ").strip()
        status = input(f"Status [{current.status}]: ").strip()
        updated = self.service.update_event(
            current.event_id, resi or current.tracking_id,
            self._time(stamp) if stamp else current.event_time,
            status or current.status,
        )
        print("Catatan berhasil diperbarui.")
        self._show([updated])

    def delete(self):
        event = self.service.delete_event(self._id())
        print(f"Catatan ID {event.event_id} pada resi {event.tracking_id} berhasil dihapus.")

    def run(self):
        actions = {"1": self.create, "2": self.list_all, "3": self.track,
                   "4": self.update, "5": self.delete}
        while True:
            print("\nSISTEM PENCATATAN DAN PELACAKAN RIWAYAT PAKET")
            print("Menu Admin Ekspedisi")
            print("1. Tambah catatan pengiriman\n2. Tampilkan seluruh catatan")
            print("3. Lacak paket berdasarkan nomor resi\n4. Ubah catatan pengiriman")
            print("5. Hapus catatan pengiriman\n0. Keluar")
            try:
                choice = input("Pilih menu: ").strip()
                if choice == "0":
                    break
                action = actions.get(choice)
                if action is None:
                    print("Pilih salah satu angka dari 0 sampai 5.")
                else:
                    action()
            except ValueError as error:
                print(f"Kesalahan: {error}")
            except (EOFError, KeyboardInterrupt):
                break
        print("Program selesai.")
