"""
Konaklama sınıfı - Otel / konaklama bilgileri.
"""


class Konaklama:
    """Bir seyahate ait konaklama bilgisi."""

    def __init__(
        self,
        otel_adi: str,
        fiyat: float,
        adres: str = "",
        oda_tipi: str = "Standart",
    ):
        self.otel_adi = otel_adi.strip()
        self.fiyat = float(fiyat)
        self.adres = adres.strip()
        self.oda_tipi = oda_tipi.strip() or "Standart"

    def toplam_fiyat(self, gun_sayisi: int) -> float:
        """Gecelik fiyat x gün sayısı."""
        return self.fiyat * max(gun_sayisi, 0)

    def to_dict(self) -> dict:
        return {
            "otel_adi": self.otel_adi,
            "fiyat": self.fiyat,
            "adres": self.adres,
            "oda_tipi": self.oda_tipi,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Konaklama":
        return cls(
            otel_adi=d["otel_adi"],
            fiyat=d["fiyat"],
            adres=d.get("adres", ""),
            oda_tipi=d.get("oda_tipi", "Standart"),
        )

    def __repr__(self):
        return f"Konaklama({self.otel_adi!r}, {self.fiyat} TL/gece)"
