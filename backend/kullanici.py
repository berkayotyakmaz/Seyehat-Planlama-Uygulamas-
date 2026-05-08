"""
Kullanici sınıfı - Giriş yapan kullanıcı bilgisi.
"""


class Kullanici:
    """Sistem kullanıcısı."""

    def __init__(
        self,
        kullanici_id: int,
        ad: str,
        email: str = "",
    ):
        self.kullanici_id = kullanici_id
        self.ad = ad.strip()
        self.email = email.strip().lower()

    def to_dict(self) -> dict:
        return {
            "kullanici_id": self.kullanici_id,
            "ad": self.ad,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kullanici":
        return cls(
            kullanici_id=d["kullanici_id"],
            ad=d["ad"],
            email=d.get("email", ""),
        )

    def __repr__(self):
        return f"Kullanici({self.ad!r})"
