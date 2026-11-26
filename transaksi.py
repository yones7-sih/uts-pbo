from datetime import datetime
from rekening import Rekening


class Transaksi:
    """Class relasi Association yang merepresentasikan transaksi pada satu Rekening."""

    def __init__(
        self,
        id_transaksi: str,
        rekening: Rekening,
        jenis_transaksi: str,
        nominal: float,
        keterangan: str = "-",
    ):
        # Atribut private (enkapsulasi)
        self.__id_transaksi = id_transaksi
        self.__rekening = rekening  # Relasi Association ke 1 objek Rekening
        self.__jenis_transaksi = jenis_transaksi  # Contoh: "Setor", "Tarik", "Bunga", "Biaya Admin"
        self.__nominal = float(nominal)
        self.__keterangan = keterangan
        self.__waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__status_transaksi = "Pending"

    # --- Getter untuk menjaga enkapsulasi ---
    def get_id_transaksi(self) -> str:
        return self.__id_transaksi

    def get_rekening(self) -> Rekening:
        return self.__rekening

    def get_jenis_transaksi(self) -> str:
        return self.__jenis_transaksi

    def get_nominal(self) -> float:
        return self.__nominal

    def get_keterangan(self) -> str:
        return self.__keterangan

    def get_waktu(self) -> str:
        return self.__waktu

    def get_status_transaksi(self) -> str:
        return self.__status_transaksi

    # --- Method tambahan ---
    def proses_transaksi(self) -> tuple[bool, str]:
        """Menjalankan transaksi terhadap objek Rekening terkait dan memperbarui status."""
        if self.__status_transaksi == "Berhasil":
            return False, "Transaksi ini sudah pernah diproses."

        jenis = self.__jenis_transaksi.lower()
        if jenis == "setor":
            sukses, pesan = self.__rekening.setor(self.__nominal)
        elif jenis == "tarik":
            sukses, pesan = self.__rekening.tarik(self.__nominal)
        else:
            sukses, pesan = False, "Jenis transaksi tidak dikenali."

        self.__status_transaksi = "Berhasil" if sukses else "Gagal"
        return sukses, pesan

    def ubah_keterangan(self, keterangan_baru: str) -> None:
        """Mengubah catatan keterangan transaksi secara terkontrol."""
        if keterangan_baru.strip():
            self.__keterangan = keterangan_baru.strip()

    def info_transaksi(self) -> str:
        """Mengembalikan ringkasan lengkap transaksi beserta nomor rekening terkait."""
        return (
            f"[{self.__id_transaksi}] {self.__waktu} | "
            f"Rek: {self.__rekening.get_no_rekening()} ({self.__rekening.get_pemilik()}) | "
            f"{self.__jenis_transaksi}: Rp{self.__nominal:,.2f} | "
            f"Status: {self.__status_transaksi} | Ket: {self.__keterangan}"
        )