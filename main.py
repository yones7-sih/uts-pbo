from rekening import Rekening, RekeningTabungan, RekeningGiro
from transaksi import Transaksi


class BankMiniApp:
    """Kelas pengelola aplikasi CLI untuk data rekening dan transaksi."""

    def __init__(self):
        # Menyimpan koleksi objek Rekening dan Transaksi
        self.__daftar_rekening: list[Rekening] = []
        self.__daftar_transaksi: list[Transaksi] = []
        self.__counter_transaksi = 1

    # --- Method bantu pencarian ---
    def _cari_rekening_by_nomor(self, no_rekening: str) -> Rekening | None:
        for rek in self.__daftar_rekening:
            if rek.get_no_rekening().lower() == no_rekening.strip().lower():
                return rek
        return None

    # --- 1. Menu Tambah Data ---
    def menu_tambah_data(self) -> None:
        print(" --- TAMBAH DATA ---")
        print("1. Tambah Rekening Baru (Tabungan / Giro)")
        print("2. Tambah Transaksi Baru (Setor / Tarik)")
        pilihan = input("Pilih submenu (1/2): ").strip()

        if pilihan == "1":
            no_rek = input("Nomor Rekening   : ").strip()
            if not no_rek:
                print("Nomor rekening tidak boleh kosong.")
                return
            if self._cari_rekening_by_nomor(no_rek) is not None:
                print("Nomor rekening sudah terdaftar.")
                return

            pemilik = input("Nama Pemilik     : ").strip()
            try:
                saldo_awal = float(input("Saldo Awal (Rp)  : "))
            except ValueError:
                print("Input saldo harus berupa angka.")
                return

            print("Jenis Rekening: [1] Tabungan  [2] Giro")
            jenis = input("Pilih jenis (1/2): ").strip()

            if jenis == "1":
                rek_baru = RekeningTabungan(no_rek, pemilik, saldo_awal)
            elif jenis == "2":
                rek_baru = RekeningGiro(no_rek, pemilik, saldo_awal)
            else:
                print("Jenis rekening tidak valid.")
                return

            self.__daftar_rekening.append(rek_baru)
            print(f"Rekening {rek_baru.__class__.__name__} berhasil ditambahkan!")

        elif pilihan == "2":
            no_rek = input("Masukkan Nomor Rekening Tujuan: ").strip()
            rek = self._cari_rekening_by_nomor(no_rek)
            if rek is None:
                print("Rekening tidak ditemukan.")
                return

            print("Jenis Transaksi: [1] Setor  [2] Tarik")
            j_trx = input("Pilih jenis (1/2): ").strip()
            jenis_str = "Setor" if j_trx == "1" else ("Tarik" if j_trx == "2" else "")
            if not jenis_str:
                print("Jenis transaksi tidak valid.")
                return

            try:
                nominal = float(input("Nominal (Rp)     : "))
            except ValueError:
                print("Nominal harus berupa angka.")
                return

            ket = input("Keterangan       : ").strip() or "-"
            id_trx = f"TRX-{self.__counter_transaksi:03d}"
            self.__counter_transaksi += 1

            # Membuat objek Transaksi yang berelasi dengan 1 objek Rekening
            trx = Transaksi(id_trx, rek, jenis_str, nominal, ket)
            sukses, pesan = trx.proses_transaksi()
            self.__daftar_transaksi.append(trx)
            print(f"[{trx.get_status_transaksi()}] {pesan}")
        else:
            print("Pilihan submenu tidak valid.")

    # --- 2. Menu Tampilkan Data ---
    def menu_tampilkan_data(self) -> None:
        print("--- DAFTAR REKENING ---")
        if not self.__daftar_rekening:
            print("Belum ada data rekening.")
        else:
            for idx, rek in enumerate(self.__daftar_rekening, start=1):
                print(f"{idx}. {rek.info_ringkas()}")

        print("--- RIWAYAT TRANSAKSI ---")
        if not self.__daftar_transaksi:
            print("Belum ada riwayat transaksi.")
        else:
            for idx, trx in enumerate(self.__daftar_transaksi, start=1):
                print(f"{idx}. {trx.info_transaksi()}")

    # --- 3. Menu Cari Data ---
    def menu_cari_data(self) -> None:
        print(" --- CARI DATA REKENING ---")
        kata_kunci = input("Masukkan Nomor Rekening atau Nama Pemilik: ").strip().lower()
        hasil = [
            rek for rek in self.__daftar_rekening
            if kata_kunci in rek.get_no_rekening().lower()
            or kata_kunci in rek.get_pemilik().lower()
        ]

        if not hasil:
            print("Data rekening tidak ditemukan.")
        else:
            print(f"Ditemukan {len(hasil)} rekening:")
            for rek in hasil:
                print(f"- {rek.info_ringkas()}")

    # --- 4. Menu Ubah Data ---
    def menu_ubah_data(self) -> None:
        print(" --- UBAH DATA REKENING ---")
        no_rek = input("Masukkan Nomor Rekening yang ingin diubah: ").strip()
        rek = self._cari_rekening_by_nomor(no_rek)
        if rek is None:
            print("Rekening tidak ditemukan.")
            return

        print(f"Data saat ini: {rek.info_ringkas()}")
        print("1. Ubah Nama Pemilik")
        print("2. Ubah Status Rekening (Aktif / Diblokir)")
        opsi = input("Pilih data yang diubah (1/2): ").strip()

        if opsi == "1":
            nama_baru = input("Masukkan Nama Pemilik Baru: ").strip()
            rek.ubah_pemilik(nama_baru)
            print("Nama pemilik berhasil diperbarui.")
        elif opsi == "2":
            status_baru = input("Masukkan Status Baru (Aktif/Diblokir): ").strip().capitalize()
            if rek.ubah_status(status_baru):
                print(f"Status rekening berhasil diubah menjadi {status_baru}.")
            else:
                print("Status tidak valid. Gunakan 'Aktif' atau 'Diblokir'.")
        else:
            print("Pilihan tidak valid.")

    # --- 5. Menu Cek Status Data ---
    def menu_cek_status_data(self) -> None:
        print(" --- CEK STATUS DATA REKENING ---")
        no_rek = input("Masukkan Nomor Rekening: ").strip()
        rek = self._cari_rekening_by_nomor(no_rek)
        if rek is None:
            print("Rekening tidak ditemukan.")
            return

        print(f"Nomor Rekening : {rek.get_no_rekening()}")
        print(f"Nama Pemilik   : {rek.get_pemilik()}")
        print(f"Jenis Rekening : {rek.__class__.__name__}")
        print(f"Status Akun    : {rek.get_status()}")
        print(f"Saldo Saat Ini : Rp{rek.get_saldo():,.2f}")

        # Menampilkan informasi spesifik sesuai subclass
        if isinstance(rek, RekeningTabungan):
            print(f"Bunga Tabungan : {rek.get_bunga_persen()}% (Estimasi: Rp{rek.hitung_bunga():,.2f})")
            print(f"Batas Tarik    : Rp{rek.get_batas_tarik():,.2f}")
        elif isinstance(rek, RekeningGiro):
            print(f"Limit Overdraft: Rp{rek.get_limit_overdraft():,.2f}")
            print(f"Maksimal Tarik : Rp{rek.cek_sisa_limit_tarik():,.2f}")

    # --- Loop Menu Utama CLI ---
    def jalankan(self) -> None:
        while True:
            print("=========================================")
            print("    APLIKASI REKENING BANK MINI (CLI)    ")
            print("=========================================")
            print("1. Tambah data")
            print("2. Tampilkan data")
            print("3. Cari data")
            print("4. Ubah data")
            print("5. Cek status data")
            print("6. Keluar dari program")
            print("=========================================")
            pilihan = input("Pilih menu (1-6): ").strip()

            if pilihan == "1":
                self.menu_tambah_data()
            elif pilihan == "2":
                self.menu_tampilkan_data()
            elif pilihan == "3":
                self.menu_cari_data()
            elif pilihan == "4":
                self.menu_ubah_data()
            elif pilihan == "5":
                self.menu_cek_status_data()
            elif pilihan == "6":
                print("Terima kasih telah menggunakan Aplikasi Rekening Bank Mini.")
                break
            else:
                print("Menu tidak valid. Silakan pilih angka 1 sampai 6.")


if __name__ == "__main__":
    app = BankMiniApp()
    app.jalankan()