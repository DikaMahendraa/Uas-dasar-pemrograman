import csv

BOBOT_TUGAS = 0.30
BOBOT_UTS = 0.35
BOBOT_UAS = 0.35
FILE_DATA = "datanew1_mahasiswa.csv"

# class untuk mahasiswa
class Mahasiswa:
    def __init__(self, nim: str, nama: str):
        self.nim = nim
        self.nama = nama
        self.nilai = {"tugas": 0, "uts": 0, "uas": 0}
        self.hadir = 0
        self.total_pertemuan = 0

    def nilai_akhir(self):
        hitung = lambda n: (
            BOBOT_TUGAS * n["tugas"] +
            BOBOT_UTS * n["uts"] +
            BOBOT_UAS * n["uas"]
        )
        return hitung(self.nilai)

    def grade(self):
        n = self.nilai_akhir()
        if n >= 85:
            return "A"
        elif n >= 70:
            return "B"
        elif n >= 55:
            return "C"
        elif n >= 40:
            return "D"
        return "E"

    def persentase_hadir(self):
        return 0 if self.total_pertemuan == 0 else (self.hadir / self.total_pertemuan) * 100
    
class SistemAkademik:
    def __init__(self):
        self.mahasiswa_list = []

    def _cari(self, nim):
        return next((m for m in self.mahasiswa_list if m.nim == nim), None)

    def tambah_mahasiswa(self):
        nim = input("NIM        : ")
        if self._cari(nim):
            print("NIM sudah terdaftar")
            return
        nama = input("Nama       : ")
        self.mahasiswa_list.append(Mahasiswa(nim, nama))
        print("Mahasiswa ditambahkan")

    def input_nilai(self):
        nim = input("NIM        : ")
        mhs = self._cari(nim)
        if not mhs:
            print("Data tidak ditemukan")
            return

        for key in mhs.nilai:
            while True:
                nilai = int(input(f"Nilai {key.upper():7}: "))
                if 0 <= nilai <= 100:
                    mhs.nilai[key] = nilai
                    break
                print("Rentang nilai 0–100")

    def presensi(self):
        pertemuan = int(input("Pertemuan ke-: "))
        jenis = "Teori" if pertemuan % 2 != 0 else "Praktikum"
        print(f" sesi {jenis}")

        for mhs in self.mahasiswa_list:
            status = input(f"{mhs.nama:<15} (Hadir/Alpha/Izin): ").lower()
            mhs.total_pertemuan += 1
            if status == "hadir":
                mhs.hadir += 1

    def laporan(self):
        print("\n=== LAPORAN AKADEMIK ===")
        print(f"{'NIM':<10}{'Nama':<15}{'Akhir':<8}{'Grade':<7}{'Hadir'}")
        print("-" * 50)

        for mhs in self.mahasiswa_list:
            print(
                f"{mhs.nim:<10}{mhs.nama:<15}"
                f"{mhs.nilai_akhir():<8.2f}"
                f"{mhs.grade():<7}"
                f"{mhs.persentase_hadir():.1f}%"
            )

    def simpan(self):
        with open(FILE_DATA, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["NIM", "Nama", "Tugas", "UTS", "UAS", "Hadir", "Total"])
            for mhs in self.mahasiswa_list:
                writer.writerow([
                    mhs.nim, mhs.nama,
                    mhs.nilai["tugas"], mhs.nilai["uts"], mhs.nilai["uas"],
                    mhs.hadir, mhs.total_pertemuan
                ])
        print("Data tersimpan")

    def baca(self):
        try:
            with open(FILE_DATA, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    m = Mahasiswa(row["NIM"], row["Nama"])
                    m.nilai["tugas"] = int(row["Tugas"])
                    m.nilai["uts"] = int(row["UTS"])
                    m.nilai["uas"] = int(row["UAS"])
                    m.hadir = int(row["Hadir"])
                    m.total_pertemuan = int(row["Total"])
                    self.mahasiswa_list.append(m)
        except FileNotFoundError:
            pass

# ================= MAIN =================
def main():
    sistem = SistemAkademik()
    sistem.baca()

    while True:
        print("\n1.Tambah  2.Nilai  3.Presensi  4.Laporan  5.Keluar")
        pilih = input(">> ")

        if pilih == "1":
            sistem.tambah_mahasiswa()
        elif pilih == "2":
            sistem.input_nilai()
        elif pilih == "3":
            sistem.presensi()
        elif pilih == "4":
            sistem.laporan()
        elif pilih == "5":
            sistem.simpan()
            print("Program selesai")
            break
        else:
            print("Menu tidak valid")

main()

# copyright dika & mahesa 2025
