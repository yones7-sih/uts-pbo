class Rekening:
    """Superclass yang merepresentasikan rekening bank secara umum."""

    def __init__(self, no_rekening: str, pemilik: str, saldo_awal: float = 0.0, status: str = "Aktif"):
        # Atribut private (enkapsulasi menggunakan prefix double underscore __)
        self.__no_rekening = no_rekening
        self.__pemilik = pemilik
        self.__saldo = float(saldo_awal)
        self.__status = status

    # --- Getter untuk menjaga enkapsulasi ---
    def get_no_rekening(self) -> str:
        return self.__no_rekening

    def get_pemilik(self) -> str:
        return self.__pemilik

    def get_saldo(self) -> float:
        return self.__saldo

    def get_status(self) -> str:
        return self.__status

    # --- Method khusus / Setter terkontrol untuk mengubah data ---
    def ubah_pemilik(self, pemilik_baru: str) -> None:
        if pemilik_baru.strip():
            self.__pemilik = pemilik_baru.strip()

    def ubah_status(self, status_baru: str) -> bool:
        if status_baru in ("Aktif", "Diblokir"):
            self.__status = status_baru
            return True
        return False

    def _set_saldo(self, saldo_baru: float) -> None:
        """Method internal (protected) agar subclass dapat memperbarui saldo secara terkontrol."""
        self.__saldo = float(saldo_baru)

    # --- Method tambahan operasi rekening ---
    def setor(self, jumlah: float) -> tuple[bool, str]:
        """Menambah saldo ke rekening jika rekening aktif dan nominal valid."""
        if self.__status != "Aktif":
            return False, "Gagal: Rekening dalam status Diblokir."
        if jumlah <= 0:
            return False, "Gagal: Nominal setor harus lebih dari 0."
        self.__saldo += jumlah
        return True, f"Setor sebesar Rp{jumlah:,.2f} berhasil."

    def tarik(self, jumlah: float) -> tuple[bool, str]:
        """Mengurangi saldo rekening jika rekening aktif dan saldo mencukupi."""
        if self.__status != "Aktif":
            return False, "Gagal: Rekening dalam status Diblokir."
        if jumlah <= 0:
            return False, "Gagal: Nominal tarik harus lebih dari 0."
        if jumlah > self.__saldo:
            return False, "Gagal: Saldo tidak mencukupi."
        self.__saldo -= jumlah
        return True, f"Penarikan sebesar Rp{jumlah:,.2f} berhasil."

    def info_ringkas(self) -> str:
        """Mengembalikan ringkasan informasi rekening."""
        return (
            f"[{self.__no_rekening}] {self.__pemilik} | "
            f"Jenis: {self.__class__.__name__} | "
            f"Saldo: Rp{self.__saldo:,.2f} | Status: {self.__status}"
        )


class RekeningTabungan(Rekening):
    """Subclass dari Rekening khusus untuk jenis rekening tabungan."""

    def __init__(
        self,
        no_rekening: str,
        pemilik: str,
        saldo_awal: float = 0.0,
        bunga_persen: float = 2.5,
        batas_tarik: float = 5_000_000.0,
        status: str = "Aktif",
    ):
        # Memanggil constructor superclass Rekening
        super().__init__(no_rekening, pemilik, saldo_awal, status)
        # Atribut private khusus RekeningTabungan
        self.__bunga_persen = float(bunga_persen)
        self.__batas_tarik = float(batas_tarik)
        self.__jenis_tabungan = "Reguler"

    # --- Getter atribut khusus RekeningTabungan ---
    def get_bunga_persen(self) -> float:
        return self.__bunga_persen

    def get_batas_tarik(self) -> float:
        return self.__batas_tarik

    def get_jenis_tabungan(self) -> str:
        return self.__jenis_tabungan

    # --- Method tambahan khusus RekeningTabungan ---
    def hitung_bunga(self) -> float:
        """Menghitung estimasi bunga berdasarkan saldo dan persentase bunga."""
        return self.get_saldo() * (self.__bunga_persen / 100.0)

    def tambah_bunga_ke_saldo(self) -> tuple[bool, str]:
        """Menambahkan hasil perhitungan bunga langsung ke saldo rekening."""
        if self.get_status() != "Aktif":
            return False, "Gagal: Rekening tidak aktif."
        bunga = self.hitung_bunga()
        self._set_saldo(self.get_saldo() + bunga)
        return True, f"Bunga sebesar Rp{bunga:,.2f} berhasil ditambahkan."

    def tarik(self, jumlah: float) -> tuple[bool, str]:
        """Override method tarik dengan validasi batas maksimal penarikan tabungan."""
        if jumlah > self.__batas_tarik:
            return False, f"Gagal: Melebihi batas tarik harian (Rp{self.__batas_tarik:,.2f})."
        return super().tarik(jumlah)


class RekeningGiro(Rekening):
    """Subclass dari Rekening khusus untuk jenis rekening giro (mendukung overdraft)."""

    def __init__(
        self,
        no_rekening: str,
        pemilik: str,
        saldo_awal: float = 0.0,
        limit_overdraft: float = 2_000_000.0,
        biaya_admin: float = 15_000.0,
        status: str = "Aktif",
    ):
        # Memanggil constructor superclass Rekening
        super().__init__(no_rekening, pemilik, saldo_awal, status)
        # Atribut private khusus RekeningGiro
        self.__limit_overdraft = float(limit_overdraft)
        self.__biaya_admin = float(biaya_admin)
        self.__status_fasilitas_giro = "Tersedia"

    # --- Getter atribut khusus RekeningGiro ---
    def get_limit_overdraft(self) -> float:
        return self.__limit_overdraft

    def get_biaya_admin(self) -> float:
        return self.__biaya_admin

    def get_status_fasilitas_giro(self) -> str:
        return self.__status_fasilitas_giro

    # --- Method tambahan khusus RekeningGiro ---
    def cek_sisa_limit_tarik(self) -> float:
        """Menghitung total dana yang bisa ditarik termasuk limit overdraft."""
        return self.get_saldo() + self.__limit_overdraft

    def potong_biaya_admin(self) -> tuple[bool, str]:
        """Memotong biaya administrasi bulanan dari saldo giro."""
        if self.get_status() != "Aktif":
            return False, "Gagal: Rekening tidak aktif."
        if self.get_saldo() - self.__biaya_admin < -self.__limit_overdraft:
            return False, "Gagal: Saldo dan limit overdraft tidak cukup untuk biaya admin."
        self._set_saldo(self.get_saldo() - self.__biaya_admin)
        return True, f"Biaya admin sebesar Rp{self.__biaya_admin:,.2f} telah dipotong."

    def tarik(self, jumlah: float) -> tuple[bool, str]:
        """Override method tarik agar mendukung penarikan hingga batas limit overdraft."""
        if self.get_status() != "Aktif":
            return False, "Gagal: Rekening dalam status Diblokir."
        if jumlah <= 0:
            return False, "Gagal: Nominal tarik harus lebih dari 0."
        if jumlah > self.cek_sisa_limit_tarik():
            return False, f"Gagal: Melebihi saldo + limit overdraft (Maks: Rp{self.cek_sisa_limit_tarik():,.2f})."
        self._set_saldo(self.get_saldo() - jumlah)
        return True, f"Penarikan giro sebesar Rp{jumlah:,.2f} berhasil."