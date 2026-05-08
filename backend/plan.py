"""
Plan sınıfı - Günlük seyahat planı (rota + aktiviteler).
"""
from datetime import datetime


class Plan:
    """Bir seyahatin belirli bir gününe ait plan."""

    def __init__(
        self,
        gun: int,
        tarih: datetime | None = None,
        rota: list[str] | None = None,
        aktiviteler: list[str] | None = None,
    ):
        self.gun = gun
        self.tarih = tarih
        self.rota: list[str] = rota or []
        self.aktiviteler: list[str] = aktiviteler or []

    def rota_ekle(self, yer: str):
        yer = yer.strip()
        if yer and yer not in self.rota:
            self.rota.append(yer)

    def aktivite_ekle(self, aktivite: str):
        aktivite = aktivite.strip()
        if aktivite and aktivite not in self.aktiviteler:
            self.aktiviteler.append(aktivite)

    def rota_sil(self, yer: str):
        if yer in self.rota:
            self.rota.remove(yer)

    def aktivite_sil(self, aktivite: str):
        if aktivite in self.aktiviteler:
            self.aktiviteler.remove(aktivite)

    def to_dict(self) -> dict:
        return {
            "gun": self.gun,
            "tarih": self.tarih.strftime("%d.%m.%Y") if self.tarih else None,
            "rota": self.rota,
            "aktiviteler": self.aktiviteler,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Plan":
        tarih = None
        if d.get("tarih"):
            tarih = datetime.strptime(d["tarih"], "%d.%m.%Y")
        return cls(
            gun=d["gun"],
            tarih=tarih,
            rota=d.get("rota", []),
            aktiviteler=d.get("aktiviteler", []),
        )

    def __repr__(self):
        return f"Plan(Gün {self.gun}, {len(self.rota)} rota, {len(self.aktiviteler)} aktivite)"
