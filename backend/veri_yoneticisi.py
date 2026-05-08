"""
Seyahat Veri Yöneticisi - JSON kalıcılık ile tüm seyahatleri yönetir.
Konaklama ve Plan'lar seyahat içinde nested olarak saklanır.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .seyahat import Seyahat
from .konaklama import Konaklama
from .plan import Plan


class VeriYoneticisi:
    """Seyahat verilerini JSON dosyasında yönetir."""

    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self.seyahatler_dosya = os.path.join(veri_klasoru, "seyahatler.json")

        self._seyahatler: Dict[int, Seyahat] = {}
        self._sonraki_id = 1

        self._yukle()

    # ── Kalıcılık ──

    def _yukle(self) -> None:
        if not os.path.exists(self.seyahatler_dosya):
            return
        try:
            with open(self.seyahatler_dosya, "r", encoding="utf-8") as f:
                for d in json.load(f):
                    s = Seyahat.from_dict(d)
                    self._seyahatler[s.seyahat_id] = s
                    self._sonraki_id = max(self._sonraki_id, s.seyahat_id + 1)
        except (json.JSONDecodeError, KeyError):
            pass

    def kaydet(self) -> None:
        with open(self.seyahatler_dosya, "w", encoding="utf-8") as f:
            json.dump(
                [s.to_dict() for s in self._seyahatler.values()],
                f, ensure_ascii=False, indent=2,
            )

    # ── Seyahat CRUD ──

    def seyahat_ekle(
        self,
        gidis_yeri: str,
        tarih: datetime,
        donus_tarihi: datetime,
        kullanici_id: int = 1,
        konaklama: Konaklama | None = None,
        notlar: str = "",
    ) -> Seyahat:
        if not gidis_yeri.strip():
            raise ValueError("Gidiş yeri boş olamaz.")
        if donus_tarihi < tarih:
            raise ValueError("Dönüş tarihi gidiş tarihinden önce olamaz.")

        seyahat = Seyahat(
            seyahat_id=self._sonraki_id,
            gidis_yeri=gidis_yeri,
            tarih=tarih,
            donus_tarihi=donus_tarihi,
            kullanici_id=kullanici_id,
            konaklama=konaklama,
            notlar=notlar,
        )
        seyahat.planlari_olustur()
        self._seyahatler[seyahat.seyahat_id] = seyahat
        self._sonraki_id += 1
        self.kaydet()
        return seyahat

    def seyahat_ekle_hazir(self, seyahat: Seyahat) -> Seyahat:
        """Seed için: hazır Seyahat nesnesini ekler."""
        self._seyahatler[seyahat.seyahat_id] = seyahat
        self._sonraki_id = max(self._sonraki_id, seyahat.seyahat_id + 1)
        self.kaydet()
        return seyahat

    def seyahat_guncelle(
        self,
        seyahat_id: int,
        gidis_yeri: str,
        tarih: datetime,
        donus_tarihi: datetime,
        konaklama: Konaklama | None = None,
        notlar: str = "",
    ) -> Seyahat:
        s = self._seyahatler.get(seyahat_id)
        if not s:
            raise ValueError(f"Seyahat bulunamadı (ID: {seyahat_id}).")
        if s.gecmis_mi():
            raise ValueError("Geçmiş seyahatler düzenlenemez.")
        if donus_tarihi < tarih:
            raise ValueError("Dönüş tarihi gidiş tarihinden önce olamaz.")

        s.gidis_yeri = gidis_yeri.strip()
        s.tarih = tarih
        s.donus_tarihi = donus_tarihi
        s.konaklama = konaklama
        s.notlar = notlar.strip()
        s.planlari_olustur()
        self.kaydet()
        return s

    def seyahat_sil(self, seyahat_id: int) -> bool:
        if seyahat_id not in self._seyahatler:
            return False
        del self._seyahatler[seyahat_id]
        self.kaydet()
        return True

    def seyahat_getir(self, seyahat_id: int) -> Optional[Seyahat]:
        return self._seyahatler.get(seyahat_id)

    def plan_guncelle(self, seyahat_id: int, gun: int, rota: list[str], aktiviteler: list[str]):
        """Belirli bir günün planını günceller."""
        s = self._seyahatler.get(seyahat_id)
        if not s:
            raise ValueError("Seyahat bulunamadı.")
        for p in s.planlar:
            if p.gun == gun:
                p.rota = rota
                p.aktiviteler = aktiviteler
                self.kaydet()
                return
        raise ValueError(f"Gün {gun} bulunamadı.")

    # ── Sorgular ──

    def tum_seyahatler(self) -> List[Seyahat]:
        return sorted(self._seyahatler.values(), key=lambda s: s.tarih, reverse=True)

    def aktif_seyahatler(self) -> List[Seyahat]:
        return [s for s in self._seyahatler.values() if s.aktif_mi()]

    def gelecek_seyahatler(self) -> List[Seyahat]:
        return sorted(
            [s for s in self._seyahatler.values() if s.gelecek_mi()],
            key=lambda s: s.tarih,
        )

    def gecmis_seyahatler(self) -> List[Seyahat]:
        return sorted(
            [s for s in self._seyahatler.values() if s.gecmis_mi()],
            key=lambda s: s.tarih, reverse=True,
        )

    # ── İstatistik ──

    def genel_istatistikler(self) -> dict:
        tum = list(self._seyahatler.values())
        toplam_harcama = sum(s.toplam_butce() for s in tum)
        aktif = [s for s in tum if s.aktif_mi()]
        gelecek = [s for s in tum if s.gelecek_mi()]

        return {
            "toplam_seyahat": len(tum),
            "aktif_seyahat": len(aktif),
            "yaklasan_seyahat": len(gelecek),
            "toplam_harcama": toplam_harcama,
        }

    def sehir_dagilimi(self) -> dict:
        """En çok gidilen şehirler."""
        dagilim: dict[str, int] = {}
        for s in self._seyahatler.values():
            dagilim[s.gidis_yeri] = dagilim.get(s.gidis_yeri, 0) + 1
        return dagilim

    def ortalama_sure(self) -> float:
        tum = list(self._seyahatler.values())
        if not tum:
            return 0
        return sum(s.gun_sayisi() for s in tum) / len(tum)
