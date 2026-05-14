"""
Seyahat sınıfı - Ana model. Konaklama ve Plan'ları composition ile içerir.
"""
from datetime import datetime, timedelta

from .konaklama import Konaklama
from .plan import Plan


class Seyahat:
    """Bir seyahat planı."""

    def __init__(
        self,
        seyahat_id: int,
        gidis_yeri: str,
        tarih: datetime,
        donus_tarihi: datetime,
        kullanici_id: int = 1,
        konaklama: Konaklama | None = None,
        planlar: list[Plan] | None = None,
        notlar: str = "",
    ):
        self.seyahat_id = seyahat_id
        self.gidis_yeri = gidis_yeri.strip()
        self.tarih = tarih
        self.donus_tarihi = donus_tarihi
        self.kullanici_id = kullanici_id
        self.konaklama = konaklama
        self.planlar: list[Plan] = planlar or []
        self.notlar = notlar.strip()

    def gun_sayisi(self) -> int:
        return (self.donus_tarihi - self.tarih).days + 1

    def toplam_butce(self) -> float:
        if self.konaklama:
            return self.konaklama.toplam_fiyat(self.gun_sayisi())
        return 0.0

    @staticmethod
    def _bugun() -> datetime:
        """Saat 00:00:00'a normalize edilmiş 'bugün'."""
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def aktif_mi(self) -> bool:
        bugun = self._bugun()
        return self.tarih <= bugun <= self.donus_tarihi

    def gelecek_mi(self) -> bool:
        return self.tarih > self._bugun()

    def gecmis_mi(self) -> bool:
        return self.donus_tarihi < self._bugun()

    def kalan_gun(self) -> int | None:
        """Gelecek seyahat ise kaç gün kaldığını döner."""
        bugun = self._bugun()
        if self.tarih <= bugun:
            return None
        return (self.tarih - bugun).days

    def duzenlenebilir_mi(self) -> bool:
        """Geçmiş seyahatler düzenlenemez kuralının tek kaynağı."""
        return not self.gecmis_mi()

    def durum_metni(self) -> str:
        if self.gecmis_mi():
            return "GECMİŞ"
        if self.aktif_mi():
            return "AKTİF"
        kalan = self.kalan_gun()
        if kalan is not None:
            return f"{kalan} GÜN KALDI"
        return "YAKLAŞIYOR"

    def planlari_olustur(self):
        """Gün sayısı kadar boş plan oluşturur (mevcutları korur)."""
        mevcut = {p.gun: p for p in self.planlar}
        yeni_planlar = []
        for i in range(1, self.gun_sayisi() + 1):
            if i in mevcut:
                plan = mevcut[i]
                plan.tarih = self.tarih + timedelta(days=i - 1)
                yeni_planlar.append(plan)
            else:
                yeni_planlar.append(
                    Plan(gun=i, tarih=self.tarih + timedelta(days=i - 1))
                )
        self.planlar = yeni_planlar

    def kaybolacak_dolu_planlar(self, yeni_gun_sayisi: int) -> list[int]:
        """
        Gün sayısı azaltıldığında veri kaybı olacak gün numaralarını döner.
        Sadece içeriği (rota veya aktivite) DOLU olan günler sayılır.
        """
        if yeni_gun_sayisi >= self.gun_sayisi():
            return []
        kayip = []
        for p in self.planlar:
            if p.gun > yeni_gun_sayisi and (p.rota or p.aktiviteler):
                kayip.append(p.gun)
        return kayip

    def to_dict(self) -> dict:
        return {
            "seyahat_id": self.seyahat_id,
            "gidis_yeri": self.gidis_yeri,
            "tarih": self.tarih.strftime("%d.%m.%Y"),
            "donus_tarihi": self.donus_tarihi.strftime("%d.%m.%Y"),
            "kullanici_id": self.kullanici_id,
            "konaklama": self.konaklama.to_dict() if self.konaklama else None,
            "planlar": [p.to_dict() for p in self.planlar],
            "notlar": self.notlar,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Seyahat":
        konaklama = None
        if d.get("konaklama"):
            konaklama = Konaklama.from_dict(d["konaklama"])

        planlar = [Plan.from_dict(p) for p in d.get("planlar", [])]

        return cls(
            seyahat_id=d["seyahat_id"],
            gidis_yeri=d["gidis_yeri"],
            tarih=datetime.strptime(d["tarih"], "%d.%m.%Y"),
            donus_tarihi=datetime.strptime(d["donus_tarihi"], "%d.%m.%Y"),
            kullanici_id=d.get("kullanici_id", 1),
            konaklama=konaklama,
            planlar=planlar,
            notlar=d.get("notlar", ""),
        )

    def __repr__(self):
        return f"Seyahat({self.gidis_yeri!r}, {self.tarih:%d.%m.%Y})"
